---
name: whathappened
description: >
  Brief what just happened on a topic and map public opinion from X (Twitter)
  only. Adaptive recency window biased to the freshest coherent story. Soft
  exception: at most one web lookup for entity resolution. Use when the user
  runs /whathappened, or asks what happened / what's going on / X or Twitter
  reaction / public opinion on X about a person, product, launch, or event.
  Supports optional views from accounts the user follows or an X List when a
  usable local Field Theory roster is available. Grok Build only (requires
  native X tools). Neutral analyst tone. No discovery mode in v1.
metadata:
  short-description: "X-only adaptive briefing of events + public opinion"
---

# /whathappened

You are running the **whathappened** skill. Produce a neutral briefing of
**what happened** and what public X or the requested personal audience is saying
about a named topic.

This is not generic research. Follow this file top to bottom.

## Host requirement

You need these tools:

- `x_keyword_search`
- `x_semantic_search`
- `x_thread_fetch`
- `x_user_search`

If they are missing, **stop**. Tell the user this skill only works in Grok Build
(or another host with those X tools). Do not fake an X briefing from web search.

Personal audience requests also need:

- A terminal or shell tool
- A local `ft` command from Field Theory

Do not require Field Theory for the default global-X brief. If a personal
audience was requested and `ft` is unavailable, stop and explain how to run the
same topic globally. Do not silently fall back and label global results as the
user's network.

## Hard rules

1. **X-first synthesis.** All claims about the event and public opinion come
   from X tool results. Never invent posts, handles, engagement, or quotes.
2. **Soft web exception.** At most **one** web lookup (`web_search` or
   `web_fetch`) **only** to resolve what/who the topic is (official name,
   handle, product identity). Do not use web for opinions, sentiment, or
   "what people think." If you use the web lookup, say so in Gaps.
3. **No discovery.** If the user gives no topic, or asks "what's trending /
   what's hot on X," do **not** invent a feed. Ask for a topic in one short
   question.
4. **Natural audience modifiers only.** Understand phrases such as "from people
   I follow" and "only from this list." Continue to ignore flag-like window or
   depth overrides. Infer the window from the pulse below.
5. **Neutral analyst tone.** No hype voice, no dunking, no "the room is
   screaming." Report camps and debates as observed.
6. **Adaptive window, freshest-first.** Do not default to 30 days. Prefer the
   shortest window that still explains the story.
7. **Opinion is not ground truth.** Frame sentiment as public conversation on
   this X sample.
8. **Citations.** Prefer `@handle` plus post links when available. Use the
   host's inline post citation render when you have post citation IDs from X
   tools. Never invent URLs. Never append a trailing dump of unrelated Sources.
9. **Roster data is a filter, not evidence.** Field Theory can establish that an
   author belongs to Following or a List and can supply candidate post IDs. Any
   quoted text, event claim, engagement number, or receipt must still come from
   an X tool result in this run.

Read `references/query-patterns.md` when building search queries.
Read `references/failure-modes.md` when the sample looks thin, mixed, or noisy.

## Pipeline

### Step 0 - Parse topic

- Require a **named topic** (person, org, product, launch, event, controversy).
- Strip intent modifiers for search entities (`sentiment`, `drama`, `takes`)
  but keep them as synthesis focus if the user asked for them.
- Classify loosely: event | person/org | product/release | debate.
- Parse one audience scope and one behavior:

  | User intent | Audience | Behavior |
  |-------------|----------|----------|
  | No personal qualifier | Global X | global |
  | "from my following", "people I follow" | Following | prefer |
  | "only people I follow" | Following | strict |
  | "from this list", "from my {name} list" | X List | prefer |
  | "only from this list" | X List | strict, subject to the completeness gate below |

- If the user asks for more than one personal audience, ask them to choose one.
- Followers and mutuals are not supported. Say so and offer Following or one X
  List instead.

### Step 1 - Resolve a personal audience when requested

Skip this step for Global X.

#### Following

1. Run `ft experts list --json --limit 5000` and save the JSON to a private
   temporary file for exact membership checks. Use restrictive permissions
   (`umask 077`) and delete the file before sending the brief.
2. If the command fails because the snapshot is missing or incomplete, stop.
   Point the user to `ft sync-following` or `ft sync-following --rebuild`.
3. Keep every returned handle. Do not select only loud or classified accounts.
   Check each candidate author mechanically against the saved roster with exact,
   case-insensitive equality using `jq` or an equivalent local command. Never
   decide Following membership from memory.
