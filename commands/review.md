---
description: Spaced repetition review — practice knowledge graph nodes due today
argument-hint: [optional: topic name]
allowed-tools: Bash, mcp__knowledge-graph__read_graph, mcp__knowledge-graph__advance_review, mcp__knowledge-graph__save_graph
---

## Context

**Requested topic**: $ARGUMENTS

**Active topic** (first word if it matches a known topic, otherwise "claude-code"):
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ -n "$FIRST" ] && { [ -f "$HOME/.claude/ramp/schemas/$FIRST.md" ] || [ -f ".claude/knowledge-graphs/schemas/$FIRST.md" ]; }; then echo "$FIRST"; else echo "claude-code"; fi`

**Today's date**: !`date +%Y-%m-%d`

**Due nodes** (kernel-computed SR queue for the active topic — the same rule as every due count ramp shows):
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ -n "$FIRST" ] && { [ -f "$HOME/.claude/ramp/schemas/$FIRST.md" ] || [ -f ".claude/knowledge-graphs/schemas/$FIRST.md" ]; }; then TOPIC="$FIRST"; else TOPIC="claude-code"; fi; python3 "$CLAUDE_PLUGIN_ROOT/ramp_core.py" due "$TOPIC" 2>/dev/null || echo "DUE_UNAVAILABLE"`

**First-run signal** (zero started topics ⇒ redirect a newcomer):
!`python3 "$CLAUDE_PLUGIN_ROOT/ramp_core.py" catalog 2>/dev/null | python3 -c "import sys,json; c=json.load(sys.stdin); print('FIRST_RUN' if not any(t['started'] for t in c) else 'HAS_GRAPHS')" 2>/dev/null || echo "HAS_GRAPHS"`

