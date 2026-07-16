<h1 align="center">whathappened</h1>

<p align="center">
  <a href="https://agentskills.io"
    ><img
      alt="Agent Skills"
      src="https://img.shields.io/badge/Agent%20Skills-compatible-blue?style=flat-square"
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

Something drops. A model ships. A founder posts. A product melts down.

You open X and get dunks, screenshots, quote-tweet chains, and three conflicting "official" takes - none of them in one place.

**whathappened** is an [Agent Skill](https://agentskills.io) that turns that firehose into a short neutral briefing: what happened, where the conversation is, the opinion map, the live debates, and the receipts.

- **X-first** - public conversation from X, not a blog roundup. One optional web lookup only to resolve *who/what* the topic is.
- **Adaptive window** - not stuck on "last 30 days." Breaking stories use hours; slower ones widen only as needed. Freshness wins by default.
- **Opinion map + debates** - camps, rough sample shares, steelman vs critique, with real post links - not a vibes paragraph.

## Quick Start

```sh
# recommended: install globally for your coding agents
$ npx skills add kunchenguid/whathappened -g

# then in a host with native X tools (Grok Build):
/whathappened Kimi K3
```

You get a structured brief: **What happened**, **Where the conversation is**, **Public opinion map**, **The live debates**, **Notable posts**, **Gaps**.

## Install

**Global (recommended)** - available across projects:

```sh
npx skills add kunchenguid/whathappened -g
```

**Project-local** - committed with a repo for the team:

```sh
npx skills add kunchenguid/whathappened
```

**Specific agents** (examples):

```sh
npx skills add kunchenguid/whathappened -g -a claude-code -a cursor -a codex
npx skills add kunchenguid/whathappened -g -a '*'   # all detected agents
```

**List skills in this package without installing:**

```sh
npx skills add kunchenguid/whathappened --list
```

**From source / Grok Build user skill path:**

```sh
git clone https://github.com/kunchenguid/whathappened.git
cp -R whathappened/skills/whathappened ~/.grok/skills/whathappened
# or: ln -s "$(pwd)/whathappened/skills/whathappened" ~/.grok/skills/whathappened
```

Grok Build also discovers skills under `.agents/skills/` and (optionally) Claude/Cursor skill dirs, so a normal `npx skills add -g` install is often enough.

## Host requirement

This skill is written for agents that can search X natively:

- `x_keyword_search`
- `x_semantic_search`
- `x_thread_fetch`
- `x_user_search`

**Grok Build** is the primary host. If those tools are missing, the skill should refuse rather than fake an X briefing from web search.

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
│ thread fetch    │  origin · official · camps · steelman
└────────┬────────┘
         ▼
┌─────────────────┐
│ rank + cluster  │  engagement × freshness × on-entity
└────────┬────────┘
         ▼
      briefing
```

- **Modes:** Breaking (hours) → Same-day → Story (days) → Background (up to ~30d) - shortest window that still explains the story.
- **Soft web rule:** at most one lookup for identity. Sentiment stays X-only.
- **No discovery mode in v1:** you must name a topic (`/whathappened` alone asks for one).

## Usage

| Invoke | Example |
| ------ | ------- |
| Slash | `/whathappened Kimi K3` |
| Natural language | "what are people on X saying about the OpenAI board drama" |

The agent should auto-invoke when the description matches (launch reaction, X/Twitter sentiment, "what happened with…").

## Package layout

```
skills/whathappened/
  SKILL.md                 # agent contract (pipeline + output template)
  references/
    query-patterns.md      # X advanced search recipes
    failure-modes.md       # thin sample, bots, entity collisions, …
```

Compatible with [`npx skills`](https://github.com/vercel-labs/skills) discovery (`skills/<name>/SKILL.md`).

## Development

```sh
# edit the skill
$EDITOR skills/whathappened/SKILL.md

# smoke-test discovery locally
npx skills add ./ -l

# install from this checkout into your agents
npx skills add ./ -g -y
```

## Notes

- Opinion percentages in the brief are **qualitative sample judgment**, not polling.
- Day-0 launches will skew toward announcement posts; Gaps should say so.
- Name stays `whathappened` for now. Better branding welcome later.
