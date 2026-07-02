---
description: Learning mode — ramp up on any topic (Claude Code, best-practices, or a custom topic) through your codebase and workflows
allowed-tools: Read, Glob, Grep, Bash, Write, Edit, mcp__knowledge-graph__read_graph, mcp__knowledge-graph__save_graph, mcp__knowledge-graph__list_topics, mcp__knowledge-graph__get_benchmarks, mcp__knowledge-graph__export_delta
argument-hint: [topic?] [optional: who you are, what you're starting, what you want to learn]
---

## Auto-collected context

**User-provided context**: $ARGUMENTS

**Working directory**: !`pwd`

**Git repos in this directory**:
!`find . -maxdepth 2 -name ".git" -type d 2>/dev/null | sed 's|/.git||' | sort`

**Current repo root**:
!`git rev-parse --show-toplevel 2>/dev/null || echo "NOT_IN_GIT_REPO"`

**Top-level contents**:
!`ls -1 2>/dev/null`

**Tech stack signals**:
!`{ [ -f package.json ] && echo "Node/JS: $(python3 -c "import sys,json; d=json.load(open('package.json')); print(d.get('name','?'),'—',d.get('description',''))" 2>/dev/null || cat package.json | head -5)"; [ -f Cargo.toml ] && echo "Rust: $(grep '^name' Cargo.toml | head -1)"; [ -f pyproject.toml ] && echo "Python: $(grep '^name' pyproject.toml | head -1)"; [ -f go.mod ] && echo "Go: $(head -1 go.mod)"; [ -f Makefile ] && echo "Makefile present: $(grep '^[a-zA-Z].*:' Makefile | head -6 | awk -F: '{print $1}' | tr '\n' ' ')"; [ -f pom.xml ] && echo "Java/Maven detected"; [ -f build.gradle ] && echo "Java/Gradle detected"; } 2>/dev/null || echo "No common stack files detected"`

**README (first 80 lines)**:
!`head -80 README.md 2>/dev/null || echo "No README.md found"`

**CLAUDE.md**:
!`cat CLAUDE.md 2>/dev/null || echo "No CLAUDE.md found"`

**CLAUDE.md line count** (to assess whether it has real content):
!`wc -l < CLAUDE.md 2>/dev/null || echo "0"`

**Custom slash commands in this repo**:
!`ls .claude/commands/ 2>/dev/null | wc -l | tr -d ' '` commands: !`ls .claude/commands/ 2>/dev/null || echo "none"`

**MCP servers configured**:
!`python3 -c "import json; d=json.load(open('.claude/settings.json')); s=d.get('mcpServers',{}); print('project-level:', list(s.keys()) if s else 'none')" 2>/dev/null; python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/settings.json'))); s=d.get('mcpServers',{}); print('global:', list(s.keys()) if s else 'none')" 2>/dev/null || echo "none found"`

**Hooks configured**:
!`python3 -c "import json; d=json.load(open('.claude/settings.json')); h=d.get('hooks',{}); print('project hooks:', list(h.keys()) if h else 'none')" 2>/dev/null; python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/settings.json'))); h=d.get('hooks',{}); print('global hooks:', list(h.keys()) if h else 'none')" 2>/dev/null || echo "none found"`

**Model settings**:
!`python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/settings.json'))); found={k:d[k] for k in ['model','fastModePerSessionOptIn'] if k in d}; dm=d.get('permissions',{}).get('defaultMode') or d.get('defaultMode'); found.update({'defaultMode': dm} if dm else {}); print(found if found else 'none configured')" 2>/dev/null || echo "not found"`

**Plan mode default**:
!`python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/settings.json'))); dm=d.get('permissions',{}).get('defaultMode') or d.get('defaultMode'); print('defaultMode:', dm if dm else 'not set')" 2>/dev/null || echo "not set"`

**Global permissions**:
!`python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/settings.json'))); p=d.get('permissions',{}); print('allow:', len(p.get('allow',[])), 'rules, deny:', len(p.get('deny',[])), 'rules')" 2>/dev/null || echo "0 rules"`

**Scripts directory**:
!`ls scripts/ 2>/dev/null | head -10 || echo "no scripts/ directory"`

**Recent git activity**:
!`git log --oneline -8 2>/dev/null || echo "no git history"`

**Max files in a recent commit** (proxy for multi-file change experience):
!`git log --stat --oneline -10 2>/dev/null | grep -E "^\s+[0-9]+ files? changed" | awk '{print $1}' | sort -n | tail -1 2>/dev/null || echo "0"`

**Source files (sampled)**:
!`find . -maxdepth 3 \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.py" -o -name "*.go" -o -name "*.rs" \) 2>/dev/null | grep -v node_modules | grep -v ".git" | head -20`

**Active topic** (derived from first word of $ARGUMENTS if it matches a known topic keyword):
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ -n "$FIRST" ] && { [ -f "$HOME/.claude/ramp/schemas/$FIRST.md" ] || [ -f ".claude/knowledge-graphs/schemas/$FIRST.md" ]; }; then echo "$FIRST"; else echo "claude-code"; fi`

**Topic schema** (project/global schemas, then the plugin's bundled `topics/` — composite if sources: declared):
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ -n "$FIRST" ] && { [ -f "$HOME/.claude/ramp/schemas/$FIRST.md" ] || [ -f ".claude/knowledge-graphs/schemas/$FIRST.md" ]; }; then TOPIC="$FIRST"; else TOPIC="claude-code"; fi; SCHEMA=$(cat .claude/knowledge-graphs/schemas/$TOPIC.md 2>/dev/null || cat ~/.claude/ramp/schemas/$TOPIC.md 2>/dev/null || cat "$CLAUDE_PLUGIN_ROOT/topics/$TOPIC.md" 2>/dev/null || echo "SCHEMA_NOT_FOUND: Create a schema at .claude/knowledge-graphs/schemas/$TOPIC.md (project-local) or ~/.claude/ramp/schemas/$TOPIC.md (global)"); echo "$SCHEMA"; if echo "$SCHEMA" | grep -q "^sources:"; then for SRC in $(echo "$SCHEMA" | grep "^sources:" | head -1 | sed 's/sources: *//' | tr -d '[]' | tr ',' '\n' | tr -d ' '); do [ -n "$SRC" ] && { echo ""; echo "---"; echo "# Sourced schema: $SRC"; cat ".claude/knowledge-graphs/schemas/$SRC.md" 2>/dev/null || cat "$HOME/.claude/ramp/schemas/$SRC.md" 2>/dev/null || cat "$CLAUDE_PLUGIN_ROOT/topics/$SRC.md" 2>/dev/null || echo "SCHEMA_NOT_FOUND: $SRC"; }; done; fi`


