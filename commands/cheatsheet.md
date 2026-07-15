---
description: Personal cheat sheet — your demonstrated knowledge with real examples
argument-hint: [optional: topic name]
allowed-tools: Bash
model: claude-haiku-4-5-20251001
---

## Context

**Requested topic**: $ARGUMENTS

**First-run signal** (zero started topics ⇒ redirect a newcomer):
!`python3 "$CLAUDE_PLUGIN_ROOT/ramp_core.py" catalog 2>/dev/null | python3 -c "import sys,json; c=json.load(sys.stdin); print('FIRST_RUN' if not any(t['started'] for t in c) else 'HAS_GRAPHS')" 2>/dev/null || echo "HAS_GRAPHS"`

**Active topic** (first word if it matches a known topic, otherwise "claude-code"):
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ -n "$FIRST" ] && { [ -f "$HOME/.claude/ramp/schemas/$FIRST.md" ] || [ -f ".claude/knowledge-graphs/schemas/$FIRST.md" ]; }; then echo "$FIRST"; else echo "claude-code"; fi`

**Knowledge graph contents** (for active topic):
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ -n "$FIRST" ] && { [ -f "$HOME/.claude/ramp/schemas/$FIRST.md" ] || [ -f ".claude/knowledge-graphs/schemas/$FIRST.md" ]; }; then TOPIC="$FIRST"; else TOPIC="claude-code"; fi; cat ~/.claude/ramp/graphs/$TOPIC.md 2>/dev/null || echo "NO_TREE_FILE:$TOPIC"`

**Topic schema** (for source_url links):
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ -n "$FIRST" ] && { [ -f "$HOME/.claude/ramp/schemas/$FIRST.md" ] || [ -f ".claude/knowledge-graphs/schemas/$FIRST.md" ]; }; then TOPIC="$FIRST"; else TOPIC="claude-code"; fi; cat ~/.claude/ramp/schemas/$TOPIC.md 2>/dev/null | grep -E "^\|.*http" | head -40 || echo "NO_SCHEMA"`

---

## Your role

**Empty-state redirect (check first):** If the **First-run signal** (auto-collected context) is `FIRST_RUN` — no graphs exist yet — do not render an empty cheatsheet. This takes precedence over the `NO_TREE_FILE` handling below; short-circuit and say:
> No demonstrated skills yet. Run `/ramp:help` for orientation, then `/ramp:up <topic>` to start building your graph. Browse topics with `/ramp:list`.

Then stop.

Read the knowledge graph above and render a **personal cheat sheet** — a structured reference of everything the user has demonstrated, with their own evidence trails as examples.

This is personal documentation generated from what they've actually done, not generic docs.

**If `NO_TREE_FILE:[topic]`:** Say "No knowledge graph yet for **[topic]**. Run `/ramp:up [topic]` to start one — your demonstrated skills will appear here."

---

## Rendering the cheat sheet

For each section in the tree, in the order they appear:

1. Only include sections that have at least one `[✓]` node
2. Render the section header as its plain title — the text after the closing `]`; the bracketed prefix is internal, never shown: `## Agents and Orchestration`
3. For each `[✓]` node in that branch:

```
**[Node name]**
- *[repo, date]*: [evidence trail note]
- Reference: [link from source_url if available]
```

If a `[✓]` node has no evidence trail (old file format), show it with just `- *(demonstrated)*` and the reference link if available.

Skip all `[~]`, `[ ]`, `[·]` nodes entirely — this is a reference of what's been proven, not a gap analysis.

---

## Format rules

- No status markers (`[✓]`, `[~]`) in the output — the cheat sheet assumes everything shown is demonstrated
- No review dates or ids (`| next: …`, `| id: …`) — strip both from the evidence trail display
- Each node fits in 2–4 lines: name, evidence, reference
- Branch headers only appear if the branch has demonstrated nodes
- If all branches are empty (no `[✓]` nodes at all): "Nothing demonstrated yet. Run `/ramp:up` to start your first session."

---

## Close

End with one line:
```
[N] skills documented · Level: [level from frontmatter] · [XP] XP
```

Then: "Run `/ramp:up` to add more demonstrated skills to this reference."

---

## Constraints

- No assessment questions
- No tree rendering with status markers
- No gap analysis or frontier suggestions
- No writes — this is read-only
- Keep it scannable: this is a reference, not a report
