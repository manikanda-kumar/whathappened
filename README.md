<h1 align="center">/whathappened</h1>

<p align="center">
  <a href="https://docs.x.ai/build/overview"
    ><img
      alt="Grok Build only"
      src="https://img.shields.io/badge/Grok%20Build-only-black?style=flat-square"
  /></a>
  <a href="https://agentskills.io"
    ><img
      alt="Agent Skills"
      src="https://img.shields.io/badge/Agent%20Skills-package-blue?style=flat-square"
  /></a>
  <a href="LICENSE"
    ><img
      alt="License"
      src="https://img.shields.io/badge/license-MIT-green?style=flat-square"
  /></a>
  <a href="https://x.com/kunchenguid"
    ><img
      alt="X"
      src="https://img.shields.io/badge/X-@kunchenguid-black?style=flat-square"
  /></a>
  <a href="https://discord.gg/Wsy2NpnZDu"
    ><img
      alt="Discord"
      src="https://img.shields.io/discord/1439901831038763092?style=flat-square&label=discord"
  /></a>
</p>

<h3 align="center">What just happened on X - and what is the room actually saying?</h3>

<p align="center"><strong>Grok Build only.</strong> This skill needs Grok’s native X tools. Other agents can install the package; they cannot run it for real.</p>

Something drops. A model ships. A founder posts. A product melts down.

You open X and get dunks, screenshots, quote-tweet chains, and three conflicting "official" takes - none of them in one place.