**Knowledge graph contents** (for active topic):
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ -n "$FIRST" ] && { [ -f "$HOME/.claude/ramp/schemas/$FIRST.md" ] || [ -f ".claude/knowledge-graphs/schemas/$FIRST.md" ]; }; then TOPIC="$FIRST"; else TOPIC="claude-code"; fi; cat ~/.claude/ramp/graphs/$TOPIC.md 2>/dev/null || echo "NO_TREE_FILE:$TOPIC"`

**All topics — due counts** (which other topics have due nodes):
!`python3 "$CLAUDE_PLUGIN_ROOT/ramp_core.py" catalog 2>/dev/null | python3 -c "import sys,json; rows=[f\"{t['name']}: {t['summary']['due']} due\" for t in json.load(sys.stdin) if t.get('started') and t.get('summary') and t['summary']['due']>0]; print('\n'.join(rows) if rows else 'none')" 2>/dev/null || echo "none"`

---

## Your role

**Empty-state redirect (check first):** If the **First-run signal** (auto-collected context) is `FIRST_RUN` — no graphs exist yet — do not render an empty review. This takes precedence over the `NO_TREE_FILE` / "nothing due" handling below; short-circuit and say:
> Nothing to review yet — you haven't started a topic. Run `/ramp:help` to get oriented, or `/ramp:up <topic>` to begin. See all topics with `/ramp:list`.

Then stop.

You are running a focused spaced repetition review session. No full assessment, no tree rendering, no questions about new skills. Only review nodes that are due.

**Interval ladder:**
- L1 = 1 day · L2 = 3 days · L3 = 7 days · L4 = 21 days · L5 = 60 days · L6 = permanent (no further review)

---

## Step 1: Find due nodes

The **Due nodes** context above is the primary SR queue — kernel-computed (valid `next:` date
≤ today; a malformed or absent date is never queued). Do not re-derive it by scanning the raw
graph.

1. Primary queue = the Due nodes JSON array, in its order. The due count = its length.
2. Count all `[~]` nodes in the **Knowledge graph contents** — the secondary verification queue.

If Due nodes is `DUE_UNAVAILABLE` (kernel CLI missing): fall back to scanning the graph for
`[✓]` nodes with `next:` ≤ today and say the count is best-effort.

If `NO_TREE_FILE:[topic]`: say "No knowledge graph found for **[topic]**. Run `/ramp:up [topic]` to create one." Stop.

If no `[✓]` nodes due AND no `[~]` nodes: say "Nothing due and no claimed skills to verify for **[topic]**." Show the earliest upcoming review date. Check the "All topics" list above and mention if other topics have due nodes.

If no `[✓]` nodes due BUT `[~]` nodes exist: skip the "nothing due" message. Go directly to Step 2b.

If `[✓]` due nodes exist: say "**[N] node(s) due for review in [topic]**." Proceed with Step 2a, then offer Step 2b afterward.

---

## Step 2a: SR pass — review due `[✓]` nodes

For each due `[✓]` node, one at a time:

**Present the node:**
```
Reviewing: [Node name]
What mastery looks like: [the mastery criterion — one sentence, specific]
```

Ask exactly one question targeting the criterion. Use this format based on the node type:
- Artifact nodes: "Can you describe the specific [file/config/pattern] you built for this? One concrete detail."
- Exercise nodes: "Walk me through the last time you did this. One specific thing that happened."
- Qualitative nodes: "Explain [specific aspect from criterion]. I'm looking for [the specific thing that distinguishes knowing from doing]."
- Historical nodes: "When did you last do this, and what specifically did you do?"

Wait for the user's answer. Apply the qualitative rubric, then record the outcome **in code** — do not compute the level or the date yourself:

- **Pass** — specific, verifiable detail. Call `mcp__knowledge-graph__advance_review(topic=[active-topic], node_name=[node name], outcome="pass")`. It advances the level, computes the next date, and recomputes XP. Report what it returns: "✓ Solid — [its result line]". A [✓]-node SR pass does **not** change XP (status is unchanged), so do not announce an XP gain — report the schedule advance only.
- **Fail** — vague or none. Call `advance_review(..., outcome="fail")` (resets to L1, next = tomorrow). Report: "× Let's revisit soon — [its result line]".

*Non-MCP fallback:* if the `knowledge-graph` MCP is not configured, run
`python3 "$CLAUDE_PLUGIN_ROOT/ramp_core.py" advance [topic] "[node name]" pass` (or `fail`) —
same math, same validated writer; report its result line exactly as above. If that exits 2,
report its output verbatim. If the kernel CLI is unavailable too, say the pass couldn't be
recorded and move on — never hand-edit the `| next:` field.

Move to the next due node.

---

## Step 2b: Teach-back verification — claimed `[~]` nodes

After the SR pass (or if no `[✓]` nodes were due), check if `[~]` nodes exist.

If `[~]` nodes exist, offer: "You have [N] claimed (unverified) skill(s). Want to verify one? A teaching-level answer earns `[✓]`."

If user agrees (or if there were no `[✓]` nodes due and `[~]` nodes exist):

- Pick the highest-priority `[~]` node: earliest branch first, in schema order; leftmost first within each branch.
- Present it:
  ```
  Verifying: [Node name]
  What mastery looks like: [the mastery criterion — one sentence]
  ```
- Ask one teach-back question: "Explain [X] as you'd teach it — include the *why*, a concrete scenario, and one edge case or tradeoff."
- Apply the teach-back rubric:
  - **Pass** — answer includes why, a scenario with context, and an edge/tradeoff: change the node line to `[✓|exercise] Node name — [repo], [today]: verified by teach-back in /ramp:review` (omit the `| next:` field — `save_graph` fills it). Then call `mcp__knowledge-graph__save_graph(topic=[active-topic], content=[full updated tree])`; it recomputes XP and fills the L1 review date. This `[~]→[✓]` upgrade **does** raise XP — report the new total from save_graph's confirmation. *(Non-MCP fallback: apply the same line change to the full tree — still omitting `| next:` — and persist via `python3 "$CLAUDE_PLUGIN_ROOT/ramp_core.py" save [active-topic]` with the tree on stdin; the writer fills the L1 date and recomputes XP.)*
  - **Fail** — vague or affirmation-only ("I've used it", "it does X"): stays `[~]`. Say "Let's revisit — it'll come up again."

Do **one** `[~]` verification per session. End after one regardless of outcome.

---

## Step 3: Persistence (handled by the tools)

Every outcome is written by code: `advance_review` (SR passes) and `save_graph` (teach-back
upgrades) via MCP when configured, or the kernel CLI verbs `advance` and `save` when not — XP
and review dates are always computed in code. Never hand-edit `xp:`, `| next:`, or a node's
status marker. MCP tools can be deferred (absent from the visible tool list until searched
for) — if the server is registered, load the tool rather than assuming no MCP. In the Step 4
close, say which path persisted this session's outcomes (MCP tools or kernel CLI verbs).

---

## Step 4: Close

Show a brief summary:
```
Reviewed [N] nodes. [N passed] passed, [N failed] reset. (SR passes advance the schedule; they do not change XP.)
[If teach-back ran] Verified: [node name] → [✓] (XP raised — new total from save_graph)   OR   Unverified: [node name] — try again after practicing it.
Next session: [earliest next: date across all nodes in this topic]
```

If `[~]` nodes remain unverified: "Run `/ramp:review` again to verify more claimed skills, or `/ramp:up` to demonstrate them in-session."

If other topics show due nodes (from the **All topics — due counts** context above), mention: "Also due today: [topic] ([N] due). Run `/ramp:review [topic]` when ready."

---

## Constraints

- One node at a time in both queues — do not show all nodes upfront
- Do not ask follow-up questions after the user answers — accept at face value and apply the rubric
- Do not explain the spaced repetition system unless asked
- Do not offer to practice new skills in this command — that's `/ramp:up`
- Teach-back verification: one `[~]` node per session, always offered after the SR pass
- Keep the whole session under 5 exchanges per node
