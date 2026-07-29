# Getting started with ramp

*A 10-minute guided walk through ramp's loop. By the end you'll have a personalized, evidence-backed map of your Claude Code skills — and you'll know how to keep it honest.*

## What ramp is, in one idea

ramp maps what you can actually **do** with Claude Code — a knowledge graph grounded in your real environment, not a checklist you tick.

The whole thing turns on one distinction:

- **`[✓] demonstrated`** — there's *evidence*: a file you wrote, an exercise you did, an explanation you passed.
- **`[~] self-reported`** — you said you've done it, but nothing proves it yet.

Most learning tools let you mark yourself done. ramp only grants `[✓]` from evidence. So your map reflects the truth about your skills, not your self-image of them — which is exactly what makes it useful for deciding *what to learn next*.

## Before you start

- **Claude Code**, installed and run at least once.
- **`python3` 3.8+** on your `PATH`. ramp's local layer is stdlib-only — nothing to `pip install`.
- **No MCP server, no backend, no account.** Everything below runs on the local path.

## Install

```
/plugin marketplace add gf-labs/gfl-marketplace
/plugin install ramp@gfl-marketplace
```

That's the whole setup. A passive-observer hook and the topic schemas register automatically on your next session start.

## The loop — five moves

ramp is one engine (`/ramp:up`) plus a handful of commands that read, capture, and maintain your map. Here's the whole loop once, in order.

### 1. See what's on offer — `/ramp:list`

```
/ramp:list
```

The catalog: every topic you can ramp up on, and where you've already started. `claude-code` is the default — start there.

### 2. Build your map — `/ramp:up claude-code`

```
/ramp:up claude-code
```

This is the engine. It scans your environment — your Claude Code config, git history, session history, prior progress — and asks at most two or three questions about things it *can't* detect. Then it renders a personalized graph: what you've demonstrated, what you haven't, and your **frontier** — the two or three things to learn next.

It doesn't stop at a report. It hands you a first mastery mission grounded in your actual files, and stays engaged as your co-pilot for the rest of the session.

*Prefer a structured start? `/ramp:calibrate claude-code` writes a placement worksheet
you fill in on your own time; `/ramp:check` grades it and seeds your graph from your
claims. Same destination — a map that reflects you — different front door.*

### 3. Look at your map — `/ramp:tree claude-code`

```
/ramp:tree claude-code
```

A read-only view of your graph: branches, node statuses, your frontier, your level. Come back to it any time — it never changes anything.

### 4. Do real work — and watch it get captured two ways

Here's the part that makes the map honest: it fills in from work you actually do, not a quiz. ramp captures in **two layers**.

- **Always-on (automatic).** A passive observer runs on every tool call. The moment you write a slash command (`.claude/commands/*.md`), add a hook to `settings.json`, or create a subagent, it recognizes the artifact and flips that node to `[✓]` in the background — no command, no ceremony. Run `/ramp:tree` afterward and you'll find it already updated. (The observer started watching the moment step 2 created your graph.)
- **On checkpoint (reasoning).** Some things aren't a single-file signal — writing a thoughtful `CLAUDE.md`, navigating a tradeoff. Run **`/ramp:pin`** mid-session and ramp reads what actually happened this session and captures those too.

Together: a cheap layer that auto-catches specific artifacts as you work, plus a reasoning layer for everything else. Either way, `[✓]` is *earned by evidence*.

### 5. Keep it honest — `/ramp:review`

```
/ramp:review
```

Skills decay. Every `[✓]` node carries a spaced-repetition schedule (1d → 3d → 7d → 21d → 60d → permanent). `/ramp:review` walks the nodes due today, one question each — pass and the interval grows; miss and it resets. Your map stays true over time instead of going stale the day after you built it.

## That's the loop

`list → up → tree → work + pin → review`. Run `/ramp:up` whenever you start something new; let the observer and `/ramp:pin` keep the map current as you work; let `/ramp:review` keep it honest.

## Where to go next

- **Prefer to be walked through it inside a session?** Run **`/ramp:tour`** — the interactive twin of this guide, right in your terminal.
- **Just want the command reference?** `/ramp:help` (60-second card) or the [README command table](./README.md#the-commands).
