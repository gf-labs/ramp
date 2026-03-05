---
description: Spaced repetition review — practice knowledge tree nodes due today
argument-hint: [optional: topic name]
allowed-tools: Bash, Write, Edit
---

## Context

**Requested topic**: $ARGUMENTS

**Active topic** (first word if it matches a known topic, otherwise "claude-code"):
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ -n "$FIRST" ] && { [ -f "$HOME/.claude/knowledge-trees/schemas/$FIRST.md" ] || [ -f ".claude/knowledge-trees/schemas/$FIRST.md" ]; }; then echo "$FIRST"; else echo "claude-code"; fi`

**Today's date**: !`date +%Y-%m-%d`

**Knowledge tree contents** (for active topic):
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ -n "$FIRST" ] && { [ -f "$HOME/.claude/knowledge-trees/schemas/$FIRST.md" ] || [ -f ".claude/knowledge-trees/schemas/$FIRST.md" ]; }; then TOPIC="$FIRST"; else TOPIC="claude-code"; fi; cat ~/.claude/knowledge-trees/$TOPIC.md 2>/dev/null || echo "NO_TREE_FILE:$TOPIC"`

**All topics — earliest due dates** (to check if other topics have due nodes):
!`for f in ~/.claude/knowledge-trees/*.md; do [ -f "$f" ] || continue; TOPIC=$(basename "$f" .md); EARLIEST=$(grep -oP "next: \K[0-9]{4}-[0-9]{2}-[0-9]{2}" "$f" 2>/dev/null | sort | head -1); [ -n "$EARLIEST" ] && echo "$TOPIC: next review $EARLIEST"; done 2>/dev/null || echo "none"`

---

## Your role

You are running a focused spaced repetition review session. No full assessment, no tree rendering, no questions about new skills. Only review nodes that are due.

**Interval ladder:**
- L1 = 1 day · L2 = 3 days · L3 = 7 days · L4 = 21 days · L5 = 60 days · L6 = permanent (no further review)

---

## Step 1: Find due nodes

Read the knowledge tree above. Find all `[✓]` nodes where the `next: YYYY-MM-DD` date is **≤ today's date**.

If `NO_TREE_FILE:[topic]`: say "No knowledge tree found for **[topic]**. Run `/sup [topic]` to create one." Stop.

If no due nodes today: say "Nothing due today for **[topic]**." Then show the earliest upcoming review date from the tree (lowest future `next:` date). Check the "All topics" list above and mention if other topics have due nodes. End with: "Run `/sup [topic]` to practice new skills."

If due nodes exist: proceed to Step 2.

---

## Step 2: Run reviews

Open with: "**[N] node(s) due for review in [topic]** — let's go through them."

For each due node, one at a time:

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

Wait for the user's answer. Apply the qualitative rubric:
- **Pass** — specific, verifiable detail: advance one level (L1→L2→...→L5), compute new `next` date
- **Fail** — vague or no: reset to L1, `next = today + 1 day`

Tell the user the result with XP delta:
- **Pass**: "✓ Solid — moved to [LN+1], next review [date]. +[XP] XP" (XP per branch: ROOT=10, A=15, B=20, C=25, D=35, E=50 — award the full node XP as a review bonus)
- **Fail**: "× Let's revisit soon — reset to L1, next review [tomorrow]. +0 XP"

New `next` dates by level after pass: L1→L2=today+3d, L2→L3=today+7d, L3→L4=today+21d, L4→L5=today+60d, L5→L6=permanent.

Move to the next due node.

---

## Step 3: Update the saved file

After all due nodes are reviewed, update `~/.claude/knowledge-trees/[topic].md`:

- For each reviewed node, update the `| next: YYYY-MM-DD [LN]` field on its line
- Recompute total XP (XP per branch: ROOT=10, A=15, B=20, C=25, D=35, E=50; [✓]=full, [~]=half, [ ]=0) and update the `xp:` field in YAML frontmatter
- Update the `updated: YYYY-MM-DD` field in the YAML frontmatter to today's date
- Do not change any other fields, statuses, or content

Use Edit tool to make targeted replacements.

---

## Step 4: Close

Show a brief summary:
```
Reviewed [N] nodes. [N passed] passed, [N failed] reset. +[total XP] XP this session.
Next session: [earliest next: date across all nodes in this topic]
```

If other topics have due nodes today (from the "All topics" context above), mention: "Also due today: [topic] ([N] nodes). Run `/review [topic]` when ready."

---

## Constraints

- One node at a time — do not show all nodes upfront
- Do not ask follow-up questions after the user answers — accept at face value and apply the rubric
- Do not explain the spaced repetition system unless asked
- Do not offer to practice new skills in this command — that's `/sup`
- Keep the whole session under 5 exchanges per node
