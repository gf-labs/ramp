# `/tools:wrap` — Reference for `/ramp:wrap` Implementation

This is the working implementation of `/tools:wrap` from the `claude-toolbox` project.
Use it as a structural template when building `/ramp:wrap`.

**Source:** `claude-toolbox/commands/wrap.md`
**Key difference:** `ramp:wrap` is knowledge-graph-focused (node upgrades, SR scheduling);
`tools:wrap` is housekeeping-focused (snapshot, git, plans, backlog, done marker).
Both are designed to run together: `/ramp:wrap` → `/tools:wrap`.

---

## Structural patterns to reuse

### Auto-collected context block
The command uses frontmatter-gated `!cmd` blocks to pre-load context before the prompt runs.
For ramp, you'll want to pre-load the relevant knowledge graph file(s) via MCP or Read.

### Interactive step-by-step flow
Each step waits for user reply before proceeding. Pattern:
```
## Step N — [name]
[do thing]
Ask: "[question]. Reply `yes`/`skip`."
Wait for reply.
```

### Scope utility
```python
sys.path.insert(0, os.environ.get('CLAUDE_TOOLBOX_ROOT', '') + '/scripts')
from _scope import get_scope
mode, data, cwd = get_scope()
```

---

## Full source: `commands/wrap.md`

```markdown
---
description: End-of-session housekeeping — snapshot, git check, plan cleanup, backlog review, done marker
allowed-tools: Bash, Read, Write, Edit
---

## Your role

You are the end-of-session close-out assistant. Work through the steps below in order.
Each step is interactive — wait for the user's reply before proceeding to the next.
Do not skip steps unless the user says `skip`.

---

## Step 0 — Ramp check

Ask: "Did you run `/ramp:wrap` first? Reply `yes` or `skip` (skip if ramp is not installed)."

Wait for reply, then proceed to Step 1 regardless of answer.

---

## Step 1 — Snapshot

Follow the full snapshot flow using the MEMORY.md PATH and content collected above:

1. Reflect on this session — what was discussed and done. Identify key decisions, patterns,
   file paths, and anything a future session needs. Discard ephemeral details.
2. Draft a dated snapshot section (5–15 bullets)
3. Show the draft. Ask: "Add this to MEMORY.md? Reply `yes` to save, or tell me what to change."
4. On confirmation: append to MEMORY.md using Edit tool.

Constraints:
- Append only — never overwrite existing content
- Do not include ramp knowledge-graph, XP, or level details (those belong in /ramp:wrap)

---

## Step 2 — Git check

If uncommitted changes: list + ask "address before closing? `done`/`skip`"
If unpushed commits: list + ask "push before closing? `done`/`skip`"

---

## Step 3 — Plan cleanup

List plans from `collect-plans.py`. Ask which completed ones to delete.
Delete named files from `~/.claude/plans/`.

---

## Step 4 — Backlog review

Show In Progress + Up Next. Ask which items completed this session.
Move to Done section or remove.

---

## Step 5 — Memory health

Warn if MEMORY.md ≥ 150 lines (truncation at 200).

---

## Step 6 — Done marker

Ask "Mark this session for deletion?" If yes, append `custom-title` JSON record to
the session's `.jsonl` file with `-delete-me` suffix.

---

## Wrap-up summary

```
## Session closed — [date]
Snapshot: saved | Git: clean | Plans: [N] | Backlog: [N] | Done: marked
```
```

---

## Suggested `/ramp:wrap` structure

```
## Step 0 — Reflect
Scan this session's tool calls, exercises, explanations.
List nodes that were actively demonstrated (Feynman-level, not just claimed).

## Step 1 — Propose upgrades
For each node: show `[ ]`/`[~]` → `[✓|exercise]` + one-line evidence note.
Ask for confirmation.

## Step 2 — Write updates
Write to `~/.claude/knowledge-graphs/[topic].md` via MCP save_graph or Write tool.
Reset SR schedule for newly confirmed nodes: `next: today+1d [L1]`.

## Step 3 — Optional MEMORY.md snapshot
Ask: "Add a ramp-focused snapshot to MEMORY.md? `yes`/`skip`"
If yes: draft 3–5 bullets covering ramp-relevant context only.

## Wrap-up
"Knowledge graph updated: [N] nodes upgraded. Next review: [date]."
```
