---
description: Display your knowledge graph — /ramp:tree, /ramp:tree [topic], or /ramp:tree all
argument-hint: [optional: topic name or "all"]
allowed-tools: Bash
model: claude-haiku-4-5-20251001
---

## Context

**Requested topic**: $ARGUMENTS

**Active topic** (first word if it matches a known topic, otherwise "claude-code"):
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ "$FIRST" = "all" ]; then echo "all"; elif [ -n "$FIRST" ] && { [ -f "$HOME/.claude/knowledge-graphs/schemas/$FIRST.md" ] || [ -f ".claude/knowledge-graphs/schemas/$FIRST.md" ]; }; then echo "$FIRST"; else echo "claude-code"; fi`

**Available knowledge graphs**:
!`ls ~/.claude/knowledge-graphs/*.md 2>/dev/null | while read f; do TOPIC=$(basename "$f" .md); LEVEL=$(python3 -c "import re; lines=open('$f').read(); m=re.search(r'^level: (.+)$', lines, re.M); print(m.group(1) if m else 'unknown')" 2>/dev/null || echo "?"); echo "  $TOPIC — $LEVEL"; done || echo "  none yet"`

**Requested tree contents**:
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ "$FIRST" = "all" ]; then for f in ~/.claude/knowledge-graphs/*.md; do [ -f "$f" ] && echo "=== $(basename $f .md) ===" && cat "$f" && echo; done; elif [ -n "$FIRST" ] && { [ -f "$HOME/.claude/knowledge-graphs/schemas/$FIRST.md" ] || [ -f ".claude/knowledge-graphs/schemas/$FIRST.md" ]; }; then cat ~/.claude/knowledge-graphs/$FIRST.md 2>/dev/null || echo "NO_TREE_FILE:$FIRST"; else cat ~/.claude/knowledge-graphs/claude-code.md 2>/dev/null || echo "NO_TREE_FILE:claude-code"; fi`

---

## Your role

Read the "Active topic" and "Requested tree contents" above.

**If `$ARGUMENTS` is empty or defaults to `claude-code`:**
1. Show the Available knowledge graphs list (as a summary — topic name + level)
2. Display the `claude-code` tree contents cleanly
3. End with: "To show a different topic: `/ramp:tree [topic]`. To show all: `/ramp:tree all`."

**If `$ARGUMENTS` is a specific topic (e.g., `best-practices`):**
1. Display that topic's tree contents cleanly
2. If `NO_TREE_FILE:[topic]`, say: "No tree yet for **[topic]**. Run `/ramp:up [topic]` to create one."
3. End with: "To share: copy the contents of `~/.claude/knowledge-graphs/[topic].md`"

**If `$ARGUMENTS` is `all`:**
1. Show each tree separated by a topic header
2. End with: "To share a specific tree: copy the contents of `~/.claude/knowledge-graphs/[topic].md`"

This is a read-only viewer. No inference, no writes, no questions.