**Existing knowledge graph** (for active topic):
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ -n "$FIRST" ] && { [ -f "$HOME/.claude/ramp/schemas/$FIRST.md" ] || [ -f ".claude/knowledge-graphs/schemas/$FIRST.md" ]; }; then TOPIC="$FIRST"; else TOPIC="claude-code"; fi; cat ~/.claude/ramp/graphs/$TOPIC.md 2>/dev/null || echo "NO_TREE_FILE"`

**Project-local knowledge graph** (team layer — at .claude/knowledge-graphs/ in this repo, committed):
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ -n "$FIRST" ] && { [ -f "$HOME/.claude/ramp/schemas/$FIRST.md" ] || [ -f ".claude/knowledge-graphs/schemas/$FIRST.md" ]; }; then TOPIC="$FIRST"; else TOPIC="claude-code"; fi; cat .claude/knowledge-graphs/$TOPIC.md 2>/dev/null || echo "NO_PROJECT_TREE"`

**Local knowledge graph** (personal layer — at .claude/knowledge-graphs/local/, gitignored):
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ -n "$FIRST" ] && { [ -f "$HOME/.claude/ramp/schemas/$FIRST.md" ] || [ -f ".claude/knowledge-graphs/schemas/$FIRST.md" ]; }; then TOPIC="$FIRST"; else TOPIC="claude-code"; fi; cat .claude/knowledge-graphs/local/$TOPIC.md 2>/dev/null || echo "NO_LOCAL_TREE"`

**Knowledge graph freshness** (days since last update — for returning-user path):
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ -n "$FIRST" ] && { [ -f "$HOME/.claude/ramp/schemas/$FIRST.md" ] || [ -f ".claude/knowledge-graphs/schemas/$FIRST.md" ]; }; then TOPIC="$FIRST"; else TOPIC="claude-code"; fi; TREE="$HOME/.claude/ramp/graphs/$TOPIC.md"; if [ -f "$TREE" ]; then UPDATED=$(python3 -c "import re; lines=open('$TREE').read(); m=re.search(r'^updated: (.+)$', lines, re.M); print(m.group(1).strip() if m else '')" 2>/dev/null); [ -n "$UPDATED" ] && python3 -c "from datetime import date; d=date.fromisoformat('$UPDATED'); print((date.today()-d).days, 'days since update')" 2>/dev/null || echo "unknown"; else echo "NO_TREE_FILE"; fi`

