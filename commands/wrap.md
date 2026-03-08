---
description: End-of-session knowledge harvest — upgrade nodes, update SR schedule, optional snapshot
argument-hint: [optional: topic name]
allowed-tools: Bash, Read, Write, Edit
---

## Context

**Requested topic**: $ARGUMENTS

**Active topic**:
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ -n "$FIRST" ] && { [ -f "$HOME/.claude/knowledge-graphs/schemas/$FIRST.md" ] || [ -f ".claude/knowledge-graphs/schemas/$FIRST.md" ]; }; then echo "$FIRST"; else echo "claude-code"; fi`

**Today's date**: !`date +%Y-%m-%d`

**Knowledge graph** (active topic):
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ -n "$FIRST" ] && { [ -f "$HOME/.claude/knowledge-graphs/schemas/$FIRST.md" ] || [ -f ".claude/knowledge-graphs/schemas/$FIRST.md" ]; }; then TOPIC="$FIRST"; else TOPIC="claude-code"; fi; cat ~/.claude/knowledge-graphs/$TOPIC.md 2>/dev/null || echo "NO_TREE_FILE:$TOPIC"`

**All available topics**:
!`ls ~/.claude/knowledge-graphs/*.md 2>/dev/null | xargs -I{} basename {} .md | sort || echo "none"`

---

## Your role

You are the end-of-session knowledge harvester for ramp. Work through the steps below in order. Each step waits for the user's reply before proceeding. Do not skip steps unless the user says `skip`.

---

## Step 0 — Reflect

Scan the **current session's conversation** for evidence of demonstrated knowledge:
- Tool use patterns (Write, Edit, Bash, MCP calls, Agent launches)
- Exercises completed, configurations made, commands run
- Feynman-level explanations given (not just "I've used this")
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

On confirmation, update `~/.claude/knowledge-graphs/[topic].md`:

For each confirmed upgrade:
- Replace the node line status and append evidence trail:
  ```
  [✓|exercise] Node name — [repo/context], [today]: [evidence] in /ramp:wrap | next: [today+1d] [L1]
  ```
- If node already had evidence, append with ` · ` separator before the `| next:` field

Also update:
- `xp:` in YAML frontmatter — recompute from all nodes (ROOT=10, A=15, B=20, C=25, D=35, E=50; `[✓]`=full, `[~]`=half)
- `updated: YYYY-MM-DD` frontmatter field to today

Use Edit tool for targeted replacements (do not rewrite whole file).

If `NO_TREE_FILE:[topic]`: say "No knowledge graph file found. Run `/ramp:up [topic]` to create one." Skip to Step 3.

---

## Step 3 — Optional snapshot

Ask: "Add a ramp-focused note to MEMORY.md? Reply `yes` or `skip`."

If `yes`: draft 3–5 bullets covering only ramp-relevant context from this session:
- Which nodes were upgraded and why
- Any exercises or patterns that were demonstrated
- Topics or areas to revisit

Append to the project MEMORY.md (same scope logic as `/tools:wrap` Step 1).
Do NOT duplicate housekeeping context (git, plans, backlog) — that belongs in `/tools:wrap`.

---

## Wrap-up

Show a one-line summary:
```
## ramp:wrap — [date]
[topic]: [N] node(s) upgraded. XP: [old] → [new]. Next review: [earliest next: date].
[If no upgrades: "No upgrades this session."]
[If snapshot: "Snapshot: saved." else "Snapshot: skipped."]
```

Then: "Run `/tools:wrap` for housekeeping (git, plans, backlog, done marker)."

---

## Constraints

- Never downgrade a `[✓]` node
- Use Edit tool for targeted replacements — do not rewrite whole graph file
- Evidence must be specific — reject vague signals ("user seemed to understand X")
- One topic per session — if `$ARGUMENTS` is blank, default to `claude-code`
- Do not run housekeeping steps — those belong in `/tools:wrap`
