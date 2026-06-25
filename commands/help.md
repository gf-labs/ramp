---
description: What ramp is and how to use it — a 60-second orientation
allowed-tools: Bash, Read
model: claude-haiku-4-5-20251001
---

## Context

**Your state** (for the dynamic top line):
!`python3 "$CLAUDE_PLUGIN_ROOT/ramp_core.py" catalog 2>/dev/null | python3 -c "import sys,json; c=json.load(sys.stdin); started=[t for t in c if t['started']]; due=sum((t['summary'] or {}).get('due',0) for t in started); print(f'STARTED={len(started)} DUE={due}')" 2>/dev/null || echo "STARTED=0 DUE=0"`

---

## Your role

Render an orientation page. Read-only: **no writes, no questions.**

Parse the `STARTED=N DUE=M` line above and open with the matching **dynamic top line**:
- `STARTED=0` → `**You're new here.** Run `/ramp:list` to see topics, then `/ramp:up <topic>` to begin.`
- `DUE` > 0 → `**Welcome back — [DUE] node(s) due.** Run `/ramp:review` to keep them fresh.`
- `STARTED` > 0 and `DUE` = 0 → `**Pick up where you left off:** `/ramp:up <topic>`.`

Then render this evergreen body verbatim (fill nothing in — it is static):

```
## What ramp is

ramp maps what you can *do* with Claude Code — a knowledge graph grounded in your
real environment, not a checklist. It scores `[✓]` demonstrated over `[~]`
self-reported, and keeps skills alive with spaced repetition.

## Commands

**Start**
  /ramp:up <topic>    Assess, build your graph, and learn — the main command
  /ramp:list          See every topic and where you've started
  /ramp:help          This 60-second orientation

**Review & reference**
  /ramp:review        Run spaced-repetition review of what's due
  /ramp:tree <topic>  View a topic's full graph
  /ramp:cheatsheet    Your demonstrated skills + evidence trail

**Capture**
  /ramp:pin           Mid-session checkpoint
  /ramp:wrap          End-of-session knowledge harvest

**Extend**
  /ramp:ingest        Generate a topic schema from a PDF, URL, or file
```

End with a single **Your next step** line that expands the dynamic signal into one concrete command:
- new → `**Your next step:** `/ramp:list``
- due → `**Your next step:** `/ramp:review``
- started, none due → `**Your next step:** `/ramp:up <topic>``
