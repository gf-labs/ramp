---
description: End-of-session knowledge harvest — upgrade nodes, update SR schedule, optional snapshot
argument-hint: [optional: topic name]
allowed-tools: Bash, Read, Write, Edit, mcp__knowledge-graph__read_graph, mcp__knowledge-graph__save_graph
---

## Context

**Requested topic**: $ARGUMENTS

**Active topic**:
!`python3 "$CLAUDE_PLUGIN_ROOT/ramp_core.py" resolve -- "$ARGUMENTS" 2>/dev/null || echo "claude-code"`

**Today's date**: !`date +%Y-%m-%d`

**Knowledge graph** (active topic):
!`TOPIC=$(python3 "$CLAUDE_PLUGIN_ROOT/ramp_core.py" resolve -- "$ARGUMENTS" 2>/dev/null || echo "claude-code"); cat ~/.claude/ramp/graphs/$TOPIC.md 2>/dev/null || echo "NO_TREE_FILE:$TOPIC"`

**All available topics**:
!`ls ~/.claude/ramp/graphs/*.md 2>/dev/null | xargs -I{} basename {} .md | sort || echo "none"`

---

## Your role

You are the end-of-session knowledge harvester for ramp. Work through the steps below in order. Each step waits for the user's reply before proceeding. Do not skip steps unless the user says `skip`.

---

## Step 0 — Reflect

Scan the **current session's conversation** for evidence of demonstrated knowledge:
- Tool use patterns (Write, Edit, Bash, MCP calls, Agent launches)
- Exercises completed, configurations made, commands run
- Teaching-level explanations given (not just "I've used this")
- Artifacts created or modified

Produce a private working list of candidate nodes (do not show yet). Each entry:
```
[node name] | current status | proposed status | one-line evidence
```

If no demonstrable activity detected for any knowledge graph node: say "No node upgrades detected this session — nothing to harvest." Offer Step 3 (optional snapshot) anyway.

---

## Step 1 — Propose upgrades

Show the candidate list one topic group at a time:

```
Proposed upgrades for [topic] — [date]:

[ ] Node name → [✓|exercise] — [evidence note]
[~] Node name → [✓|exercise] — [evidence note]
...
```

Rules:
- Only propose `[ ]` → `[✓|exercise]` or `[~]` → `[✓|exercise]` (never downgrade)
- Evidence note must be specific: what was done, not just "used in session"
- `[✓]` nodes already demonstrated: skip unless SR interval should reset (rare)

Ask: "Confirm these upgrades? Reply `yes`, edit inline, or `skip`."

Wait for reply.

---

## Step 2 — Write updates

On confirmation, update `~/.claude/ramp/graphs/[topic].md`:

For each confirmed upgrade:
- Replace the node line status and append evidence trail:
  ```
  [✓|exercise] Node name — [repo/context], [today]: [evidence] in /ramp:wrap
  ```
- If node already had evidence, append with ` · ` separator (`save_graph` fills the `| next:` review field — don't hand-write a date)

Also update:
- `xp:` — do not recompute; `save_graph` recomputes it in code on write
- `updated: YYYY-MM-DD` frontmatter field to today

When the `knowledge-graph` MCP is configured, persist the upgraded tree by calling `save_graph(topic=[topic], content=[full updated tree])` — it recomputes XP, fills review dates on newly-`[✓]` nodes, and never downgrades an on-disk `[✓]`. Otherwise, persist the same full tree through the kernel CLI: `python3 "$CLAUDE_PLUGIN_ROOT/ramp_core.py" save [topic]` with the tree on stdin (heredoc); exit 2 means the writer REJECTED it — report the message verbatim and don't write. If neither is reachable, say so and stop — never Edit the graph file directly. Say which writer path ran. (MCP tools can be deferred — absent from the visible tool list until searched for; if the server is registered, load the tool rather than assuming no MCP.)

If `NO_TREE_FILE:[topic]`: say "No knowledge graph file found. Run `/ramp:up [topic]` to create one." Skip to Step 3.

---

## Step 3 — Snapshot

Draft 3–5 bullets covering only ramp-relevant context from this session:
- Which nodes were upgraded and why
- Any exercises or patterns that were demonstrated
- Topics or areas to revisit

Append directly to the project MEMORY.md. No confirmation needed.
Do NOT duplicate housekeeping context (git, plans, backlog) — that's session housekeeping, not knowledge capture.

---

## Wrap-up

Show a one-line summary:
```
## ramp:wrap — [date]
[topic]: [N] node(s) upgraded. XP: [old] → [new]. Next review: [earliest next: date].
[If no upgrades: "No upgrades this session."]
Snapshot: saved.
```

---

## Constraints

- Never downgrade a `[✓]` node
- Persist full-tree writes through `save_graph` or the kernel CLI `save` verb — never Edit the graph file directly
- Evidence must be specific — reject vague signals ("user seemed to understand X")
- One topic per session — if `$ARGUMENTS` is blank, default to `claude-code`
- Do not run housekeeping steps (git, plans, backlog) — this command harvests knowledge only
