---
description: List all ramp topics — what you could learn and where you've started
allowed-tools: Bash, Read
model: claude-haiku-4-5-20251001
---

## Context

**Topic catalog** (catalog ⟕ your progress, personal layer):
!`python3 "$CLAUDE_PLUGIN_ROOT/ramp_core.py" catalog 2>/dev/null || echo "CATALOG_UNAVAILABLE"`

---

## Your role

Render the topic catalog above as a grouped, read-only list. This is a viewer: **no writes, no questions, no inference.**

The catalog is a JSON array; each entry has: `name`, `description`, `node_count`, `group` (`core`/`sub`/`standalone`), `sources` (for `core`), `started` (bool), and `summary` (`{level, xp, due, counts}` when started, else null).

If the line is `CATALOG_UNAVAILABLE` or empty: the CLI shim could not run — either `$CLAUDE_PLUGIN_ROOT` isn't set (a manual-copy install without `ramp_core.py`) or `python3` **3.8+** isn't on the `PATH`. Say "Couldn't read the topic catalog — check that `python3` 3.8+ is installed. Run `/ramp:help` for orientation, or `/ramp:up <topic>` to start a topic." and stop.

**Layout:**

1. Header: `## ramp topics`
2. **Core** section — each `group: "core"` topic on one line:
   `[mark] [name padded]  [description]   [progress]`
   - `[mark]` = `✓` if `started`, else `·`
   - `[progress]` = if started: `[level] · [xp] XP · [due] due` (use `summary.level`, `summary.xp`, `summary.due`; show `· N due` only when due > 0); if not started: `[node_count] nodes · not started`
   - Under a core topic, add an indented line listing its `sources`:
     `    └ covers [sources joined by " · "]  (each also startable individually)`
3. **Standalone** section — each `group: "standalone"` topic, same one-line format. Do **not** print a separate flat list of `sub` topics — they are shown nested under their composite in step 2. (If a `sub` topic has its own started graph, it still appears nested; its progress is not double-counted.)
4. Footer, verbatim:
   `→ /ramp:up <topic> to start · /ramp:tree <topic> to view · /ramp:help if you're new`

Keep it tight — one screen. Preserve the catalog's ordering within each group.