**whathappened** is a [Grok Build](https://docs.x.ai/build/overview) [Agent Skill](https://agentskills.io) that turns that firehose into a short neutral briefing: what happened, where the conversation is, the opinion map, the live debates, and the receipts.

- **X-first** - public conversation from X, not a blog roundup. One optional web lookup only to resolve *who/what* the topic is.
- **Adaptive window** - breaking stories use minutes or hours; quieter ones widen only when the story is incomplete. Freshness wins by default.
- **Opinion map + debates** - camps, rough sample shares, steelman vs critique, with real post links - not a vibes paragraph.
- **Your network when asked** - prefer or strictly filter to accounts you follow, or prefer a saved X List, using a local Field Theory roster.
- **Dual output** - chat markdown brief **and** a self-contained HTML report under sibling `../whathappened-reports/` on every full run (opt out with `markdown only`).

## Quick Start

```sh
# install into Grok Build (global recommended)
$ npx skills add kunchenguid/whathappened -g
# or: copy skills/whathappened → ~/.grok/skills/whathappened

# in Grok Build
/whathappened Kimi K3
/whathappened Kimi K3 from people I follow
/whathappened Kimi K3 only from people I follow
/whathappened Kimi K3 from https://x.com/i/lists/1979812953135497678
```

Global X remains the default. Personal audience requests use local Field Theory
data only to verify membership and find candidates. Grok still fetches every
quoted post and receipt through its native X tools.

### Personal audience setup

Following requires a complete local snapshot:

```sh
ft sync-following
ft experts list --json --limit 2
```

X List prefer mode requires a saved member roster and may also use a cached List
timeline:

```sh
ft x-list-members https://x.com/i/lists/1979812953135497678
ft x-list https://x.com/i/lists/1979812953135497678 --since-hours 24
```

Supported personal scopes:

| Request | Behavior |
| ------- | -------- |
| "from people I follow" | Prefer followed accounts while retaining global context |
| "only people I follow" | Strict Following opinion map and receipts |
| "from this List" | Prefer roster-verified List members |
| "only from this List" | Strict only when Field Theory writes `stats.snapshotComplete: true` |

Personal-audience results are sampled, not exhaustive. Followers and mutuals are
not supported. A List name without a local alias needs its URL or numeric ID.

Example output from a real run on launch day (edited only for README length; structure is what the skill produces):

```markdown
# /whathappened: Kimi K3

**Window:** last ~24h · mode Same-day · as of 2026-07-16 ~22:30 UTC
**X sample:** ~60+ posts · Top + Latest + Semantic + first-party · 4 threads · confidence high (event) / medium-high (opinion; day-0)
**Entity resolve:** none (X user search → official @Kimi_Moonshot)

## What happened

Moonshot’s Kimi account launched Kimi K3 today as “Open Frontier Intelligence”: a 2.8T-parameter, 1M-context, native multimodal model for long-horizon agentic coding, live on Kimi product surfaces and API, with full weights promised by July 27, 2026.

The official thread also stresses architecture (Kimi Delta Attention, Attention Residuals, sparse MoE) and demos (kernel optimization, vision-in-the-loop game/UI work).

Independent and community scoreboards moved quickly: Arena Frontend Code Arena #1 (over Claude Fable 5), Text Arena roughly top-10, and Artificial Analysis Intelligence Index ~57 (near Opus 4.8 / GPT-5.5, behind Fable 5 and GPT-5.6 Sol).

## Where the conversation is

- Dominant frame: open weights (or soon-to-be) at near-frontier quality, especially coding/frontend - often cast as a milestone for open models.
- Secondary frames: API price/latency vs closed flagships; China vs US competitive pressure; policy/safety backlash expected next.
- Who is loud: Moonshot first-party; eval accounts (Arena, Artificial Analysis); coding-agent vendors (e.g. Cline); AI Twitter builders; a thinner but clear skeptic lane on cost/speed/real-work gaps.

## Public opinion map

Shares are rough qualitative judgment from this X sample, not polling.

| Camp | Share (rough) | Core claim | Representative voices |
|------|---------------|------------|------------------------|
| Open-frontier bulls | ~50% | Near Fable/Sol on many axes; #1 frontend; open weights change the game | @cline, @arena, @TheAhmadOsman |
| Nuanced practitioners | ~25% | Very strong (esp. frontend), not undefeated overall; slow / thinks hard / API not “cheap open” | @goodworse, @DimitriGilbert, @runzhuotao, @jaminball |
| Geopolitics / policy | ~15% | “Sputnik” for the US; fear of open-model bans; cycle of China/safety rhetoric | @MTSlive (quoting Amp CEO), @Dan_Jeffries1, @haider1 |
| Maximal hype | ~10% | AGI-adjacent language, “mogs everything” | e.g. @dedene |

## The live debates

1. **Is it frontier, or “almost frontier”?**
   Side A: same ballpark as GPT-5.6 / Fable 5, #1 frontend. Side B: AA puts it behind Fable/Sol overall; some real-workload tests put it nearer Opus 4.8 / GPT-5.5.

2. **Cheap open win vs expensive reasoning tax**
   Side A: $3/$15 per MTok framed as Sonnet-like value. Side B: “thinks a lot → costs a lot,” slower than hoped, pricier than prior Kimi models.

3. **Competition catalyst vs regulatory panic**
   Side A: healthy race, progress accelerates. Side B: expect essays, China-hawk policy, open-weight restrictions.

4. **“Open” today vs weights on July 27**
   API/product is live; weights are scheduled, not yet downloadable.

## Notable posts (receipts)

- @Kimi_Moonshot - origin: official launch specs + July 27 weights
- @arena - scoreboard: Frontend Code Arena #1 over Fable 5
- @ArtificialAnlys - independent eval: AA ~57; agentic gains; cost/task framing
- @cline - builder frame: largest open-weight class model, near Fable/GPT-5.6, Sonnet-like API price
- @synthwavedd - receipt: “drops at 57 on Artificial Analysis, just behind Fable and Sol”
- @goodworse - steelman critique: frontend strength vs real-world closer to Opus 4.8/GPT-5.5; slow; pricier than K2.7
- @DimitriGilbert - hands-on: “really good… only downside, it thinks a LOT… and therefore costs a LOT”
- @theo - ecosystem: practical “which harness?” question, not pure scoreboard talk

## Gaps / caveats

- Day-0 recency bias: likes and quotes still forming; Top lane is announcement-heavy.
- Weights not out yet: open-weight celebration is partly forward-looking (July 27).
- English/AI-Twitter skew; capacity/noise on Latest.
- What would change the read: multi-day coding failures, weights delayed, or closed labs shipping clear counters.
```

## Grok Build only

This skill is **not** a multi-harness research product. It depends on Grok Build’s native X stack:

- `x_keyword_search`
- `x_semantic_search`
- `x_thread_fetch`
- `x_user_search`

If those tools are missing, the skill should **refuse** rather than fake an X briefing from web search. Installing into Claude Code, Cursor, Codex, etc. will not give you a working run.

Personal audience filters also need the local `ft` command and terminal access.
The default global-X mode does not require Field Theory.

## Install

**Global (recommended)** for Grok:

```sh
npx skills add kunchenguid/whathappened -g
```

**Project-local:**

```sh
npx skills add kunchenguid/whathappened
```

**Direct into Grok’s user skills dir:**

```sh
git clone https://github.com/kunchenguid/whathappened.git
cp -R whathappened/skills/whathappened ~/.grok/skills/whathappened
# or: ln -s "$(pwd)/whathappened/skills/whathappened" ~/.grok/skills/whathappened
```

Grok also discovers skills under `.agents/skills/`, so a normal `npx skills add -g` install often lands where Grok can see it. Prefer `~/.grok/skills/` when you want the Grok-native path explicitly.

**List skills in this package without installing:**

```sh
npx skills add kunchenguid/whathappened --list
```

## How It Works

```
topic
  │
  ▼
┌─────────────────┐
│ optional web x1 │  resolve entity only (name / handle)
└────────┬────────┘
         ▼
┌─────────────────┐
│ pulse (Latest)  │  measure velocity → commit window mode
└────────┬────────┘
         ▼
┌─────────────────┐
│ search lattice  │  Top · Latest · Semantic · from: · debate
└────────┬────────┘
         ▼
┌─────────────────┐
│ audience verify │  optional Following / X List roster intersection
└────────┬────────┘
         ▼
┌─────────────────┐
│ thread fetch    │  origin · official · camps · steelman
└────────┬────────┘
         ▼
┌─────────────────┐
│ rank + cluster  │  engagement × freshness × on-entity
└────────┬────────┘
         ▼
      briefing
```

- **Modes:** Breaking (hours) → Same-day → Story (days) → Background (longer only if needed) - shortest window that still explains the story.
- **Soft web rule:** at most one lookup for identity. Sentiment stays X-only.
- **No discovery mode in v1:** you must name a topic (`/whathappened` alone asks for one).

## Usage

| Invoke | Example |
| ------ | ------- |
| Slash | `/whathappened Kimi K3` |
| Natural language | "what are people on X saying about the OpenAI board drama" |
| Following prefer | `/whathappened Kimi K3 from people I follow` |
| Following strict | `/whathappened Kimi K3 only from people I follow` |
| List prefer | `/whathappened Kimi K3 from https://x.com/i/lists/1979812953135497678` |

The agent should auto-invoke when the description matches (launch reaction, X/Twitter sentiment, "what happened with…").

## Package layout

```
skills/whathappened/
  SKILL.md                 # agent contract (pipeline + output template)
  references/
    query-patterns.md      # X advanced search recipes
    failure-modes.md       # thin sample, bots, entity collisions, …
    report-html.md         # standard HTML report layout (Global / Following / List)
```

HTML reports are **standard** on every full run. They live in a sibling folder
(not packaged inside the skill):

```
../whathappened-reports/whathappened-{slug}-{date}.html
```

Personal List/Following reports add Audience + Coverage mast pills and badge
roster vs global receipts — see `references/report-html.md`. Say `markdown only`
to skip the HTML file.

Ships as an [`npx skills`](https://github.com/vercel-labs/skills) package (`skills/<name>/SKILL.md`) for install convenience. Runtime target remains Grok Build only.

## Development

```sh
# edit the skill
$EDITOR skills/whathappened/SKILL.md

# smoke-test discovery locally
npx skills add ./ -l

# install from this checkout for Grok
npx skills add ./ -g -y
# or symlink into ~/.grok/skills/whathappened
```
