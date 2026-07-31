---
description: Display your knowledge graph — /ramp:tree, /ramp:tree [topic], or /ramp:tree all
argument-hint: [optional: topic name or "all"]
allowed-tools: Bash, mcp__knowledge-graph__read_graph, mcp__knowledge-graph__list_topics
model: claude-haiku-4-5-20251001
---

## Context

**Requested topic**: $ARGUMENTS

**Active topic** (the topic the arguments name — multi-word names resolve, e.g. "object oriented design"; "all", otherwise "claude-code"):
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ "$FIRST" = "all" ]; then echo "all"; else python3 "$CLAUDE_PLUGIN_ROOT/ramp_core.py" resolve -- "$ARGUMENTS" 2>/dev/null || echo "claude-code"; fi`

**Topic catalog** (levels, XP, due — for the summary line and the "all" list):
!`python3 "$CLAUDE_PLUGIN_ROOT/ramp_core.py" catalog 2>/dev/null || echo "CATALOG_UNAVAILABLE"`

**Structured nodes** (the data this view renders; empty array if the topic has no graph yet):
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ "$FIRST" = "all" ]; then echo "SEE_CATALOG"; else TOPIC=$(python3 "$CLAUDE_PLUGIN_ROOT/ramp_core.py" resolve -- "$ARGUMENTS" 2>/dev/null || echo "claude-code"); python3 "$CLAUDE_PLUGIN_ROOT/ramp_core.py" nodes "$TOPIC" 2>/dev/null || echo "NODES_UNAVAILABLE"; fi`

**Summary** (level/xp/due for the active topic):
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ "$FIRST" = "all" ]; then echo "{}"; else TOPIC=$(python3 "$CLAUDE_PLUGIN_ROOT/ramp_core.py" resolve -- "$ARGUMENTS" 2>/dev/null || echo "claude-code"); python3 "$CLAUDE_PLUGIN_ROOT/ramp_core.py" summary "$TOPIC" 2>/dev/null || echo "{}"; fi`

**Raw graph (fallback only — use if Structured nodes is `NODES_UNAVAILABLE`)**:
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ "$FIRST" = "all" ]; then for f in ~/.claude/ramp/graphs/*.md; do [ -f "$f" ] && echo "=== $(basename $f .md) ===" && cat "$f" && echo; done; else TOPIC=$(python3 "$CLAUDE_PLUGIN_ROOT/ramp_core.py" resolve -- "$ARGUMENTS" 2>/dev/null || echo "claude-code"); cat ~/.claude/ramp/graphs/$TOPIC.md 2>/dev/null || echo "NO_TREE_FILE:$TOPIC"; fi`

---

## Your role

Read-only viewer. No inference, no writes, no questions. Render the active topic's graph from the **Structured nodes** + **Summary** data; the raw graph is a fallback only.

**Data source rule:** If "Structured nodes" is a JSON array, render from it — it reproduces the graph faithfully. Each node has `name`, `status` (`done`/`reported`/`todo`/`locked`), `type`, `xp`, `branch`, `section`, `next_date`, `level`, `evidence`, `target`.

**Completeness is mandatory — render EVERY section and EVERY node in the array. Never merge, skip, condense, or drop a section or a node.** First scan the array for the distinct `section` values in the order they first appear, then emit exactly one `## ` heading for each, in that order, with that section's nodes listed beneath it — displaying only the section's **plain title** (the text after the closing `]`; the bracketed prefix is internal bookkeeping, never shown). **The number of `## ` headings you print MUST equal the number of distinct `section` values.** Never combine two sections under one heading even when their titles look related — e.g. `[Getting Started · ROOT] Core Foundations` and `[Getting Started · A] Working Effectively` are SEPARATE headings (`## Core Foundations`, `## Working Effectively`), each with its own nodes. (The `branch` letter alone is ambiguous — several sections share one, so always group and count by the full `section` string, never by `branch` and never by the displayed title.)

Render each node as exactly one line:
- **Marker:** `done`→`[✓]`, `reported`→`[~]`, `todo`→`[ ]`, `locked`→`[·]` — **but if `target` is `true`, render `[★]`** (a mastery-target frontier node). When a `done`/`reported` node has a non-null `type`, keep it in the marker: `[✓|<type>]`, `[~|<type>]`.
- then the node `name`;
- then, if `evidence` is non-null, ` — <evidence>`;
- then **only if `next_date` is non-null**, ` | next: <next_date> [L<level>]`. If `next_date` is null, append nothing — never print the literal word `null`, an empty date, or `[L??]`.

Open every tree render with the legend line: `*[✓] Demonstrated · [~] Self-reported · [ ] Not yet · [★] Mastery target · [·] Locked*`

If "Structured nodes" is `NODES_UNAVAILABLE`, fall back to printing the **Raw graph** contents cleanly.

**If `$ARGUMENTS` is empty or defaults to `claude-code`:**
1. From the **Topic catalog**, show a one-line summary list of started topics (name · level · XP · due).
2. Render the `claude-code` graph from Structured nodes, with a heading line from Summary: `claude-code — [level] · [xp] XP · [due] due`.
3. End with: "To show a different topic: `/ramp:tree [topic]`. To show all: `/ramp:tree all`. To browse every topic: `/ramp:list`."

**If `$ARGUMENTS` is a specific topic:**
1. Render that topic's graph from Structured nodes with the Summary heading line.
2. If the node array is empty (no graph yet), say: "No tree yet for **[topic]**. Run `/ramp:up [topic]` to create one."
3. End with: "To share: copy the contents of `~/.claude/ramp/graphs/[topic].md`"

**If `$ARGUMENTS` is `all`:**
1. From the **Raw graph** block (which already concatenates every started graph), show each tree separated by its topic header. (The `all` view is a dump of started graphs; per-topic structured rendering applies to single-topic views.)
2. End with: "To share a specific tree: copy the contents of `~/.claude/ramp/graphs/[topic].md`. To see topics you haven't started: `/ramp:list`."
