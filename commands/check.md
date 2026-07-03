---
description: Check back the active task — grade the worksheet, persist via save_graph, report the XP delta
argument-hint: [optional: what you did, e.g. "I added the hook to settings.json"]
allowed-tools: Read, Write, Bash, mcp__knowledge-graph__read_graph, mcp__knowledge-graph__save_graph
---

## Context

**Your note (optional)**: $ARGUMENTS

**Today's date**: !`date +%Y-%m-%d`

**Repo name** (for the evidence trail):
!`basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"`

**Active worksheet** (`./.ramp/worksheet.md`):
!`cat .ramp/worksheet.md 2>/dev/null || echo "NO_WORKSHEET"`

**Active topic** (from the worksheet's *Skill tree:* line, else claude-code):
!`TOPIC=$(sed -nE 's/^\*Skill tree: ([A-Za-z0-9_-]+).*/\1/p' .ramp/worksheet.md 2>/dev/null | head -1); echo "${TOPIC:-claude-code}"`

**Knowledge graph contents** (for the active topic — the tree the save applies to):
!`TOPIC=$(sed -nE 's/^\*Skill tree: ([A-Za-z0-9_-]+).*/\1/p' .ramp/worksheet.md 2>/dev/null | head -1); TOPIC="${TOPIC:-claude-code}"; cat "$HOME/.claude/ramp/graphs/$TOPIC.md" 2>/dev/null || echo "NO_TREE_FILE:$TOPIC"`

**Kernel CLI** (the no-MCP write path):
!`[ -n "$CLAUDE_PLUGIN_ROOT" ] && [ -f "$CLAUDE_PLUGIN_ROOT/ramp_core.py" ] && echo "KERNEL_OK" || echo "KERNEL_UNAVAILABLE"`

**Lesson registry** (`./.ramp/lessons.md`):
!`cat .ramp/lessons.md 2>/dev/null || echo "NO_LESSONS"`

---

## Your role

Check-back: grade the active task, persist the result through the validated writer, and **report the XP delta**. This file is the **canonical check-back protocol** — `up.md`'s natural-language **done** handler runs the same protocol inline; if you change one, change both.

A demonstration only counts when it reaches the graph **through the writer** (`save_graph` — never-downgrade, XP recomputed in code). Never record it by editing the graph file directly, and never just acknowledge in chat — persist, then report what changed.

## Step 1 — Locate the task

If the worksheet is `NO_WORKSHEET`: say "No active task — nothing to check. Run `/ramp:up` to get one." Stop.

From the worksheet, read the node title (the `# ` heading), the **Goal** (the mastery criterion), and the **Task**. If the graph is `NO_TREE_FILE` or contains no node line matching the title: say the worksheet doesn't match the saved graph (stale workspace) and suggest `/ramp:up` to regenerate it. Stop.

## Step 2 — Grade

Evidence, in priority order: work done in this session (files created, commands run — verify claims with Read/Bash where cheap), the worksheet's `>` answer block, the user's note above.

**Pass** requires at least one specific, verifiable detail tied to the criterion — a flag, a path, an observed behavior, a tradeoff navigated. "I did it" / "makes sense" is not evidence.

If your feedback corrects a factual claim, verify the fact first — against the node's **Reference** URL when fetchable, otherwise state only what you actually know. If the schema's criterion itself conflicts with the reference, trust the reference and flag the discrepancy in your report. Never teach an unverified correction — a confident wrong fact from the grader is worse than a miss.

- Demonstration type: `artifact` if a file/config now exists (check it), else `exercise`.
- **Not yet:** name the one concrete gap ("the criterion needs X; I saw Y"), leave the task active, write nothing. Stop.

## Step 3 — Persist through the writer

Build the **full updated tree**: take the graph contents above and change only the one node line —
`- [✓|<type>] <Node title> — <repo>, <today>: <specific evidence> via /ramp:check`
(append to an existing evidence trail with ` · `). Do **not** hand-write `| next:` (the writer fills L1 on newly-`[✓]` nodes) and do **not** touch `xp:` (recomputed in code).

- **MCP configured:** call `mcp__knowledge-graph__save_graph(topic=[active-topic], content=[full updated tree])`. MCP tools can be *deferred* — absent from your visible tool list until searched for — so don't conclude "no MCP" from the list alone: if the server is registered, load the tool and call it.
- **No MCP, `KERNEL_OK`:** run the CLI verb with the tree on stdin:

  ```bash
  python3 "$CLAUDE_PLUGIN_ROOT/ramp_core.py" save [active-topic] <<'RAMP_TREE'
  [the full updated tree]
  RAMP_TREE
  ```

  Exit 0 prints the same `saved · …` confirmation; exit 2 means the writer **REJECTED** the content — report its message verbatim and stop (do not fall back to editing the graph file).
- **Neither** (`KERNEL_UNAVAILABLE` and no MCP): ramp's validated writer isn't reachable on this install (manual copy without `ramp_core.py`). Say so and stop — do not simulate the save with Edits; XP and review dates must be computed in code.

## Step 4 — Report the delta

From the writer's confirmation (`saved · [topic] · [level] · [XP] XP → [path]`):

> **+[gained] XP** ([xp: from the graph frontmatter above] → [XP from the confirmation]) · **[node title]** is now `[✓]`
> Unlocked: [branch name] — only if this flip crossed an unlock threshold in the schema; omit otherwise
> Next review: tomorrow (L1) · Level: [level from the confirmation]

The XP numbers come from the graph frontmatter and the writer's confirmation — never from your own arithmetic. Name the writer path that ran (MCP tool or kernel CLI).

## Step 5 — Workspace bookkeeping

Per the `## The ./.ramp/ workspace` contract in `up.md`:

- `.ramp/lessons.md`: flip the task's row to `done` (append the row first, per the contract format, if the registry is missing it).
- `.ramp/current.md`: rewrite — inside a `/ramp:up` session the engine's done handler delivers the next task; standalone, write "No active task — run `/ramp:up` for the next one."
- Leave `worksheet.md` in place; the next task overwrites it.

## Constraints

- One check per invocation — the active worksheet task only
- Never downgrade a `[✓]`; never hand-edit `xp:` or `| next:` — the writer owns both
- Full-tree write through `save_graph` or the CLI `save` verb only; no Edit-tool writes to the graph, ever
- Evidence must be specific and verifiable — vague claims don't flip a node
- Report the delta from the writer's confirmation, not an estimate
