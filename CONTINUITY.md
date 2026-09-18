# Continuity Ledger

## Goal (incl. success criteria)

Maintain /whathappened (this repo). New (2026-09-18): add an optional Jev
(System One) signal filter at SKILL Step 7 that scores/ranks high-signal X
posts via OpenRouter's /api/alpha/decisions (option 1: local standalone script,
OPENROUTER_API_KEY from env). Success: live-verified on real batches, oracle-
reviewed, committed + pushed.

## Constraints/Assumptions

- whathappened is Grok-Build-only (needs native X tools). The Jev filter is
  LOCAL-side (script + same key as Sonar grounding); it never runs inside Grok
  Build.
- Jev is a judge/scorer, NOT a summarizer/retriever: it prunes+ranks, never
  writes the brief. Never block the brief on Jev (fall back to in-head score).
- Jev is a decisions model: served on /api/alpha/decisions, NOT chat/completions;
  also absent from the public /v1/models catalog.

## Key decisions

- Jev filter = option 1: `skills/whathappened/scripts/signal_filter.py`
  (stdlib-only, urllib; one request per batch; 4 atomic judgments/post:
  signal Score, on_entity Noul, disclosure Noul, category Choice). All policy
  + arithmetic in code (confidence-gated on_entity drop, normalized ranking;
  fails loudly on missing key / API error).
- Category answer-space now `launch/milestone/debate/analysis/meme/other`.
  `analysis` was added after amp oracle review flagged it missing (bug/medium:
  downstream could never branch on it).
- Committed + pushed as a0fde5a on main (2026-09-18). Their working doc edits
  (HTML report Step 9 etc.) also landed in this/prior commit(s).

## State

### Done

- Jev signal filter built + live-verified on 2 use-cases (webmcp appfunctions
  for mobile; jev for token generation). ~$0.00009/batch at ~4-5 posts.
- amp oracle review (2026-09-18): 1 bug/medium — `analysis` missing from Choice
  answer space; fixed + SKILL docs now enumerate the set.
- Commit + push a0fde5a (main), 2026-09-18 17:49.

### Now

- update continuity file — 2026-09-18 18:11

### Next

- None pending in this repo. Consider integrating an `analysis`-branch in the
  synthesis template only when one actually branches on category; otherwise
  leave signal-based ranking as is.

## Open questions

- None blocking. Jev `jevv-1.13` limits (per docs) may improve on later models;
  recheck morphology/pricing when the model alias bumps.

## Working set (files/ids/commands)

- modified: /Users/manik/Github/whathappened/CONTINUITY.md
- commands:
  - `cd /Users/manik/Github/whathappened && cat CONTINUITY.md`
  - `cd /Users/manik/Github/whathappened && cat CONTINUITY.md`

## Activity log

- [2026-09-18 14:28] <skill name="jev" location="/Users/manik/.agents/skills/jev/SKILL.md"> — modified: 0, read: 0, commands: 23, errors: 2
- [2026-09-18 17:21] check https://openrouter.ai/typesafe and use openrouter key, we already use for sonar grounding — modified: 0, read: 0, commands: 5, errors: 0
- [2026-09-18 17:25] option 1 — modified: 3, read: 0, commands: 8, errors: 0
- [2026-09-18 17:36] let's run the test for 'webmcp appfunctions integration for mobile' and 'jev for token generation' — modified: 2, read: 0, commands: 7, errors: 0
- [2026-09-18 17:40] let's add analysis category, before this have a check with amp oracle — modified: 4, read: 0, commands: 9, errors: 1
- [2026-09-18 17:49] commit and push — modified: 1, read: 0, commands: 9, errors: 1
- [2026-09-18 18:11] update continuity file — modified: 1, read: 0, commands: 2, errors: 0

## Project learnings

- OpenRouter serves Jev (decisions model) at `/api/alpha/decisions`, and only
  there: chat/completions 400s ("is a decisions model…"), and it's absent from
  the public /v1/models catalog (445 entries, zero typesafe/*). Model resolves
  to `typesafe/jev-1.13-20260917` for both ~typesafe/jev-latest and the pinned
  ID. Pricing ~$0.042/M input, $0/M output (measured: ~$0.0001 per batch).
- grok-cli reads its own `~/.config/grok-cli/config.json` for the Sonar key;
  the Jev filter instead reads `OPENROUTER_API_KEY` from env — same key value,
  different lookup path.
- Per-item Score + Noul judgments batched into ONE decisions request are
  parallel and cheap; a small per-post experiment showed the `analysis`
  category (added post-oracle) fixed the earlier `other(99%)` misfires on
  deep-dive/standards posts.

