<h1 align="center">whathappened</h1>

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

## Quick Start

```sh
# install into Grok Build (global recommended)
$ npx skills add kunchenguid/whathappened -g
# or: copy skills/whathappened → ~/.grok/skills/whathappened

# in Grok Build
/whathappened Kimi K3
```

You get a structured brief: **What happened**, **Where the conversation is**, **Public opinion map**, **The live debates**, **Notable posts**, **Gaps**.

## Grok Build only

This skill is **not** a multi-harness research product. It depends on Grok Build’s native X stack:

- `x_keyword_search`
- `x_semantic_search`
- `x_thread_fetch`
- `x_user_search`

If those tools are missing, the skill should **refuse** rather than fake an X briefing from web search. Installing into Claude Code, Cursor, Codex, etc. will not give you a working run.

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

The agent should auto-invoke when the description matches (launch reaction, X/Twitter sentiment, "what happened with…").

## Package layout

```
skills/whathappened/
  SKILL.md                 # agent contract (pipeline + output template)
  references/
    query-patterns.md      # X advanced search recipes
    failure-modes.md       # thin sample, bots, entity collisions, …
```

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

## Notes

- Opinion percentages in the brief are **qualitative sample judgment**, not polling.
- Day-0 launches will skew toward announcement posts; Gaps should say so.
- Name stays `whathappened` for now. Better branding welcome later.
