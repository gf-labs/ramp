---
description: Spaced repetition review — practice knowledge graph nodes due today
argument-hint: [optional: topic name]
allowed-tools: Bash, Write, Edit, mcp__knowledge-graph__read_graph, mcp__knowledge-graph__advance_review, mcp__knowledge-graph__save_graph
---

## Context

**Requested topic**: $ARGUMENTS

**Active topic** (first word if it matches a known topic, otherwise "claude-code"):
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ -n "$FIRST" ] && { [ -f "$HOME/.claude/knowledge-graphs/schemas/$FIRST.md" ] || [ -f ".claude/knowledge-graphs/schemas/$FIRST.md" ]; }; then echo "$FIRST"; else echo "claude-code"; fi`

**Today's date**: !`date +%Y-%m-%d`

**Knowledge graph contents** (for active topic):
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ -n "$FIRST" ] && { [ -f "$HOME/.claude/knowledge-graphs/schemas/$FIRST.md" ] || [ -f ".claude/knowledge-graphs/schemas/$FIRST.md" ]; }; then TOPIC="$FIRST"; else TOPIC="claude-code"; fi; cat ~/.claude/knowledge-graphs/$TOPIC.md 2>/dev/null || echo "NO_TREE_FILE:$TOPIC"`

**All topics — earliest due dates** (to check if other topics have due nodes):
!`for f in ~/.claude/knowledge-graphs/*.md; do [ -f "$f" ] || continue; TOPIC=$(basename "$f" .md); EARLIEST=$(grep -oP "next: \K[0-9]{4}-[0-9]{2}-[0-9]{2}" "$f" 2>/dev/null | sort | head -1); [ -n "$EARLIEST" ] && echo "$TOPIC: next review $EARLIEST"; done 2>/dev/null || echo "none"`

---

## Your role

You are running a focused spaced repetition review session. No full assessment, no tree rendering, no questions about new skills. Only review nodes that are due.

**Interval ladder:**
- L1 = 1 day · L2 = 3 days · L3 = 7 days · L4 = 21 days · L5 = 60 days · L6 = permanent (no further review)

---

## Step 1: Find due nodes

Read the knowledge graph above.

1. Find all `[✓]` nodes where the `next: YYYY-MM-DD` date is **≤ today's date** — the primary SR queue.
2. Count all `[~]` nodes in the tree — the secondary verification queue.

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

*Non-MCP fallback (best effort):* if the `knowledge-graph` MCP is not configured, advance the level one rung (L1→L2→L3→L4→L5; L1=1d, L2=3d, L3=7d, L4=21d, L5=60d) and edit the node's `| next:` field with the Edit tool. This path is the documented degradation; the MCP path is authoritative.

Move to the next due node.

---

## Step 2b: Feynman verification — claimed `[~]` nodes

After the SR pass (or if no `[✓]` nodes were due), check if `[~]` nodes exist.

If `[~]` nodes exist, offer: "You have [N] claimed (unverified) skill(s). Want to verify one? A teaching-level answer earns `[✓]`."

If user agrees (or if there were no `[✓]` nodes due and `[~]` nodes exist):

- Pick the highest-priority `[~]` node: ROOT > A > B > C > D > E; leftmost first within each branch.
- Present it:
  ```
  Verifying: [Node name]
  What mastery looks like: [the mastery criterion — one sentence]
  ```
- Ask one Feynman question: "Explain [X] as you'd teach it — include the *why*, a concrete scenario, and one edge case or tradeoff."
- Apply the Feynman rubric:
  - **Pass** — answer includes why, a scenario with context, and an edge/tradeoff: change the node line to `[✓|exercise] Node name — [repo], [today]: verified via Feynman in /ramp:review` (omit the `| next:` field — `save_graph` fills it). Then call `mcp__knowledge-graph__save_graph(topic=[active-topic], content=[full updated tree])`; it recomputes XP and fills the L1 review date. This `[~]→[✓]` upgrade **does** raise XP — report the new total from save_graph's confirmation. *(Non-MCP fallback: Edit the line and add `| next: [today+1d] [L1]`.)*
  - **Fail** — vague or affirmation-only ("I've used it", "it does X"): stays `[~]`. Say "Let's revisit — it'll come up again."

Do **one** `[~]` verification per session. End after one regardless of outcome.

---

## Step 3: Persistence (handled by the tools)

When the `knowledge-graph` MCP is configured, `advance_review` (SR passes) and `save_graph` (Feynman upgrades) have already written the file — XP and review dates are computed in code; do **not** hand-edit `xp:` or `| next:`. Only on the non-MCP fallback do you Edit the file directly, per the best-effort notes above.

---

## Step 4: Close

Show a brief summary:
```
Reviewed [N] nodes. [N passed] passed, [N failed] reset. (SR passes advance the schedule; they do not change XP.)
[If Feynman ran] Verified: [node name] → [✓] (XP raised — new total from save_graph)   OR   Unverified: [node name] — try again after practicing it.
Next session: [earliest next: date across all nodes in this topic]
```

If `[~]` nodes remain unverified: "Run `/ramp:review` again to verify more claimed skills, or `/ramp:up` to demonstrate them in-session."

If other topics have due nodes today (from the "All topics" context above), mention: "Also due today: [topic] ([N] nodes). Run `/ramp:review [topic]` when ready."

---

## Constraints

- One node at a time in both queues — do not show all nodes upfront
- Do not ask follow-up questions after the user answers — accept at face value and apply the rubric
- Do not explain the spaced repetition system unless asked
- Do not offer to practice new skills in this command — that's `/ramp:up`
- Feynman verification: one `[~]` node per session, always offered after the SR pass
- Keep the whole session under 5 exchanges per node
