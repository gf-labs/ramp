---
description: Break checkpoint — status display, graph node save, optional MEMORY.md snapshot
argument-hint: [optional: topic name]
allowed-tools: Bash, Read, Write, Edit, mcp__knowledge-graph__read_graph, mcp__knowledge-graph__save_graph
---

## Context

**Requested topic**: $ARGUMENTS

**Active topic**:
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ -n "$FIRST" ] && { [ -f "$HOME/.claude/ramp/schemas/$FIRST.md" ] || [ -f ".claude/knowledge-graphs/schemas/$FIRST.md" ]; }; then echo "$FIRST"; else echo "claude-code"; fi`

**Today's date**: !`date +%Y-%m-%d`

**Knowledge graph** (active topic):
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ -n "$FIRST" ] && { [ -f "$HOME/.claude/ramp/schemas/$FIRST.md" ] || [ -f ".claude/knowledge-graphs/schemas/$FIRST.md" ]; }; then TOPIC="$FIRST"; else TOPIC="claude-code"; fi; cat ~/.claude/ramp/graphs/$TOPIC.md 2>/dev/null || echo "NO_TREE_FILE:$TOPIC"`

---

## Your role

Mid-session knowledge checkpoint for ramp. Work through the three steps below. Step 1 is display-only — proceed immediately. Steps 2 and 3 are interactive — wait for the user's reply before proceeding.

This command is a checkpoint, not a session close. After it completes, the session continues. Do not ask the user to run any session-close command or mark anything done.

---

## Step 1 — Status (display only)

Read the loaded graph and render immediately — no questions:

```
## Pin — [topic] — [date] · Level: [level] · [XP] XP

Review due: [N nodes with next: date ≤ today] or "No nodes due"
Last saved: [updated: date from frontmatter]
```

If `NO_TREE_FILE:[topic]`: say "No knowledge graph found for **[topic]**. Run `/ramp:up [topic]` to create one." Stop.

Proceed to Step 2 immediately.

---

## Step 2 — Node save

Scan the **current conversation** for evidence of demonstrated knowledge since the last save (check the `updated:` date from the graph as a reference point):
- Tool use patterns (Write, Edit, Bash, MCP calls, Agent launches)
- Exercises completed, configurations made, commands run
- Teaching-level explanations given (not just "I've used this")
- Artifacts created or modified

If no demonstrable activity detected: say "No new demonstrations detected." Skip to Step 3.

For each candidate node, show:
```
Proposed upgrades for [topic]:

[ ] Node name → [✓|exercise] — [evidence note]
[~] Node name → [✓|exercise] — [evidence note]
```

Rules:
- Only propose `[ ]` → `[✓|exercise]` or `[~]` → `[✓|exercise]` (never downgrade)
- Evidence note must be specific: what was done, not just "used in session"

Ask: "Save these upgrades? Reply `yes`, edit inline, or `skip`."

On `yes`: update `~/.claude/ramp/graphs/[topic].md`:
- Replace each node line status and append evidence trail:
  ```
  [✓|exercise] Node name — [repo/context], [today]: [evidence] in /ramp:pin
  ```
- If node already had evidence, append with ` · ` separator (`save_graph` fills the `| next:` review field — don't hand-write a date)
- `xp:` — do not recompute; `save_graph` recomputes it in code on write
- Update `updated: YYYY-MM-DD` to today

When the `knowledge-graph` MCP is configured, persist by reading the current tree (`read_graph`), applying your targeted node upgrade to the full content, then calling `save_graph(topic, content)` with the complete updated tree — it preserves every existing `[✓]` node (never-downgrade) and recomputes XP, so a full-file write is safe. If MCP is unavailable, persist the same full updated tree through the kernel CLI: `python3 "$CLAUDE_PLUGIN_ROOT/ramp_core.py" save [topic]` with the tree on stdin (heredoc); exit 2 means the writer REJECTED it — report the message verbatim and don't write. If neither is reachable, say so and stop — never Edit the graph file directly.

---

## Step 3 — Snapshot (optional)

Ask: "Capture ramp-specific context to MEMORY.md? `yes` / `skip`"

On `yes`: append 3–5 bullets to the project MEMORY.md covering only ramp-relevant context:
- Which nodes were upgraded and why
- Any exercises or patterns demonstrated
- Decisions about the knowledge graph itself

Do NOT include general session narrative (git, plans, backlog) — that's session housekeeping, not knowledge capture.

---

## Constraints

- Never downgrade a `[✓]` node
- Evidence must be specific — reject vague signals ("user seemed to understand X")
- One topic per session — if `$ARGUMENTS` is blank, default to `claude-code`
- Do not run housekeeping steps (git, plans, backlog) — this command captures knowledge only
- Do not mark anything as done or ask about session close
