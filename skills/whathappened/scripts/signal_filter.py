#!/usr/bin/env python3
"""Jev (System One) signal filter for ranking candidate X posts in /whathappened.

Runs the exact "score = engagement x freshness x authority x on_entity" idea
from SKILL.md Step 7, but lets Jev own the *judgments* (signal, on-entity,
disclosure, category) while this script owns all arithmetic and policy.

What this is NOT:
  - Not a research retriever (that is Sonar / grok-cli). Jev only judges.
  - Not a chat model call. Jev is served through OpenRouter's
    /api/alpha/decisions endpoint, not chat/completions.
  - Not the brief writer. It returns a pruned, scored list you then rank/synthesize.

KEY:  read from OPENROUTER_API_KEY (env). Same key grok-cli uses for Sonar.

Example:
    python3 signal_filter.py --topic "Kimi K3" tour-kimi-k3.json
    cat latest.json | python3 signal_filter.py --topic "Kimi K3"
    python3 signal_filter.py --topic "Kimi K3" in.json --out scored.json --ok 3 --drop-on-entity-below 0.6

Primitives (see docs.typesafe.ai/primitives):
  - Noul  : on_entity (is this post actually about the topic?) and
            disclosure (does it reveal new, previously unknown info?)
  - Score : signal (0 = noise ... 4 = origin/official), 5 levels
  - Choice: category (launch/milestone/debate/meme/other)

Policy lives HERE, in code, not in the questions (matches the skill's
"weights and thresholds live in code" rule).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

API_URL = "https://openrouter.ai/api/alpha/decisions"
DEFAULT_MODEL = "~typesafe/jev-latest"

# Signal levels, low -> high. Must match the Score instructions/criteria we send.
SIGNAL_LEVELS = [
    "Noise; not relevant to the topic",
    "Marginal; restates what is already known",
    "Useful; adds a detail or confirms a report",
    "High signal; new information or an authoritative statement",
    "Origin; the post that started the story, or a first-party official statement",
]

CATEGORY_CRITERIA = {
    "launch": "Announcing a new product, model, release, or service",
    "milestone": "A company or personal milestone claim",
    "debate": "Takes a position in a public controversy or debate",
    "analysis": "An analytical post or commentary: a methodology, deep-dive, or opinion with reasoning (not a claimed event)",
    "meme": "Humor, meme, or low-effort content",
    "other": "Anything else",
}


def key() -> str:
    k = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not k:
        sys.exit(
            "signal_filter.py: OPENROUTER_API_KEY not set. "
            "(Same key grok-cli uses for Sonar grounding.)"
        )
    return k


def post_questions(i: int, topic: str) -> dict:
    """One (small, atomic) question per judgment on posts[i]."""
    return {
        f"post_{i}_signal": {
            "type": "score",
            "instructions": (
                f"How important is `posts[{i}]` as evidence for a news briefing "
                f"about `topic`?"
            ),
            # Standalone, situation-based levels (no numerals), per jev guidance.
            "criteria": SIGNAL_LEVELS,
        },
        f"post_{i}_on_entity": {
            "type": "noul",
            "instructions": f"Is `posts[{i}]` actually about `topic`?",
        },
        f"post_{i}_disclosure": {
            "type": "noul",
            "instructions": (
                f"Does `posts[{i}]` reveal new, previously unknown information "
                f"about `topic`, beyond restating what is already known?"
            ),
        },
        f"post_{i}_category": {
            "type": "choice",
            "instructions": f"Which best describes the main intent of `posts[{i}]`?",
            "criteria": CATEGORY_CRITERIA,
        },
    }


def build_payload(posts: list, topic: str, model: str) -> dict:
    """One request for the whole batch (speculative fan-out, one bill)."""
    questions = {}
    for i in range(len(posts)):
        questions.update(post_questions(i, topic))
    return {
        "model": model,
        "state": {"topic": topic, "posts": posts},
        "questions": questions,
    }


def call(payload: dict, timeout: int = 120) -> dict:
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {key()}",
            "Content-Type": "application/json",
            # Identifies the app on OpenRouter; put a real URL here if you ship it.
            "X-Title": "whathappened-signal-filter",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:1000]
        sys.exit(f"signal_filter.py: HTTP {e.code} from Jev API: {body}")
    except Exception as e:  # network/timeouts -> fail loudly, do not guess scores
        sys.exit(f"signal_filter.py: request failed: {e}")


def normalize_score(probabilities: dict, n_levels: int, noul: float | None = None) -> float:
    """Composite: normalized signal (0..1) gated by on-entity confidence.

    Jev's raw 'score' is a probability-weighted level mean, weakly calibrated
    as a number (per jev guidance: do not interpolate a quantity from it).
    We normalize to 0..1 for ranking and blend with an on-entity Noul so an
    off-topic viral post can't dominate. If probabilities are absent we fall
    back to the reported 'score' value.
    """
    if probabilities:
        norm = sum(float(k) * v for k, v in probabilities.items()) / (n_levels - 1)
    else:
        norm = 0.0  # caller supplies a fallback below via noul
    if noul is not None:
        # on-entity confidence as a soft multiplier (policy, in code)
        norm = norm * noul
    return round(min(max(norm, 0.0), 1.0), 4)


def apply_policy(
    answers: dict, posts: list, topic: str, *, drop_on_entity_below: float,
    nan_help: bool = False,
) -> list[dict]:
    """Turn raw answers into ranked, filtered results (all policy in code)."""
    n = len(posts)
    n_levels = len(SIGNAL_LEVELS)
    results = []
    for i in range(n):
        a_signal = answers.get(f"post_{i}_signal") or {}
        a_entity = answers.get(f"post_{i}_on_entity") or {}
        a_disc = answers.get(f"post_{i}_disclosure") or {}
        a_cat = answers.get(f"post_{i}_category") or {}

        sig = (a_signal.get("probabilities") or {})
        sig_val = (a_signal.get("score") or 0.0)
        on_entity = a_entity.get("noul", 0.0)
        disclosure = a_disc.get("noul", 0.0)

        # Fall back to raw score when probabilities are missing (cheap safety).
        norm = normalize_score(sig, n_levels, noul=on_entity)
        if not sig:
            norm = round(min(max(sig_val / (n_levels - 1) * on_entity, 0.0), 1.0), 4)

        results.append({
            "index": i,
            "handle": (posts[i].get("handle") or ""),
            "text_preview": (posts[i].get("text") or "")[:200],
            "category": a_cat.get("choice"),
            "category_confidence": round(a_cat.get("confidence", 0.0) * 100, 1),
            "signal_raw": round(sig_val, 2),
            "signal_prob": {  # keep P(each level) for debuggability
                k: round(v, 3) for k, v in sorted(sig.items(), key=lambda x: float(x[0]))
            },
            "signal_confidence": round(a_signal.get("confidence", 0.0), 2),
            "on_entity": round(on_entity, 2),
            "disclosure": round(disclosure, 2),
            "normalized": norm,
        })

    # Policy: drop off-topic or clearly non-signal posts.
    kept = [
        r for r in results
        if r["on_entity"] >= drop_on_entity_below and r["normalized"] >= 0.01
    ]
    # Rank: normalized signal desc; then raw signal desc; then confidence desc.
    kept.sort(
        key=lambda r: (
            -r["normalized"],
            -r["signal_raw"],
            -r["signal_confidence"],
        )
    )
    return kept, results


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Jev signal filter for /whathappened post ranking (option 1: local)."
    )
    ap.add_argument("input", nargs="?", help="JSON file of posts. Reads stdin if omitted.")
    ap.add_argument("--topic", required=True, help="Primary topic/entity (for on-entity checks).")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--out", help="Write ranked results to this file (JSON).")
    ap.add_argument(
        "--max-posts", type=int, default=40,
        help="Cap on posts per Jev request (default 40; raise carefully, 32K ctx)."
    )
    ap.add_argument(
        "--drop-on-entity-below", type=float, default=0.6,
        help="Drop posts whose on-entity Noul < this. (policy, in code)",
    )
    ap.add_argument(
        "--ok", type=int, default=None,
        help="Print only this many top-ranked kept posts (verbose output).",
    )
    args = ap.parse_args()

    raw = sys.stdin.read() if not args.input else open(args.input).read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        sys.exit(f"signal_filter.py: bad input JSON: {e}")

    posts = data.get("posts") if isinstance(data, dict) else data
    if not isinstance(posts, list) or not posts:
        sys.exit("signal_filter.py: input must be a JSON array of posts or {posts: [...]}.")
    topic = (data.get("topic") if isinstance(data, dict) else None) or args.topic
    posts = posts[: args.max_posts]

    payload = build_payload(posts, topic, args.model)
    resp = call(payload)

    kept, all_results = apply_policy(
        resp.get("answers", {}), posts, topic,
        drop_on_entity_below=args.drop_on_entity_below,
    )
    summary = {
        "topic": topic,
        "model": resp.get("model"),
        "n_input_posts": len(posts),
        "n_kept": len(kept),
        "usage": resp.get("usage"),
        "dropped": [
            r for r in all_results
            if r["on_entity"] < args.drop_on_entity_below or r["normalized"] < 0.01
        ],
        "ranked": kept,
    }

    out = args.out
    if out:
        with open(out, "w") as f:
            json.dump(summary, f, indent=2)
    else:
        json.dump(summary, sys.stdout, indent=2)

    if args.ok:
        print(f"\n# Top {args.ok} kept (policy in code, thresholds tunable):", file=sys.stderr)
        for r in kept[: args.ok]:
            print(f"  [{r['normalized']:.2f}] {r['handle']}: {r['text_preview']}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
