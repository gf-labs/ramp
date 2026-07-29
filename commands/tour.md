---
description: A guided walk through ramp's loop — list, up, tree, pin, review in one pass
allowed-tools: Bash, Read
model: claude-haiku-4-5-20251001
---

## Context

**Your state** (for the dynamic open + next-step lines):
!`python3 "$CLAUDE_PLUGIN_ROOT/ramp_core.py" catalog 2>/dev/null | python3 -c "import sys,json; c=json.load(sys.stdin); started=[t for t in c if t['started']]; due=sum((t['summary'] or {}).get('due',0) for t in started); print(f'STARTED={len(started)} DUE={due}')" 2>/dev/null || echo "STARTED=ERR DUE=0"`

---

## Your role

Render a guided tour of ramp's loop. Read-only: **no writes, no questions, no waiting.** This is a single-pass walkthrough with "try it" beats — the user runs the commands themselves.

**Do not run `/ramp:up`, assessments, or any graph write yourself.** The tour *points at* the commands; it never performs them. (`/ramp:up` scans the project; the tour only walks the commands. Keeping that line is what makes the tour lightweight and distinct from `up`.)

Parse the `STARTED=N DUE=M` line above and open with the matching **dynamic top line**:
- `STARTED=ERR` → `_Couldn't run ramp's Python helper — check that `python3` **3.8+** is on your `PATH`. The tour still works; the commands below are the point._`
- `STARTED=0` → `**New to ramp? This tour is for you.** Here's the whole loop in one pass — read it, then run the steps yourself.`
- `DUE` > 0 → `**Welcome back — [DUE] node(s) due.** Here's the loop as a refresher; when you're done, `/ramp:review` is your real next move.`
- `STARTED` > 0 and `DUE` = 0 → `**You already know the basics — here's the loop end to end.** Skim and pick up wherever you left off.`

Then render this evergreen body verbatim (fill nothing in — it is static):

```
## Why a graph at all

ramp maps what you can DO with Claude Code — grounded in your real
environment, not a checklist. It turns on one distinction:

  [✓] demonstrated   — there's evidence: a file you wrote, an exercise you passed
  [~] self-reported  — you said so, but nothing proves it yet

Only evidence earns a [✓]. That's what makes the map worth trusting — and
worth using to decide what to learn next.

## The loop — five moves

1. SEE WHAT'S ON OFFER          /ramp:list
   The catalog of topics and where you've started. claude-code is the default.
   -> Try it:  /ramp:list

2. BUILD YOUR MAP               /ramp:up claude-code
   The engine. It scans your environment, asks 2-3 things it can't detect,
   then renders your personalized graph + your frontier (what to learn next),
   and stays on as your co-pilot. This is the one that does the real work.
   -> Try it:  /ramp:up claude-code

3. LOOK AT YOUR MAP             /ramp:tree claude-code
   A read-only view — branches, statuses, frontier, level. Changes nothing.
   -> Try it:  /ramp:tree claude-code

4. DO REAL WORK — captured two ways
   Your map fills in from work you actually do, not a quiz:
     - Always-on: a passive observer flips specific artifacts to [✓] the
       moment you save them — write a slash command or add a hook, and the
       node updates in the background. No command needed.
     - On checkpoint: for everything else (a thoughtful CLAUDE.md, a tradeoff
       you navigated), run /ramp:pin and ramp reads the session and captures it.
   -> Try it:  build something small, then run /ramp:pin and re-check /ramp:tree

5. KEEP IT HONEST               /ramp:review
   [✓] nodes carry a spaced-repetition schedule (1d -> 3d -> 7d -> 21d -> 60d).
   /ramp:review walks what's due, one question each. Pass to advance, miss to reset.
   -> Try it (when nodes are due):  /ramp:review

That's the loop:   list -> up -> tree -> work + pin -> review

## Two more, when you want them

  /ramp:cheatsheet   a personal reference built from your own evidence trails
  /ramp:wrap         end-of-session harvest (like pin, run at the end)

## Prefer another format?

  Reading before you install, or sharing a link?   ->  GETTING-STARTED.md
  Just the 60-second command card?                 ->  /ramp:help
```

End with a single **Your next step** line that expands the dynamic signal into one concrete command:
- error → `**Your next step:** get `python3` **3.8+** on your `PATH`, then `/ramp:up claude-code`.`
- new (`STARTED=0`) → `**Your next step:** `/ramp:up claude-code` — build your first map.`
- due (`DUE` > 0) → `**Your next step:** `/ramp:review` — clear what's due.`
- started, none due → `**Your next step:** `/ramp:up <topic>` on something you're working on.`
