# Failure modes for /whathappened

Recognize these early. Prefer shrinking claims over stretching a bad sample.

## 1. No topic / discovery request

**Symptoms:** "what's hot", "trending on X", empty `/whathappened`.

**Do:** Ask for a topic. Do not run a global X firehose brief (v1 has no discovery).

## 2. Missing X tools

**Symptoms:** Only web/search tools available.

**Do:** Refuse the skill path. Explain Grok Build X tools are required. Do not
produce a fake X opinion map from Google.

## 3. Entity collision

**Symptoms:** Results mix two products, two people, or a common English word.

**Do:** Tighten to `"Exact Phrase"`, official `from:`, and aliases from the single
web resolve. Discard off-entity high-engagement posts even if viral.

## 4. Thin sample

**Symptoms:** Few unique authors, mostly retweets, or only one thread.

**Do:** Confidence `thin`. Shorten opinion map. Expand Gaps. Optionally widen
window one step. Never invent camps to fill the table.

## 5. Bot / engagement farm noise

**Symptoms:** Near-identical text, brand-new accounts, engagement without replies,
hashtag spam.

**Do:** Prefer posts with real reply chains; use thread fetch on human-looking
hubs; raise engagement floors carefully; note bot risk in Gaps.

## 6. Official silence

**Symptoms:** Lots of secondary takes, no `from:official` in window.

**Do:** Say so in What happened / Gaps. Do not treat rumor volume as confirmation.

## 7. Origin post outside short window

**Symptoms:** Everyone replies to or quotes a post older than your Breaking window.

**Do:** Fetch that origin thread even if older. Mention that the conversation is
fresh but the trigger is older.

## 8. Web leakage into sentiment

**Symptoms:** Temptation to cite articles, Reddit, or blogs for "what people think."

**Do:** Stop. Web is resolve-only (max one call). Sentiment stays X-only.

## 9. Over-long window on a fresh launch

**Symptoms:** Same-day launch but you searched 30 days and mixed prior product talk.

**Do:** Re-pulse. Commit Same-day or Breaking. Prior product discourse goes to
Gaps or a single "prior context" sentence, not the main opinion map.

## 10. Quote fabrication

**Symptoms:** Paraphrase that looks like a quote; reconstructed status URLs.

**Do:** Only quote text returned by tools. Only link URLs/IDs the tools provided.
If you lack a URL, cite `@handle` and paraphrase without a fake link.

## 11. Single-camp tunnel vision

**Symptoms:** Top lane is pure hype or pure hate.

**Do:** Force a debate lane and Latest lane. If the other side truly is absent,
say the sample is one-sided rather than inventing balance.

## 12. Percentages as false precision

**Symptoms:** "67.3% bullish" from 12 posts.

**Do:** Rough buckets only (`~half`, `~1/3`, or coarse percents) with explicit
"qualitative from this sample" language.

## 13. Field Theory unavailable or Following incomplete

**Symptoms:** `ft` is missing, `ft experts list` is unknown, or the command
refuses an incomplete Following snapshot.

**Do:** Stop the personal-audience path. Do not label global results Following.
Tell the user to update Field Theory or finish `ft sync-following`, and offer the
same topic with Global X instead.

## 14. Unknown or ambiguous List

**Symptoms:** The user says "my AI list" but no local alias resolves to one List,
or several IDs could match.

**Do:** Ask for the `x.com/i/lists/{id}` URL or numeric ID. Do not guess from
timeline content or account names.

## 15. Incomplete List requested in strict mode

**Symptoms:** The List-member digest is missing `stats.snapshotComplete: true`,
has a saved cursor, or otherwise reports a partial crawl.

**Do:** Refuse strict mode. Offer prefer mode with sampled coverage. Never promote
the partial member set to an authoritative allowlist.

## 16. Thin personal-audience intersection

**Symptoms:** Global X is active but only a few roster authors match, or all
matches come from one author.

**Do:** Widen one time step and try the allowed targeted audience searches. If
the sample stays thin, say that the user's network is quiet on the topic. Do not
fill an audience opinion map with global voices.

## 17. Followers or mutuals requested

**Symptoms:** The user asks for followers, mutuals, or "people who follow me."

**Do:** Say those rosters are not supported. Offer accounts they follow or one X
List. Do not approximate mutuals from engagement or replies.

## 18. Stale handle in a personal roster

**Symptoms:** A roster handle was renamed, a search result uses a newer handle,
or an old handle now belongs to another user.

**Do:** Treat handle membership as uncertain and say so in Gaps. Prefer a fresh
roster sync. Never infer identity continuity from display name or bio similarity.