4. Optionally run `ft experts search "{topic}" --json --limit 20` to choose a
   few useful targeted searches. This supplements the full-roster intersection;
   it never defines the audience.

Following strict mode is allowed only when the roster command succeeds. Always
label Following coverage **sampled**, because X search does not guarantee that
it returned every matching post from all followed accounts.

#### X List

1. Resolve an `x.com/i/lists/{id}` URL or numeric ID. If the user gives only a
   name and no local alias can resolve it, ask for the List URL or ID.
2. Run `ft paths --json`, take `fieldTheoryDir`, and read
   `{fieldTheoryDir}/x-lists/{id}-members-latest.json`.
3. Require a non-empty member array. Check each candidate author mechanically
   against `members[].handle` with exact, case-insensitive equality. Never decide
   List membership from memory.
4. If `{id}-latest.json` exists, use its in-window post IDs and authors as
   discovery hints. Re-fetch selected posts through X tools before quoting or
   citing them.
5. Prefer mode may use a roster without an explicit completeness marker, but
   must call the result sampled. Strict mode requires
   `stats.snapshotComplete: true` in the member digest; otherwise explain that
   strict List filtering is unavailable and offer prefer mode.

Record the audience label, roster count, snapshot timestamp, behavior, and any
completeness warning for the output header.

### Step 2 - Optional entity web lookup (0 or 1 call)

If the topic is ambiguous or you lack an obvious official handle/name:

- Make **at most one** web lookup to resolve identity.
- Extract: canonical name, official `@handle` if stated, aliases, event date
  if the page states one.

If the topic is already clear (e.g. `Kimi K3`, `@sama`), skip web.

### Step 3 - X entity grounding

- Use `x_user_search` for likely official or primary accounts when useful.
- Build aliases: exact phrase, alternate spellings, product codes, cashtags.
- Prefer first-party `from:handle` when you have a confident handle.

### Step 4 - Pulse (first X search)

Run a **cheap Latest** keyword search with a short `since:` window to measure
velocity. Example windows to try first:

- Breaking candidate: last few hours (`since:YYYY-MM-DD` for today, Latest)
- If almost empty: widen once (yesterday / last 2 days) before committing mode

**Commit a mode and window:**

| Pulse signal | Mode | Default window |
|--------------|------|----------------|
| High volume, rising engagement, clear origin | Breaking | last 1–6 hours (minutes if still exploding) |
| Clear same-day event / launch chatter | Same-day | last 24–48 hours |
| Ongoing debate, moderate velocity | Story | last 3–7 days |
| Sparse posts, mostly references to older news | Background | last 14–30 days; still prefer recent posts |

State the chosen **Window** and **Mode** in the brief. Expand later only if:

- No agreement on what happened
- Missing first-party post from the obvious account
- Debates point at an origin post you have not seen

When ranking, prefer recency over raw likes unless an older post is clearly
the origin everyone quotes or replies to - then fetch that thread.

### Step 5 - Search lattice (parallel)

Use multiple lanes. Cap total X tool calls roughly **8–14** for a normal global
run. A personal audience may add up to four focused searches or thread fetches.

| Lane | Tool | Goal |
|------|------|------|
| Top | `x_keyword_search` mode=`Top` | High-engagement consensus |
| Latest | `x_keyword_search` mode=`Latest` + time operators | Fresh narrative |
| Semantic | `x_semantic_search` | Paraphrases and adjacent framing |
| First-party | keyword `from:handle` when known | Official statement |
| Debate | controversy / quote / counter-claim queries | Disagreement surface |
| Audience | keyword/List queries + roster verification | Personal-network view |

Use advanced operators from `references/query-patterns.md`. Always keep the
primary entity in the query. Drop off-entity viral noise.

Always run the normal global lanes. They preserve the event baseline and keep
quiet accounts discoverable through broad-result intersection.

When a personal audience is active, run at least one Latest lane without
`min_faves`, `filter:has_engagement`, or another engagement floor. Floors may
still be useful on the other global lanes, but they must not remove the only path
where quiet roster accounts can surface.

For Following:

- Intersect authors from every global keyword and semantic result with the full
  Following handle set.
- Add targeted `from:` searches for a few topic-relevant roster accounts when
  useful. Do not present that targeted subset as the full audience.

For an X List:

- Try an in-window `list:{id}` entity query if the host supports it.
- Intersect all other result authors with the member roster.
- Use cached List timeline post IDs to find candidates the global lanes missed,
  then re-fetch those posts through X tools.

Apply behavior after collection:

- **prefer:** rank roster-verified posts ahead of global posts. Keep relevant
  global context and label the difference when it changes the read.
- **strict:** only roster-verified authors contribute to the audience opinion
  map, rough shares, debates, and receipts. Non-roster origin or official posts
  may still be cited and quoted in **What happened** for event facts, but they do
  not count as audience opinion.

### Step 6 - Thread enrichment

`x_thread_fetch` the **3–8** highest-signal posts, prioritizing:

1. Origin / announcement
2. Official first-party
3. Highest-engagement summary take
4. Strongest steelman and strongest criticism
5. Posts that define a camp split
6. High-signal roster voices that would otherwise be represented only by an
   isolated search result

### Step 7 - Rank and cluster (in head, lightweight)

Rough score:

```text
score = engagement × freshness_weight × authority_weight × on_entity
```

- **On-entity:** must clearly be about the primary topic (or hard alias).
- **Authority (soft):** official accounts, domain experts, primary reporters -
  never a hard allowlist; do not over-weight bluechecks alone.
- **Audience:** in prefer mode, give verified roster authors a ranking boost. In
  strict mode, exclude non-roster authors from opinion synthesis.
- **Clusters:** merge posts that make the same claim into one camp bullet.

Discard engagement bait that fails entity grounding.

### Step 8 - Synthesize

Emit the brief using the template below. Do not dump raw ranked lists.
Include **at least 2–3 short attributed quotes** from real posts when the
sample has usable text.

If the sample is thin, say so. Prefer honest uncertainty over fake consensus.

## Output template

Use this structure. Keep headings. No extra blog-style sections.

```markdown
# /whathappened: {topic}

**Window:** {human window} · mode {Breaking|Same-day|Story|Background} · as of {UTC or local stamp}
**X sample:** ~{N} posts · Top + Latest + {K} threads · confidence {high|medium|thin}
**Audience:** {Global X | Following · prefer|strict · N accounts | List label/id · prefer|strict · N members}
**Audience coverage:** {global | sampled · N matching posts from M roster authors}
**Entity resolve:** {none | one web lookup: one-line what it was for}

## What happened
2–5 sentences. Prefer first-party and origin posts. Stick to what X supports.

## Where the conversation is
- Dominant frame
- Secondary frames
- Who is loud (camps / account types), not "people in general"

## Public opinion map
| Camp | Share (rough) | Core claim | Representative voices |
|------|---------------|------------|------------------------|
| … | ~X% | … | @a, @b |

Label shares as qualitative judgment from this sample, not polling.
For personal scopes, calculate rough shares only from roster-verified posts.

## The live debates
1. **{title}** - Side A vs Side B; stakes in one line; best evidence posts
2. …

## Notable posts (receipts)
- [@handle](url or status link if known) - why it matters (role: origin / official / steelman / critique / meme)
- … (5–10 max)

## Gaps / caveats
- Thin sample, audience sampling limits, incomplete List roster, missing official
  voice, language bias, bot/noise risk, web resolve used, etc.
- What would change this read if true
```

### Formatting notes

- Use plain hyphens `-`, not em dashes.
- Rename `Public opinion map` to `Audience opinion map` for a personal scope.
- Neutral wording: "many posts claim", "a common critique is", not "everyone knows".
- Rough camp percentages must be marked as rough sample judgment.
- If confidence is thin, shrink the opinion map and expand Gaps.
- End after Gaps. No trailing invitation spam unless the user asked follow-ups.

## Pre-flight checklist (before first tool call)

- [ ] Topic present (else ask)
- [ ] X tools available (else refuse)
- [ ] Audience parsed: global, Following, or one List
- [ ] Personal audience has terminal + `ft` and a usable roster
- [ ] Strict List, if requested, has `stats.snapshotComplete: true`
- [ ] Web budget remaining: 0 or 1 resolve-only
- [ ] No discovery request

## Post-synthesis checklist (before send)

- [ ] Window + mode stated
- [ ] Every quoted line attributable to a fetched post
- [ ] No web-derived "sentiment"
- [ ] Camps grounded in multiple posts when confidence is high
- [ ] Personal-audience posts mechanically verified against the full roster
- [ ] Strict mode excludes global voices from audience opinion and receipts
- [ ] All personal-audience coverage labeled sampled
- [ ] Handle-renaming risk noted in Gaps when the roster is not freshly synced
- [ ] Temporary Following roster file deleted
- [ ] Receipts are real and on-entity
- [ ] Gaps honest about sample limits