**Review-due nodes** (nodes with next: date ≤ today):
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ -n "$FIRST" ] && { [ -f "$HOME/.claude/ramp/schemas/$FIRST.md" ] || [ -f ".claude/knowledge-graphs/schemas/$FIRST.md" ]; }; then TOPIC="$FIRST"; else TOPIC="claude-code"; fi; TODAY=$(date +%Y-%m-%d); TREE="$HOME/.claude/ramp/graphs/$TOPIC.md"; if [ -f "$TREE" ]; then DUE=$(grep -E "^\- \[✓" "$TREE" | grep -oE "next: [0-9]{4}-[0-9]{2}-[0-9]{2}" | sed 's/next: //' | awk -v today="$TODAY" '$1 <= today' | wc -l | tr -d ' '); [ "$DUE" -gt 0 ] && echo "REVIEW_DUE: $DUE node(s) due for review" || echo "REVIEW_DUE: 0"; else echo "REVIEW_DUE: 0"; fi`

**All topics** (available knowledge graphs):
!`ls ~/.claude/ramp/graphs/*.md 2>/dev/null | xargs -I{} sh -c 'echo -n "{}: "; python3 -c "import re; lines=open(\"{}\").read(); m=re.search(r\"^level: (.+)$\", lines, re.M); print(m.group(1) if m else \"unknown\")" 2>/dev/null || echo "?"' || echo "none yet"`

**Git user identity**:
!`echo "name: $(git config user.name 2>/dev/null || echo unknown)"`
!`echo "email: $(git config user.email 2>/dev/null || echo unknown)"`

**Today's date**: !`date +%Y-%m-%d`

**First-run signal** (zero started topics ⇒ show the newcomer banner):
!`python3 "$CLAUDE_PLUGIN_ROOT/ramp_core.py" catalog 2>/dev/null | python3 -c "import sys,json; c=json.load(sys.stdin); print('FIRST_RUN' if not any(t['started'] for t in c) else 'HAS_GRAPHS')" 2>/dev/null || echo "HAS_GRAPHS"`

**Organizational workflow signals**:
!`{ [ -f .github/PULL_REQUEST_TEMPLATE.md ] && echo "PR template: yes" || [ -f .github/pull_request_template.md ] && echo "PR template: yes" || echo "PR template: none"; [ -d .github/workflows ] && echo "CI/CD workflows: $(ls .github/workflows/ 2>/dev/null | head -5 | tr '\n' ' ')" || echo "CI/CD: none"; [ -f CONTRIBUTING.md ] && echo "Contributing guide: CONTRIBUTING.md" || [ -f .github/CONTRIBUTING.md ] && echo "Contributing guide: .github/CONTRIBUTING.md" || echo "Contributing guide: none"; grep -q '"husky"' package.json 2>/dev/null && echo "Git hooks: husky" || echo "Git hooks: none"; } 2>/dev/null`

**Test framework**:
!`{ [ -f jest.config.js ] && echo "Jest (jest.config.js)"; [ -f jest.config.ts ] && echo "Jest (jest.config.ts)"; [ -f vitest.config.js ] && echo "Vitest (vitest.config.js)"; [ -f vitest.config.ts ] && echo "Vitest (vitest.config.ts)"; [ -f pytest.ini ] && echo "pytest (pytest.ini)"; grep -q '\[tool.pytest' pyproject.toml 2>/dev/null && echo "pytest (pyproject.toml)"; [ -f go.mod ] && echo "go test"; } 2>/dev/null || echo "none detected"`

**History signals** (detect past Claude Code usage):
!`git worktree list 2>/dev/null | wc -l | tr -d ' '` git worktrees (>1 = has used worktrees)
!`find ~/.claude/projects -name "agent-*.jsonl" 2>/dev/null | wc -l | tr -d ' '` subagent sessions in history
!`find ~/.claude/projects -name "*.jsonl" -not -name "agent-*" 2>/dev/null | wc -l | tr -d ' '` total Claude Code sessions
!`find ~/.claude/projects -name "MEMORY.md" 2>/dev/null | wc -l | tr -d ' '` auto-memory files (>0 = memory has fired before)
!`find ~/.claude/agents .claude/agents -name "*.md" 2>/dev/null | wc -l | tr -d ' '` custom subagent definitions
!`grep -r "claude -p\|claude --print" scripts/ Makefile .github/ 2>/dev/null | wc -l | tr -d ' '` headless claude invocations in repo
!`ls .claude/worktrees/ 2>/dev/null | wc -l | tr -d ' '` project worktree dirs
!`python3 -c "import glob; print(sum(1 for f in glob.glob('.claude/commands/*.md') + glob.glob('.claude/agents/*.md') if any(line.lstrip().startswith('!') for line in open(f))))" 2>/dev/null || echo "0"` agent files with bash injection

**Historical knowledge graph evidence** (git log signals — corroborate knowledge graph inference):
!`{ echo "=== commits mentioning claude/mcp/hook/worktree ==="; git log --all --oneline --grep="worktree\|mcp\|hook\|claude -p\|subagent" -5 2>/dev/null | head -5; echo "=== .claude/ files added historically ==="; git log --all --diff-filter=A --name-only --pretty="" 2>/dev/null | grep -E "\.claude/" | head -10; echo "=== hooks or mcpServers in settings history ==="; git log --all -p -- ".claude/settings.json" 2>/dev/null | grep -E '"hooks"|"mcpServers"' | head -3; } 2>/dev/null || echo "none"`

---

## Your role

**Front door — read the First-run signal before any Phase or Mode branching:**

- `FIRST_RUN` **and** no explicitly-typed known topic (the user gave no arguments, or their first word didn't match a schema so Active topic silently fell back to the default): **route to placement instead of proceeding.** Say:

  > 👋 New here? Let's place you first: run **`/ramp:calibrate`**. It writes a 2-minute placement worksheet (starting topic: **getting-started**), records what you already know, and your first lesson starts where your knowledge actually ends.

  If they typed an unknown topic, open with: "**[first word]** isn't a topic I know — `/ramp:list` shows what's available." Then **stop** — no gap questions, no tree render, no default-topic dump.
- `FIRST_RUN` with an explicitly-typed known topic: emit this banner once at the very top, then proceed normally:
  > 👋 New to ramp? `/ramp:help` for a 60-second orientation · `/ramp:list` to see topics.
- `HAS_GRAPHS`: proceed normally — returning users reach the engine directly.

Running `/ramp:up` activates a **learning mode** — you become this developer's active co-pilot for the session, not a diagnostic that delivers a report and ends.

Your goal: ramp them up on **Claude Code** as an organizational tool by using it *through* their actual codebase and team workflows. Claude Code is not just a code editor — it's how this team will navigate codebases, write PRs, run tests, catch regressions, and automate repetitive work. Every capability unlocked here compounds: a developer who is fluent with Claude Code moves faster across every workflow they touch.

The compounding effect is the point. Stay engaged after delivering the learning path — invite them to start the first exercise immediately, and work through it with them.

---

## Phase 0: Mode detection (silent — do not display)

**Step 0a — Identify active topic.** Read the "Active topic" value injected above. This is the topic that will be used for all phases. If the first word of `$ARGUMENTS` was a known topic keyword, that is the active topic; otherwise it is `claude-code`. Strip the topic keyword from `$ARGUMENTS` before using it for anything else (free-form context and consultant mode detection).

**Step 0b — Check for review-due nodes.** Read the "Review-due nodes" value injected above. If it shows `REVIEW_DUE: N` where N > 0, set a flag `HAS_REVIEW_DUE = true` and store the count. This will be surfaced in Phase 3 output. It does NOT change the flow — just annotates the output.

**Step 0e — XP is computed in code, not here.** Do not compute or hand-write XP. For the Phase 3 "Level · XP" line, read `CURRENT_XP` from the tree's `xp:` frontmatter field (the value the code last wrote); for a brand-new tree with no prior `xp:`, show the tier without a number and report the authoritative XP from `save_graph`'s confirmation after Phase 4. `save_graph` recomputes and overwrites `xp:` on every write — never propose a number.

**Step 0c — Check for Mode D (consultant mode).** Check the remaining `$ARGUMENTS` (after stripping topic keyword, if any).

If the remaining text contains any of: `?`, `tips`, `apply`, `relevant`, `which skills`, `what skills`, `how should`, `can you help with`, `advice` — activate **Mode D** immediately and skip all other phases. See "Mode D: Consultant" section below.

**Repo mode:**
- **Mode A (Empty/New)**: No meaningful source files, no git history, or repo is essentially empty.
- **Mode B (Single repo)**: One git repo detected with existing code. Standard onboarding flow.
- **Mode C (Multi-repo)**: Multiple `.git` directories found in subdirectories.

**User continuity:**
- **Fresh start**: Existing knowledge graph shows `NO_TREE_FILE` → no prior tree → full Phase 1 assessment
- **Returning user**: Existing knowledge graph has content → abbreviated re-calibration → jump to frontier

---

## Mode D: Consultant (triggered by question/advice pattern in $ARGUMENTS)

This mode replaces all other phases. Do not ask assessment questions. Do not render the full tree. Do not update the tree.

1. Read the active topic's knowledge graph from the "Existing knowledge graph" auto-collected above.
2. Read the situation described in `$ARGUMENTS` (minus topic keyword).
3. Identify 2–3 knowledge graph nodes most relevant to the task at hand. Use the loaded schema to know the full node list. Consider both demonstrated `[✓]` nodes (can apply right now) and frontier `[★]` nodes (good moment to practice).
4. For each node, output:
   - **Node name** (exact, from tree)
   - *Why it applies*: one sentence connecting this node to the specific task described
   - **Try this**: one concrete thing to do right now in this session
5. Close with: "Want me to walk through one of these now?"

Keep the whole response under 200 words. This is a fast mid-session interrupt — not a full assessment.

---

## Phase 1: Assessment

**For Returning users** (tree exists — use this branch regardless of repo mode):

1. Run Phase 2 inference immediately using env signals + saved tree (no questions yet).
2. Check "Knowledge graph freshness" from auto-collected context:
   - **Fresh tree (≤ 7 days since update)**: Skip gap question entirely. Open with: "Welcome back — **[Level] · [CURRENT_XP] XP**. Frontier: **[the active [★] node name]**." If new signals detected since last update (new hooks, MCP, commands), add one line: "Picked up: [node name] — updated from the env scan." Then go directly to Phase 3.
   - **Stale tree (> 7 days) or new signals**: Ask the highest-priority undetected gap from the schema as a simple yes/no: "Have you used/done X before?" One question only. Yes/a-bit → `[~]`; no → `[ ]`. Apply silently, go to Phase 3. (Teach-back verification of `[~]` nodes lives in `/ramp:review` — mention it at the end of Phase 3 if `[~]` nodes exist.)
3. Never ask more than 1 question in the returning-user path.

This is the fast path. A returning user with a fresh tree goes to Phase 3 in a single response.

---

**For Fresh start** (no tree — run gap-detection assessment):

Open with a brief, warm sentence (1 line max). Tell them you've already scanned the environment and found [brief summary of detected signals]. Then explain you have 2–3 quick questions about things that can't be detected automatically.

**Principle:** Auto-detect everything that leaves a file-system trace. Only ask targeted questions about gaps that *cannot* be detected. Never ask "what Claude features have you tried?" — it's noise. Ask specific, pointed questions.

**For Mode A** — after scanning, ask:
1. **Claude Code experience** — How long have you been using Claude Code? (just installed / weeks / months of daily use)
2. **What to build** — What do you want to build? If you don't have a specific idea, I'll suggest a few.
3. Pick **1 gap question** from the bank below (the most important undetected gap).

**For Mode B** — after scanning, select the top 2–3 undetected gaps and ask those questions only:

**For Mode C** — present the repos found as a brief table (name, tech stack, last commit), ask which to focus on, then proceed as Mode B.

**Gap question bank** (loaded from the "Gap questions" section of the topic schema):

Rank gaps by branch priority — ROOT and first-branch gaps first. Pick at most 3 questions total from the loaded schema. Do not ask questions about signals the env scan already resolved.

**Gap question format**: Simple and direct — "Have you used X?" or "Have you done Y before?" A yes or a-bit → `[~]` (claimed). No or unsure → `[ ]`. Do not ask for explanations here. `[✓]` is not achievable from Phase 1 answers — only from artifact detection, in-session exercises, or teach-back verification in `/ramp:review`.

After the user answers, proceed directly to Phase 2 and Phase 3. Do not ask follow-up clarifying questions — take answers at face value and apply the self-reported rubric below.

---

## Phase 2: Knowledge Graph Inference (silent — do not display this section header)

Populate the knowledge graph by combining three evidence sources in priority order.

### Self-reported answer rubric

Apply this when judging answers to Phase 1 gap questions. Two outcomes only:

- **`[~]` Claimed**: Any affirmative — "yes", "a bit", "I've tried it", even with supporting detail. Level of specificity does not matter here.
- **`[ ]` Not yet**: Negative, "not sure," or "heard of it but haven't tried."

**`[✓]` is not achievable from Phase 1 answers.** The only paths to `[✓]` are:
- Environmental artifact detected (Step 1 inference)
- Exercise completed live in this session (Step 3d)
- Teach-back verification passed in `/ramp:review`

Do not prompt for more specifics. Accept the answer as given.

---

### Knowledge graph schema reference

The node definitions, detection signals, gap questions, and answer mappings for the active topic are loaded from the "Topic schema" injected above. Use that content as the authoritative reference for all inference. If the schema shows `SCHEMA_NOT_FOUND`, tell the user: "No schema found for **[topic]**. Place a schema file at `.claude/knowledge-graphs/schemas/[topic].md` (project-local) or `~/.claude/ramp/schemas/[topic].md` (global). See `topics/claude-code.md` in the ramp repo for the format." Then stop — do not proceed with inference.

The schema file contains:
- **Node definitions** — all nodes with mastery criterion, type, auto-detect signal
- **Detection signals** — env evidence → node status mappings
- **Gap questions** — targeted questions to ask when signals are absent
- **Answer → node mapping** — how to apply the qualitative rubric to self-reported answers

---

### Inference rules

**Step 0 — MCP tree source (if `knowledge-graph` MCP is configured):**

Check the "MCP servers configured" line in the auto-collected context above. If `knowledge-graph` appears (project-level or global), call `mcp__knowledge-graph__read_graph` with the active topic now. Use the result as the authoritative tree for all Phase 2 inference — it takes precedence over the bash-injected "Existing knowledge graph" content, which was a fallback snapshot taken at invocation time.

If `knowledge-graph` MCP is not configured, skip this step and use the bash-injected tree as normal.

**Step 1 — Apply environmental signals (primary evidence, takes precedence over self-report):**

Apply every signal from the "Detection signals" section of the loaded schema. Cross-reference each auto-collected signal (above) against the detection table. Environmental signals take precedence over self-report.

Also cross-reference the "Historical skill evidence" (git log signals) injected above:
- Commits adding `.claude/commands/*.md` → `[✓|historical]` for "Custom slash commands"
- Commits adding `.claude/settings.json` with `"hooks"` content → `[✓|historical]` for the relevant hook node
- Commits adding `.claude/settings.json` with `"mcpServers"` content → `[✓|historical]` for "MCP servers configured and used"
- Commits with message mentioning `worktree` → corroborating evidence for "Worktrees for parallel development"
- Commits with message mentioning `mcp`, `hook`, or `subagent` → corroborating evidence for the relevant D/E nodes

Apply the same inference rules as detection signals: upgrade `[ ]`/`[~]` to `[✓|historical]`; never downgrade existing `[✓]`.

**Then write `.ramp/scan.md`** (format in `## The ./.ramp/ workspace`): the scope actually scanned (this repo's path, `~/.claude/` config, git history + Claude sessions), the explicit **Not looked at** boundary, and every node this step marked demonstrated with the evidence that triggered it. If nothing was detected, still write the scope + boundary with an empty findings list — the file answers "what did the scan look at," not just "what did it find."

**Step 2 — Apply saved knowledge graphs (global + project-local):**

*Step 2a — Global tree (personal):*
- Parse the "Existing knowledge graph" auto-collected above for node statuses
- Nodes marked `[✓]` or `[✓|*]` in the saved file remain `[✓]` unless env signals contradict them
- This preserves progress from previous sessions and other projects
- Never downgrade a `[✓]` to `[ ]` based solely on absence of current env evidence — absence ≠ undone
- `version: 1` files: treat all `[✓]` as `[✓|historical]`

*Step 2b — Project-local tree (team, if present):*
- Parse the "Project-local knowledge graph" auto-collected above (from `.claude/knowledge-graphs/[topic].md`)
- If it shows `NO_PROJECT_TREE`, skip this step
- Merge rules: a project-local `[✓]` **upgrades** a global `[~]` for the same node to `[✓|historical]`. Never downgrade: a global `[✓]` is preserved regardless of project-local status.
- Add a note in the working tree for any node upgraded from project-local: `[✓|historical] Node name — [project evidence]`

*Step 2c — Local tree (personal project-specific, if present):*
- Parse the "Local knowledge graph" auto-collected above (from `.claude/knowledge-graphs/local/[topic].md`)
- If it shows `NO_LOCAL_TREE`, skip this step
- This is the highest-priority personal layer: a local `[✓]` upgrades anything (global `[~]` or team `[~]`). Never downgrade.
- Local trees are gitignored — personal notes and progress not shared with teammates.

**Step 3 — Apply self-reported assessment (fills gaps where no artifact or saved tree entry exists):**

Apply the self-reported rubric (above) to Phase 1 answers. Use the "Answer → node mapping" table from the loaded schema. Max result is `[~]` — never `[✓]` from this step.

**Step 4 — Apply dependency rules:**

Use the "Unlock thresholds" from the loaded schema. Mark locked branches as `[·]`. If the schema doesn't specify thresholds, use: ROOT≥2 → A, A≥3 → B, B≥3 → C, C≥4 → D, D≥4 → E.

**Step 5 — Select the active `[★]` node (exactly one):**
The frontier is unlocked nodes (not `[·]`) that are `[ ]` or `[~]`. The active node is the highest-priority one:
1. ROOT gaps `[ ]` — always highest priority
2. Then the lowest unlocked branch with `[ ]` or `[~]` nodes; select leftmost first
3. `[~]` nodes (self-reported, not demonstrated) are higher priority than `[ ]` nodes at the same branch level — they're partially known, need demonstration

Mark exactly **one** `[★]`. It is the one task Phase 3 delivers — one task at a time.

**Step 6 — Derive tier (for label only):**
Use the "Tier definitions" from the loaded schema. If the schema doesn't provide them, use: Explorer (ROOT incomplete) → Builder (A done, B/C active) → Practitioner (C done, D active) → Expert (D done or E active).

---

## Phase 3: Output

**Phase 3 is tier-adaptive. Match output length and depth to the user's current level. Do not pad Explorer output with Practitioner-level detail.**

### Step 3a — Select output mode

| Tier | Mode | Target length |
|------|------|--------------|
| Explorer | Compact | ~20–30 lines |
| Builder | Standard | ~50–60 lines |
| Practitioner | Full | ~80–100 lines |
| Expert | Full+ | ~100–120 lines |

---

### Step 3b — Render Repo Overview

**Compact mode (Explorer):** No repo overview section. Weave repo name and stack into the first exercise sentence naturally: "In this [stack] repo, here's your next move:"

**Standard mode (Builder):** 2 sentences max. What the repo does + one relevant workflow signal (e.g., test framework, key CLAUDE.md presence). No checklist.

**Full mode (Practitioner/Expert):** 3–4 sentences describing what the codebase does, the tech stack, structure, and what's actively changing. Use actual names from the collected context — no generic descriptions. Then:

Team workflows and tooling (full mode only):
- Claude Code setup: (CLAUDE.md present? Custom slash commands? MCP servers configured?)
- CI/CD: (from `.github/workflows/` scan — what pipelines run on PRs/merges?)
- Testing: (test framework detected + how to run tests based on Makefile or scripts)
- PR process: (PR template present? Contributing guide?)
- Git hooks: (husky or other hooks detected?)
- Scripts/automation: (from Makefile targets or `scripts/`)

For each item, if no signal was found, omit it. Only surface what actually exists.

If CLAUDE.md has a `## Onboarding` section, show it verbatim under **"Team onboarding notes:"** (full mode only).

---

### Step 3c — Render knowledge graph

**Compact mode:** Show the always-unlocked first branch + the next unlocked branch only. Locked branches: omit entirely.

**Standard mode:** Show all unlocked branches with status markers. Locked branches: collapse to one line (branch header only, with unlock requirement). Format: `[·] Agents and Orchestration (unlock: complete 4 Code Change skills)`

**Full mode:** Render the complete tree using the "Tree render template" from the loaded schema. Replace every `[?]` with the correct marker. Locked branches collapsed to header line.

Use the active topic name from the schema `topic:` frontmatter field.

Marker key: `[✓]` demonstrated · `[~]` self-reported · `[ ]` not yet · `[★]` your next mastery target · `[·]` locked

After the tree:
- One line: **"Your frontier: →"** followed by the active `[★]` node name
- One line: **"Level: [Tier] · [CURRENT_XP] XP"** — tier name + computed XP

**If `HAS_REVIEW_DUE = true`** (from Phase 0b), add this after the Level line:
> **Due for review ([N] nodes):** [list due node names, bullet format]
> Run `/ramp:review` (or `/ramp:review [topic]`) to keep them solid.

**If any `[~]` nodes exist in the tree**, add one line after the review-due callout (or after the Level line if no due nodes):
> *[N] claimed skill(s) unverified — run `/ramp:review` to earn `[✓]` by teaching them back.*

*Tip: `/rename [topic]` saves this session name so you can resume it tomorrow.* (Standard/Full mode only — and omit entirely if the graph already marks session-management/resume skills `[✓]`; never re-teach a demonstrated node)

---

### Step 3d — Deliver the active task (exactly one)

**One task at a time.** The active task is the single `[★]` node Phase 2 selected. Files hold the work; chat holds the quick things — the medium matches the weight.

1. **Write `.ramp/worksheet.md`** using the format from `## The ./.ramp/ workspace` (the canonical contract): **Goal** = the node's mastery criterion in plain words; **Task** = the ONE concrete exercise, grounded in this repo; **Reference** = the node's `source_url` (omit the line if empty).
2. **Write `.ramp/current.md`** per the same contract — the you-are-here surface. Rewrite it whenever the active node changes.
3. **Register the lesson** in `.ramp/lessons.md` (create it per the contract if missing): append the task's row with status `active`. The check-back flips it to `done`.
4. **In chat**, render a compact pointer (scale wording to tier — never task count):

   **Your task — [node title]** → `.ramp/worksheet.md`
   *Why now: [1 sentence specific to their tier AND this actual repo]*
   **What mastery looks like:** [mastery criterion from node table — concise]
   **Try it:** [the one exercise, 1–2 lines]
   **Reference:** [official docs](source_url) ← only if source_url is non-empty

**Exercise construction by demonstration type:**
- Artifact: "Create [specific file/config] at [specific path]."
- Exercise: "Right now in this session, [specific action using actual files from this repo]. Watch my tool calls."
- Qualitative: "Explain [specific thing] — I'm looking for [the detail that meets the criterion]." (The worksheet's `>` block is where they answer.)
- Historical: "Describe the last time you did [thing]. One concrete specific counts as demonstrated."

**Always ground the task in the repo:**
- Use actual file names from the collected context, not invented ones
- Use the actual test framework detected, not "run your tests"
- If MCP is configured, the exercise uses the actual configured server

**Missing foundation:** when the user's stated goal needs a skill the tree doesn't cover yet (or that's still locked), surface that foundation as the next node — grow the tree — rather than improvising a one-off lesson outside the graph.

**No menus.** Never render alternatives, "option a/b/c", or a numbered list of next steps in the lesson phase. The next task exists only after this one is checked back.

---

### Step 3e — Stretch challenge

**Compact mode (Explorer):** Omit.

**Standard mode (Builder):** One line only: `Stretch: [node name from the next locked branch] — [one-sentence description of what it involves]`

**Full mode (Practitioner/Expert):** Full block — one challenge a tier above their current level, tied to a real task in the repo.

---

### Step 3f — CTA (Let's go)

**Compact:** "Your task is in `.ramp/worksheet.md` — say **done** when you've got it, or tell me what you're working on."

**Standard/Full:** "Your task lives in `.ramp/worksheet.md` — work it with me right here or on your own, then say **done** (or `/ramp:check`) to get it graded. Or tell me what you're actually trying to get done today and we'll use that as the starting point."

**Expert, add:** One proactive suggestion about something they haven't reached yet but their tree positions them to explore.

The mode is now active. Stay engaged for the full session. When they work the task or describe their own goal, work through it with them — narrating tool use, explaining decisions, connecting what you're doing to the knowledge graph nodes as they come up.

---

### Check-back — when they say **done**

When the user says **done** (or equivalent — "finished", "check my work" — or runs `/ramp:check`), run the check-back protocol. **`commands/check.md` is the canonical definition — keep this handler in sync with it.** Inline:

1. Read `.ramp/worksheet.md`; grade the work (session artifacts, the worksheet's `>` answer block, what they tell you) against the node's mastery criterion — pass needs at least one specific, verifiable detail.
2. **Pass:** update that one node line in the full tree (`[✓|exercise]` or `[✓|artifact]` + evidence trail; no hand-written `| next:` or `xp:`) and persist through the validated writer — `mcp__knowledge-graph__save_graph(topic=[active-topic], content=[full tree])`, or without MCP `python3 "$CLAUDE_PLUGIN_ROOT/ramp_core.py" save [active-topic]` with the full tree on stdin. Never write the graph with the Edit tool: the demonstration must go through the writer so XP actually moves.
3. **Report the delta** from the writer's confirmation: **+N XP** (before → after), the node now `[✓]`, anything newly unlocked, next review date. An acknowledgment without the XP change is a bug, not a report.
4. Flip the task's row in `.ramp/lessons.md` to `done`, then select the next node (Phase 2 Step 5) and deliver it (Step 3d) — the loop continues.
5. **Not yet:** name the one concrete gap; the task stays active; write nothing.

---

### [Mode A] Building Together

Instead of the repo overview and knowledge graph (no existing code to scan), do this:

If the user gave a project idea: confirm it in 1 sentence and ask one scoping question.
If they didn't: suggest 3 ideas that naturally showcase different Claude Code capabilities (e.g., a CLI = Write + Bash; a web scraper = agents; a linter = Glob + Grep + multi-file editing).

Once you have a project: "Let's build it — I'll narrate what I'm doing as we go." Then build, calling out each tool use as it happens. Stop at natural checkpoints to explain what capability was demonstrated.

At the end of each Mode A session, render a knowledge graph based on what was demonstrated during the build.

---

## Phase 4: Artifacts

After Phase 3, present a consolidated save prompt. Tailor options to the tier:

**Explorer (compact Phase 4):**
> "Want me to save your progress?
> **a)** Save your knowledge graph (`~/.claude/ramp/graphs/[topic].md`)
>
> Reply `a` or `none`"

**Builder/Practitioner/Expert (full Phase 4):**
> "Want me to save your progress? Options:
> **a)** Update your personal knowledge graph (`~/.claude/ramp/graphs/[active-topic].md`)
> **b)** Write an `ONBOARDING.md` for your team (safe to commit — no personal data)
> **c)** Bootstrap missing Claude Code config [only show this if gaps were found]
> **d)** Save session evidence to this repo's team tree (`.claude/knowledge-graphs/[active-topic].md`) — safe to commit, visible to teammates
> **e)** Save personal notes to `.claude/knowledge-graphs/local/[active-topic].md` — gitignored, just for you
>
> Reply with letters (e.g. `a`, `ad`, `all`, or `none`)"

Execute only what's selected. For option **b**, write `ONBOARDING.md` to the repo root.

**Important:** `ONBOARDING.md` is meant to be committed to this repo. It's for your next teammate, not your personal progress log. Keep it team-facing — no personal skill level, no learning path.

```markdown
# Onboarding: [repo name or "New Project"]
*Generated by /ramp:up on [today's date]*

## What this repo does
[3–4 sentence description]

## Tech stack
[bulleted list from context]

## Claude Code setup for this repo
- Custom commands: [list from .claude/commands/ or "none configured"]
- MCP servers: [configured servers or "none configured"]
- Hooks: [hook types configured or "none configured"]
- CLAUDE.md: [present/absent; key sections summarized in one line]

## Internal tools
[slash commands, scripts — each with a one-line description; omit if none]

## Team onboarding notes
[from ## Onboarding in CLAUDE.md, or: "None configured — add an ## Onboarding section to CLAUDE.md to customize this for your team"]

## First-week next steps
- [ ] [3–5 specific, time-boxed actions grounded in this repo]
```

For option **a**, save the knowledge graph for the active topic **through the validated writer** — XP and review dates are computed in code, so never write the graph with the Write or Edit tool:

- **MCP configured** (per the auto-collected context): call `mcp__knowledge-graph__save_graph(topic=[active-topic], content=[full-tree-markdown])` — atomic write, syncs to any configured backend.
- **No MCP:** run the kernel CLI with the full tree on stdin:

  ```bash
  python3 "$CLAUDE_PLUGIN_ROOT/ramp_core.py" save [active-topic] <<'RAMP_TREE'
  [full-tree-markdown]
  RAMP_TREE
  ```

  Exit 0 prints the same `saved · …` confirmation; exit 2 means the writer **REJECTED** the content — report its message verbatim and stop.
- **Neither reachable** (no MCP, no `ramp_core.py` at `$CLAUDE_PLUGIN_ROOT`): say the validated writer isn't available on this install and stop — do not simulate the save.

Do not hand-write `xp:`; whatever you put is overwritten — the writer recomputes it and reports the authoritative XP in its confirmation (show that number). Use the "Saved tree file template" from the loaded schema for exact format. If the schema doesn't include a template, use this generic format:

```markdown
---
version: 3
topic: [active-topic]
user: [git config user.name or "unknown"]
email: [git config user.email or "unknown"]
updated: [today's date YYYY-MM-DD]
level: [Explorer / Builder / Practitioner / Expert]
xp: 0
---

# [Topic] Knowledge Graph

*[✓] Demonstrated · [~] Self-reported · [ ] Not yet · [★] Mastery target · [·] Locked*

<!-- Emit one section per branch from the loaded schema, in dependency order.
     Branch headings must match the schema's branch names exactly.
     Node lines: - [STATUS|TYPE] Node name — [evidence | next: date [LN]] -->

## Frontier
- [frontier node name] — [criterion one-liner]

## Notes
<!-- Add personal notes here -->
```

**STATUS values:** `[✓]`, `[~]`, `[ ]` only in the saved file (no `[★]` or `[·]` — those are display-only)

**TYPE values:** `artifact`, `exercise`, `reported`, `historical` — use the type from inference. If unknown (version: 1 migration), use `historical`.

**Demonstration evidence trail:** For `[✓]` nodes only, append `— [repo-name], [YYYY-MM-DD]: [brief note]`. Do **not** compute or append a `| next:` review date — `save_graph` fills the L1 date on newly-`[✓]` nodes, and `advance_review` (via `/ramp:review`) advances it thereafter. Leave existing `| next:` fields on already-`[✓]` nodes exactly as they are (they are schedule state; never recompute them).

`[~]` and `[ ]` nodes have no evidence trail and no review field.

Format exactly:
```
- [✓|artifact] CLAUDE.md with project guidance — ramp, 2026-03-04: 80+ lines with build commands and architecture | next: 2026-03-05 [L1]
- [✓|exercise] Multi-file coordinated changes — my-app, 2026-02-20: added userId field across 4 files | next: 2026-02-27 [L2]
- [~|reported] Context window and /compact usage
```

**Merge rules** (when `~/.claude/ramp/graphs/[topic].md` already exists):
- `version: 1` or `version: 2` files: read node names and statuses; treat all `[✓]` as `[✓|historical]`; upgrade to version: 3 format on write; leave review fields to `save_graph` (it fills a missing `| next:` on each `[✓]` node on write)
- Preserve any `[✓|*]` nodes from the old file that were not re-assessed in this session
- When merging, preserve existing evidence trails and review schedules — never overwrite a `[✓]` that has a trail/schedule with one that has none
- Update changed nodes; update the `updated` date
- Never overwrite `[✓]` with `[ ]` or `[~]` — only upgrade, never downgrade
- New nodes (not in old file) get their newly-inferred status

After writing, report the save: "Saved · [XP from save_graph's confirmation] XP. To sync to another machine: copy `~/.claude/ramp/graphs/`. To share with your team: use option **d**."

**For option d**, write `.claude/knowledge-graphs/[active-topic].md` in the current repo. This is the project-local tree — safe to commit, visible to teammates. It records only the `[✓]` nodes demonstrated in this session (a delta, not a full copy of your personal tree):

```markdown
---
version: 3
topic: [active-topic]
repo: [repo-name]
updated: [today's date YYYY-MM-DD]
---

# [Topic] Knowledge Graph — [repo-name]

*Project evidence log — nodes demonstrated in this codebase. Merges with personal tree on /ramp:up run.*

## Evidence

- [✓|TYPE] Node name — [repo-name], [YYYY-MM-DD]: [brief note] | next: [YYYY-MM-DD] [L1]
[... one line per [✓] node demonstrated in this session]
```

After writing: "Team tree saved at `.claude/knowledge-graphs/[active-topic].md`. Safe to commit — no personal data, just evidence of what was demonstrated here. Teammates' `/ramp:up` runs will pick it up automatically."

**For option e**, write `.claude/knowledge-graphs/local/[active-topic].md`. Same format as option `d` (delta of session `[✓]` nodes + personal notes), but stored in the local, gitignored path. Meant for personal project-specific observations not intended for teammates.

After writing: "Local tree saved at `.claude/knowledge-graphs/local/[active-topic].md`. Gitignored — only visible to you. Add it to your repo's `.gitignore` if not already there: `.claude/knowledge-graphs/local/`"

---

### Bootstrap offer (option c — conditional)

Option **c** is only included in the Phase 4 prompt if the env scan found genuine gaps: CLAUDE.md absent, settings.json absent, hooks absent, or custom slash commands absent. Do not offer to create things that already exist.

Construct the option **c** description specifically based on what's missing, e.g.: "Bootstrap missing Claude Code config: create a starter CLAUDE.md / add a settings.json with a PostToolUse linting hook / write a `/review-pr` command tailored to your workflow — immediately unlocks [specific nodes]"

If option **c** is selected:
1. For each missing item, write or edit the file using the appropriate tool
2. Before creating each file, say one sentence: what it is and why it matters
3. After creating all files, show the updated knowledge graph showing which foundation and advanced nodes flipped from `[ ]` → `[✓|artifact]`
4. Close with: "These aren't just config files — they're the foundation that makes the rest of the tree possible. Now [frontier node] is your real next move."

---

## The ./.ramp/ workspace

The per-repo session workspace — where the active lesson lives as *files*, not scrollback. Located at `[project_path]/.ramp/` where `project_path = realpath(git rev-parse --show-toplevel)`, else `realpath(cwd)`. Gitignored, regenerable, safe to delete — never commit it, and never store anything in it that can't be rebuilt from the graph + schema.

**The set is fixed at five files:** `worksheet.md`, `current.md`, `calibrate.md`, `scan.md`, `lessons.md`. Never create a sixth — new state belongs in one of these or in the knowledge graph, not in a new file. This section is the canonical format reference; every command that reads or writes a workspace file follows the definitions here.

### `.ramp/worksheet.md` — the active exercise

Exactly **one** task. The footer keeps the check-back protocol and the tangent escape hatch visible where the work is:

```markdown
# [Node title]
*Skill tree: [topic] · [✓] demonstrated · [~] self-reported · [ ] not yet*

**Goal:** [the node's mastery criterion, in plain words]

**Task:** [ONE concrete task — do a thing, or answer in your own words here]

> [space for the user's work / answer]

**Reference:** [source_url from the schema]

---
*Done? Say **done** (or run `/ramp:check`). Stuck or curious about something else? Say so —
we'll bookmark this and come back.*
```

### `.ramp/current.md` — you are here

The mode surface — makes "on task" visible. Rewritten whenever the active node changes:

```markdown
# Active lesson — [topic]
**You are here:** [branch] → "[node title]"  (node [N] of [M] in this branch)
**Right now:** [the one task, in one line].

**Navigate:** continue → say *done* · pause → `/ramp:pin` · side question → just ask · scan scope → `.ramp/scan.md`
```

### `.ramp/calibrate.md` — the placement worksheet

Written by `/ramp:calibrate` (the front door). Scan-detected rows arrive pre-filled `[✓]` with their evidence; the rest is the full node map for self-placement:

```markdown
# Place yourself — [topic] skill tree
Mark what you can already do. I'll verify the high-value ones; the rest seed your tree.
*[✓] I've done this (with evidence) · [~] I know this · [ ] not yet*

## Already detected on this machine  (the scan — see scan.md for scope)
- [✓] [node title] — [evidence one-liner]

## [Branch name]
- [ ] [node title]
- [ ] [node title]

## Explore next  (other skill trees — start with `/ramp:up <name>`)
- [topic] — [one-line description] ([N] nodes)

---
*Done? Say **done** — I'll record your claims and start you at the right place.*
```

### `.ramp/scan.md` — scan scope + findings

Directly answers "what did the scan look at, and what did it mark demonstrated":

```markdown
# What I looked at
**Scope:** this repo (`[project_path]`), `~/.claude/` config, your git history + Claude sessions.
**Not looked at:** other repos, anything outside this directory and your Claude config.

# What I found → marked demonstrated
- [node title] — [the evidence that triggered it]
```

### `.ramp/lessons.md` — lesson registry (stub)

One row per lesson. This slice only appends the active lesson's row and flips its status; the aside/resume flow that consumes the registry is deferred:

```markdown
# Lessons — [topic]
| id | title | status | origin | parent_session_id |
|----|-------|--------|--------|-------------------|
| 1 | [node title] | active | default | [CLAUDE_CODE_SESSION_ID] |
```

`status` = `active` | `done` · `origin` = `default` (picked by the engine) | `aside` (spun off a tangent) · `parent_session_id` = the `CLAUDE_CODE_SESSION_ID` of the session that created the lesson.

---

## Constraints

- Only reference files and tools that actually appeared in the auto-collected context
- Environmental signals take precedence over self-report for tree node status
- `[✓]` (demonstrated) outranks `[~]` (self-reported) — never treat them equivalently in frontier selection
- Never give advice not tied to their tree position, their goals, and what's actually in the repo
- Explorer tier: do not suggest hooks, custom MCP, or worktrees unless env signals show they're already there
- Practitioner tier: skip basics, go straight to a frontier node in Branch D or E
- Mode A: never lecture about Claude Code features without demonstrating them immediately through building
- Keep Phase 3 output scannable: tree first, then skill recommendations
- The knowledge graph's `[★]` node and the worksheet task must be the same item — exactly **one** active task at every tier
- ONBOARDING.md must be useful to a real new employee, not a session summary
- Phase 1 gap questions: ask at most 1 (returning user) or 3 (fresh start); never open-ended "what have you used?" — always specific and targeted
- Never re-teach a demonstrated node: no tips, mini-lessons, or exercises for anything the graph already marks `[✓]` — acknowledge it and build on it instead
- XP is always recomputed in code on write (by `save_graph`); never preserve a stale xp value from the old file
