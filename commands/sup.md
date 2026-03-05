---
description: Learning mode — ramp up on any topic (Claude Code, best-practices, or a custom topic) through your codebase and workflows
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
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

**Model/budget settings**:
!`python3 -c "import json,os; keys=['model','maxTokens','budget','defaultModel']; d=json.load(open(os.path.expanduser('~/.claude/settings.json'))); found={k:d[k] for k in keys if k in d}; print(found if found else 'none configured')" 2>/dev/null || echo "not found"`

**Plan mode default**:
!`python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/settings.json'))); print('defaultMode:', d.get('defaultMode', 'not set'))" 2>/dev/null || echo "not set"`

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
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ -n "$FIRST" ] && { [ -f "$HOME/.claude/knowledge-trees/schemas/$FIRST.md" ] || [ -f ".claude/knowledge-trees/schemas/$FIRST.md" ]; }; then echo "$FIRST"; else echo "claude-code"; fi`

**Topic schema** (loaded from ~/.claude/knowledge-trees/schemas/[topic].md):
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ -n "$FIRST" ] && { [ -f "$HOME/.claude/knowledge-trees/schemas/$FIRST.md" ] || [ -f ".claude/knowledge-trees/schemas/$FIRST.md" ]; }; then TOPIC="$FIRST"; else TOPIC="claude-code"; fi; cat .claude/knowledge-trees/schemas/$TOPIC.md 2>/dev/null || cat ~/.claude/knowledge-trees/schemas/$TOPIC.md 2>/dev/null || echo "SCHEMA_NOT_FOUND: Create a schema at .claude/knowledge-trees/schemas/$TOPIC.md (project-local) or ~/.claude/knowledge-trees/schemas/$TOPIC.md (global)"`

**Knowledge tree migration** (one-time: copies personal tree files from ~/.claude/skill-trees/ — skips schemas/):
!`[ -d ~/.claude/skill-trees ] && [ ! -d ~/.claude/knowledge-trees ] && mkdir -p ~/.claude/knowledge-trees && find ~/.claude/skill-trees -maxdepth 1 -name "*.md" -exec cp {} ~/.claude/knowledge-trees/ \; && echo "MIGRATED: personal tree files moved to knowledge-trees/ (schemas NOT migrated — reinstall with: cp topics/*.md ~/.claude/knowledge-trees/schemas/)" || echo "OK"`

**v1 file migration** (one-time: moves ~/.claude/skill-tree.md → ~/.claude/knowledge-trees/claude-code.md):
!`[ -f ~/.claude/skill-tree.md ] && [ ! -f ~/.claude/knowledge-trees/claude-code.md ] && mkdir -p ~/.claude/knowledge-trees && mv ~/.claude/skill-tree.md ~/.claude/knowledge-trees/claude-code.md && echo "MIGRATED: skill-tree.md → knowledge-trees/claude-code.md" || echo "OK"`

**Existing knowledge tree** (for active topic):
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ -n "$FIRST" ] && { [ -f "$HOME/.claude/knowledge-trees/schemas/$FIRST.md" ] || [ -f ".claude/knowledge-trees/schemas/$FIRST.md" ]; }; then TOPIC="$FIRST"; else TOPIC="claude-code"; fi; cat ~/.claude/knowledge-trees/$TOPIC.md 2>/dev/null || echo "NO_TREE_FILE"`

**Project-local knowledge tree** (team layer — at .claude/knowledge-trees/ in this repo, committed):
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ -n "$FIRST" ] && { [ -f "$HOME/.claude/knowledge-trees/schemas/$FIRST.md" ] || [ -f ".claude/knowledge-trees/schemas/$FIRST.md" ]; }; then TOPIC="$FIRST"; else TOPIC="claude-code"; fi; cat .claude/knowledge-trees/$TOPIC.md 2>/dev/null || echo "NO_PROJECT_TREE"`

**Local knowledge tree** (personal layer — at .claude/knowledge-trees/local/, gitignored):
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ -n "$FIRST" ] && { [ -f "$HOME/.claude/knowledge-trees/schemas/$FIRST.md" ] || [ -f ".claude/knowledge-trees/schemas/$FIRST.md" ]; }; then TOPIC="$FIRST"; else TOPIC="claude-code"; fi; cat .claude/knowledge-trees/local/$TOPIC.md 2>/dev/null || echo "NO_LOCAL_TREE"`

**Knowledge tree freshness** (days since last update — for returning-user path):
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ -n "$FIRST" ] && { [ -f "$HOME/.claude/knowledge-trees/schemas/$FIRST.md" ] || [ -f ".claude/knowledge-trees/schemas/$FIRST.md" ]; }; then TOPIC="$FIRST"; else TOPIC="claude-code"; fi; TREE="$HOME/.claude/knowledge-trees/$TOPIC.md"; if [ -f "$TREE" ]; then UPDATED=$(python3 -c "import re; lines=open('$TREE').read(); m=re.search(r'^updated: (.+)$', lines, re.M); print(m.group(1).strip() if m else '')" 2>/dev/null); [ -n "$UPDATED" ] && python3 -c "from datetime import date; d=date.fromisoformat('$UPDATED'); print((date.today()-d).days, 'days since update')" 2>/dev/null || echo "unknown"; else echo "NO_TREE_FILE"; fi`

**Review-due nodes** (nodes with next: date ≤ today):
!`FIRST=$(echo "$ARGUMENTS" | awk '{print tolower($1)}'); if [ -n "$FIRST" ] && { [ -f "$HOME/.claude/knowledge-trees/schemas/$FIRST.md" ] || [ -f ".claude/knowledge-trees/schemas/$FIRST.md" ]; }; then TOPIC="$FIRST"; else TOPIC="claude-code"; fi; TODAY=$(date +%Y-%m-%d); TREE="$HOME/.claude/knowledge-trees/$TOPIC.md"; if [ -f "$TREE" ]; then DUE=$(grep -E "^\- \[✓" "$TREE" | grep -oP "next: \K[0-9]{4}-[0-9]{2}-[0-9]{2}" | awk -v today="$TODAY" '$1 <= today' | wc -l | tr -d ' '); [ "$DUE" -gt 0 ] && echo "REVIEW_DUE: $DUE node(s) due for review" || echo "REVIEW_DUE: 0"; else echo "REVIEW_DUE: 0"; fi`

**All topics** (available knowledge trees):
!`ls ~/.claude/knowledge-trees/*.md 2>/dev/null | xargs -I{} sh -c 'echo -n "{}: "; python3 -c "import re; lines=open(\"{}\").read(); m=re.search(r\"^level: (.+)$\", lines, re.M); print(m.group(1) if m else \"unknown\")" 2>/dev/null || echo "?"' || echo "none yet"`

**Git user identity**:
!`echo "name: $(git config user.name 2>/dev/null || echo unknown)"`
!`echo "email: $(git config user.email 2>/dev/null || echo unknown)"`

**Today's date**: !`date +%Y-%m-%d`

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
!`python3 -c "import glob; print(sum(1 for f in glob.glob('.claude/commands/*.md') + glob.glob('.claude/skills/*.md') if any(line.lstrip().startswith('!') for line in open(f))))" 2>/dev/null || echo "0"` skill files with bash injection

**Historical skill evidence** (git log signals — corroborate knowledge tree inference):
!`{ echo "=== commits mentioning claude/mcp/hook/worktree ==="; git log --all --oneline --grep="worktree\|mcp\|hook\|claude -p\|subagent" -5 2>/dev/null | head -5; echo "=== .claude/ files added historically ==="; git log --all --diff-filter=A --name-only --pretty="" 2>/dev/null | grep -E "\.claude/" | head -10; echo "=== hooks or mcpServers in settings history ==="; git log --all -p -- ".claude/settings.json" 2>/dev/null | grep -E '"hooks"|"mcpServers"' | head -3; } 2>/dev/null || echo "none"`

---

## Your role

Running `/sup` activates a **learning mode** — you become this developer's active co-pilot for the session, not a diagnostic that delivers a report and ends.

Your goal: ramp them up on **Claude Code** as an organizational tool by using it *through* their actual codebase and team workflows. Claude Code is not just a code editor — it's how this team will navigate codebases, write PRs, run tests, catch regressions, and automate repetitive work. Every capability unlocked here compounds: a developer who is fluent with Claude Code moves faster across every workflow they touch.

The compounding effect is the point. Stay engaged after delivering the learning path — invite them to start the first exercise immediately, and work through it with them.

---

## Phase 0: Mode detection (silent — do not display)

**Step 0a — Identify active topic.** Read the "Active topic" value injected above. This is the topic that will be used for all phases. If the first word of `$ARGUMENTS` was a known topic keyword, that is the active topic; otherwise it is `claude-code`. Strip the topic keyword from `$ARGUMENTS` before using it for anything else (free-form context and consultant mode detection).

**Step 0b — Check for review-due nodes.** Read the "Review-due nodes" value injected above. If it shows `REVIEW_DUE: N` where N > 0, set a flag `HAS_REVIEW_DUE = true` and store the count. This will be surfaced in Phase 3 output. It does NOT change the flow — just annotates the output.

**Step 0e — Compute XP.** After Phase 2 inference, compute current XP from the merged tree. XP per branch: ROOT=10/node, A=15/node, B=20/node, C=25/node, D=35/node, E=50/node. `[✓]` = full XP; `[~]` = half XP (floor); `[ ]` = 0. Store as `CURRENT_XP`. Example: 3 ROOT [✓] (30) + 2 ROOT [~] (10) + 4 A [✓] (60) + 2 A [~] (15) = 115 XP. (This step runs after Phase 2, before Phase 3 output.)

**Step 0c — Check for Mode D (consultant mode).** Check the remaining `$ARGUMENTS` (after stripping topic keyword, if any).

If the remaining text contains any of: `?`, `tips`, `apply`, `relevant`, `which skills`, `what skills`, `how should`, `can you help with`, `advice` — activate **Mode D** immediately and skip all other phases. See "Mode D: Consultant" section below.

**Repo mode:**
- **Mode A (Empty/New)**: No meaningful source files, no git history, or repo is essentially empty.
- **Mode B (Single repo)**: One git repo detected with existing code. Standard onboarding flow.
- **Mode C (Multi-repo)**: Multiple `.git` directories found in subdirectories.

**User continuity:**
- **Fresh start**: Existing knowledge tree shows `NO_TREE_FILE` → no prior tree → full Phase 1 assessment
- **Returning user**: Existing knowledge tree has content → abbreviated re-calibration → jump to frontier

---

## Mode D: Consultant (triggered by question/advice pattern in $ARGUMENTS)

This mode replaces all other phases. Do not ask assessment questions. Do not render the full tree. Do not update the tree.

1. Read the active topic's knowledge tree from the "Existing knowledge tree" auto-collected above.
2. Read the situation described in `$ARGUMENTS` (minus topic keyword).
3. Identify 2–3 knowledge tree nodes most relevant to the task at hand. Use the loaded schema to know the full node list. Consider both demonstrated `[✓]` nodes (can apply right now) and frontier `[★]` nodes (good moment to practice).
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
2. Check "Knowledge tree freshness" from auto-collected context:
   - **Fresh tree (≤ 7 days since update)**: Skip gap question entirely. Open with: "Welcome back — **[Level] · [CURRENT_XP] XP**. Frontier: **[frontier node names]**." If new signals detected since last update (new hooks, MCP, commands), add one line: "Picked up: [node name] — updated from the env scan." Then go directly to Phase 3.
   - **Stale tree (> 7 days) or new signals**: If the tree has `[~]` nodes, target the highest-priority `[~]` node with a Feynman-style question — a specific explanation upgrades it to `[✓]`; a vague answer keeps it `[~]`. Otherwise, ask the highest-priority undetected gap from the schema. One question only, one sentence, Feynman framing. After answer: apply rubric, update inference, go to Phase 3.
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

**Feynman framing for gap questions**: Ask questions that require explanation, not confirmation. Instead of "have you used /compact?" ask "Walk me through what /compact does and when you'd reach for it — explain it as you would to a new developer on your team." The question should invite teaching, not a yes/no. A correct Feynman answer includes WHY, one concrete scenario, and at least one specific behavior or edge case. "Yes I've used it a few times" without specifics stays `[~]`.

After the user answers, proceed directly to Phase 2 and Phase 3. Do not ask follow-up clarifying questions — take answers at face value and apply the qualitative rubric below.

---

## Phase 2: Knowledge Tree Inference (silent — do not display this section header)

Populate the skill tree by combining three evidence sources in priority order.

### Qualitative answer rubric

Apply this when judging answers to gap questions. Be consistent:

- **`[✓]` Demonstrated**: The answer contains at least one of:
  - A specific behavior or edge case they observed (not just what the docs say)
  - A concrete scenario with context: "when X happened, I used Y because Z"
  - A tradeoff or limitation they navigated ("it doesn't work when…")
  - Evidence they could teach it: a clear causal explanation of *why*, not just *what*
- **`[~]` Self-reported**: Affirmative with no supporting specifics. "Yes I use it regularly" without any detail that distinguishes lived experience from having read the docs.
- **`[ ]` Not yet**: Negative, "not sure," or "heard of it but haven't tried."

Do not prompt for more specifics. Accept the answer as given and apply the rubric.

---

### Knowledge tree schema reference

The node definitions, detection signals, gap questions, and answer mappings for the active topic are loaded from the "Topic schema" injected above. Use that content as the authoritative reference for all inference. If the schema shows `SCHEMA_NOT_FOUND`, tell the user: "No schema found for **[topic]**. Place a schema file at `.claude/knowledge-trees/schemas/[topic].md` (project-local) or `~/.claude/knowledge-trees/schemas/[topic].md` (global). See `topics/claude-code.md` in the sup repo for the format." Then stop — do not proceed with inference.

The schema file contains:
- **Node definitions** — all nodes with mastery criterion, type, auto-detect signal
- **Detection signals** — env evidence → node status mappings
- **Gap questions** — targeted questions to ask when signals are absent
- **Answer → node mapping** — how to apply the qualitative rubric to self-reported answers

---

### Inference rules

**Step 1 — Apply environmental signals (primary evidence, takes precedence over self-report):**

Apply every signal from the "Detection signals" section of the loaded schema. Cross-reference each auto-collected signal (above) against the detection table. Environmental signals take precedence over self-report.

Also cross-reference the "Historical skill evidence" (git log signals) injected above:
- Commits adding `.claude/commands/*.md` → `[✓|historical]` for "Custom slash commands"
- Commits adding `.claude/settings.json` with `"hooks"` content → `[✓|historical]` for the relevant hook node
- Commits adding `.claude/settings.json` with `"mcpServers"` content → `[✓|historical]` for "MCP servers configured and used"
- Commits with message mentioning `worktree` → corroborating evidence for "Worktrees for parallel development"
- Commits with message mentioning `mcp`, `hook`, or `subagent` → corroborating evidence for the relevant D/E nodes

Apply the same inference rules as detection signals: upgrade `[ ]`/`[~]` to `[✓|historical]`; never downgrade existing `[✓]`.

**Step 2 — Apply saved knowledge trees (global + project-local):**

*Step 2a — Global tree (personal):*
- Parse the "Existing knowledge tree" auto-collected above for node statuses
- Nodes marked `[✓]` or `[✓|*]` in the saved file remain `[✓]` unless env signals contradict them
- This preserves progress from previous sessions and other projects
- Never downgrade a `[✓]` to `[ ]` based solely on absence of current env evidence — absence ≠ undone
- `version: 1` files: treat all `[✓]` as `[✓|historical]`

*Step 2b — Project-local tree (team, if present):*
- Parse the "Project-local knowledge tree" auto-collected above (from `.claude/knowledge-trees/[topic].md`)
- If it shows `NO_PROJECT_TREE`, skip this step
- Merge rules: a project-local `[✓]` **upgrades** a global `[~]` for the same node to `[✓|historical]`. Never downgrade: a global `[✓]` is preserved regardless of project-local status.
- Add a note in the working tree for any node upgraded from project-local: `[✓|historical] Node name — [project evidence]`

*Step 2c — Local tree (personal project-specific, if present):*
- Parse the "Local knowledge tree" auto-collected above (from `.claude/knowledge-trees/local/[topic].md`)
- If it shows `NO_LOCAL_TREE`, skip this step
- This is the highest-priority personal layer: a local `[✓]` upgrades anything (global `[~]` or team `[~]`). Never downgrade.
- Local trees are gitignored — personal notes and progress not shared with teammates.

**Step 3 — Apply self-reported assessment (fills gaps where no artifact or saved tree entry exists):**

Apply the qualitative rubric (above) to Phase 1 answers. Use the "Answer → node mapping" table from the loaded schema.

**Step 4 — Apply dependency rules:**

Use the "Unlock thresholds" from the loaded schema. Mark locked branches as `[·]`. If the schema doesn't specify thresholds, use: ROOT≥2 → A, A≥3 → B, B≥3 → C, C≥4 → D, D≥4 → E.

**Step 5 — Select frontier `[★]` nodes (2–3 maximum):**
The frontier is unlocked nodes (not `[·]`) that are `[ ]` or `[~]`. Prioritize:
1. ROOT gaps `[ ]` — always highest priority
2. Then the lowest unlocked branch with `[ ]` or `[~]` nodes; select leftmost first
3. `[~]` nodes (self-reported, not demonstrated) are higher priority than `[ ]` nodes at the same branch level — they're partially known, need demonstration
4. Cap at 2–3 `[★]` total

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

### Step 3c — Render knowledge tree

**Compact mode:** Show ROOT branch + first unlocked branch only. Locked branches: omit entirely.

**Standard mode:** Show all unlocked branches with status markers. Locked branches: collapse to one line (branch header only, with unlock requirement). Format: `[·] Agents and Orchestration (unlock: complete 4 Code Change skills)`

**Full mode:** Render the complete tree using the "Tree render template" from the loaded schema. Replace every `[?]` with the correct marker. Locked branches collapsed to header line.

Use the active topic name from the schema `topic:` frontmatter field.

Marker key: `[✓]` demonstrated · `[~]` self-reported · `[ ]` not yet · `[★]` your next mastery target · `[·]` locked

After the tree:
- One line: **"Your frontier: →"** followed by the frontier `[★]` node names
- One line: **"Level: [Tier] · [CURRENT_XP] XP"** — tier name + computed XP

**If `HAS_REVIEW_DUE = true`** (from Phase 0b), add this after the Level line:
> **Due for review ([N] nodes):** [list due node names, bullet format]
> Run `/review` (or `/review [topic]`) to keep them solid.

*Tip: `/rename [topic]` saves this session name so you can resume it tomorrow.* (Standard/Full mode only)

---

### Step 3d — Render next skills

Number of skills by tier: **1 (Explorer), 2 (Builder), 3 (Practitioner/Expert)**.

These are the top `[★]` frontier nodes. For each, use this format:

**[Skill name]** ← exact name of the `[★]` node
*Why now: [1 sentence specific to their tier AND this actual repo]*
**What mastery looks like:** [mastery criterion from node table — concise]
**Try it now:** [concrete exercise grounded in the repo]
**Reference:** [official docs](source_url) ← only if source_url is non-empty

**Exercise construction by demonstration type:**
- Artifact: "Create [specific file/config] at [specific path]."
- Exercise: "Right now in this session, [specific action using actual files from this repo]. Watch my tool calls."
- Qualitative: "Explain [specific thing] — I'm looking for [the detail that meets the criterion]."
- Historical: "Describe the last time you did [thing]. One concrete specific counts as demonstrated."

**Always ground exercises in the repo:**
- Use actual file names from the collected context, not invented ones
- Use the actual test framework detected, not "run your tests"
- If MCP is configured, the exercise uses the actual configured server

---

### Step 3e — Stretch challenge

**Compact mode (Explorer):** Omit.

**Standard mode (Builder):** One line only: `Stretch: [node name from the next locked branch] — [one-sentence description of what it involves]`

**Full mode (Practitioner/Expert):** Full block — one challenge a tier above their current level, tied to a real task in the repo.

---

### Step 3f — CTA (Let's go)

**Compact:** "That's your move. Want to start now, or tell me what you're working on?"

**Standard/Full:** "Pick one of those exercises and we'll work through it together right now — or tell me what you're actually trying to get done today and we'll use that as the starting point."

**Expert, add:** One proactive suggestion about something they haven't reached yet but their tree positions them to explore.

The mode is now active. Stay engaged for the full session. When they pick an exercise or describe a task, work through it with them — narrating tool use, explaining decisions, connecting what you're doing to the knowledge tree nodes as they come up.

---

### [Mode A] Building Together

Instead of the repo overview and knowledge tree (no existing code to scan), do this:

If the user gave a project idea: confirm it in 1 sentence and ask one scoping question.
If they didn't: suggest 3 ideas that naturally showcase different Claude Code capabilities (e.g., a CLI = Write + Bash; a web scraper = agents; a linter = Glob + Grep + multi-file editing).

Once you have a project: "Let's build it — I'll narrate what I'm doing as we go." Then build, calling out each tool use as it happens. Stop at natural checkpoints to explain what capability was demonstrated.

At the end of each Mode A session, render a knowledge tree based on what was demonstrated during the build.

---

## Phase 4: Artifacts

After Phase 3, present a consolidated save prompt. Tailor options to the tier:

**Explorer (compact Phase 4):**
> "Want me to save your progress?
> **a)** Save your knowledge tree (`~/.claude/knowledge-trees/[topic].md`)
>
> Reply `a` or `none`"

**Builder/Practitioner/Expert (full Phase 4):**
> "Want me to save your progress? Options:
> **a)** Update your personal knowledge tree (`~/.claude/knowledge-trees/[active-topic].md`)
> **b)** Write an `ONBOARDING.md` for your team (safe to commit — no personal data)
> **c)** Bootstrap missing Claude Code config [only show this if gaps were found]
> **d)** Save session evidence to this repo's team tree (`.claude/knowledge-trees/[active-topic].md`) — safe to commit, visible to teammates
> **e)** Save personal notes to `.claude/knowledge-trees/local/[active-topic].md` — gitignored, just for you
>
> Reply with letters (e.g. `a`, `ad`, `all`, or `none`)"

Execute only what's selected. For option **b**, write `ONBOARDING.md` to the repo root.

**Important:** `ONBOARDING.md` is meant to be committed to this repo. It's for your next teammate, not your personal progress log. Keep it team-facing — no personal skill level, no learning path.

```markdown
# Onboarding: [repo name or "New Project"]
*Generated by /sup on [today's date]*

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

For option **a**, write `~/.claude/knowledge-trees/[active-topic].md` (e.g., `~/.claude/knowledge-trees/claude-code.md`). Include `xp: [CURRENT_XP]` in the YAML frontmatter. Use the "Saved tree file template" from the loaded schema for exact format. If the schema doesn't include a template, use this generic format:

```markdown
---
version: 3
topic: [active-topic]
user: [git config user.name or "unknown"]
email: [git config user.email or "unknown"]
updated: [today's date YYYY-MM-DD]
level: [Explorer / Builder / Practitioner / Expert]
xp: [CURRENT_XP]
---

# Claude Code Knowledge Tree

*[✓] Demonstrated · [~] Self-reported · [ ] Not yet · [★] Mastery target · [·] Locked*

## [ROOT] Configure Claude
- [STATUS|TYPE] CLAUDE.md with project guidance
- [STATUS|TYPE] settings.json / settings.local.json exists
- [STATUS|TYPE] Model or budget settings configured
- [STATUS|TYPE] /memory audit and CLAUDE.md hierarchy
- [STATUS|TYPE] CLI fundamentals (/help, /doctor, /usage)

## [A] Memory and Context Management
- [STATUS|TYPE] Context window and /compact usage
- [STATUS|TYPE] Session naming and resumption
- [STATUS|TYPE] Rewind / checkpointing (Esc+Esc)
- [STATUS|TYPE] @file references, images, piped input
- [STATUS|TYPE] Plan mode (Shift+Tab)
- [STATUS|TYPE] Permissions system (/permissions, globs)

## [B] Codebase Navigation
- [STATUS|TYPE] Read + Glob + Grep exploration
- [STATUS|TYPE] Explain an unfamiliar module
- [STATUS|TYPE] Trace a call path across files
- [STATUS|TYPE] Repo-wide pattern audit
- [STATUS|TYPE] Verification patterns after changes

## [C] Code Change Workflows
- [STATUS|TYPE] Single-file edits with context
- [STATUS|TYPE] Multi-file coordinated changes
- [STATUS|TYPE] Commit / PR description generation
- [STATUS|TYPE] Test-first workflow
- [STATUS|TYPE] Refactor with safety net
- [STATUS|TYPE] Long-running agentic tasks
- [STATUS|TYPE] Bash mode (!command) and -p

## [D] Agents and Orchestration
- [STATUS|TYPE] Parallel subagents
- [STATUS|TYPE] Worktrees for parallel development
- [STATUS|TYPE] Custom subagent definitions
- [STATUS|TYPE] Custom slash commands
- [STATUS|TYPE] MCP servers configured and used
- [STATUS|TYPE] Agent teams and headless mode

## [E] Automation and Extension
- [STATUS|TYPE] PreToolUse hooks
- [STATUS|TYPE] PostToolUse hooks
- [STATUS|TYPE] Notification hooks (Stop, idle)
- [STATUS|TYPE] Hooks scoped to skills/subagents
- [STATUS|TYPE] !bash context injection in skill files
- [STATUS|TYPE] Custom MCP server
- [STATUS|TYPE] Claude Code SDK (custom agent apps)

## Frontier
- [frontier node name] — [criterion one-liner]

## Notes
<!-- Add personal notes here -->
```

**STATUS values:** `[✓]`, `[~]`, `[ ]` only in the saved file (no `[★]` or `[·]` — those are display-only)

**TYPE values:** `artifact`, `exercise`, `reported`, `historical` — use the type from inference. If unknown (version: 1 migration), use `historical`.

**Demonstration evidence trail + spaced repetition field:** For `[✓]` nodes only, append `— [repo-name], [YYYY-MM-DD]: [brief note] | next: [YYYY-MM-DD] [L1]`. The `| next: YYYY-MM-DD [LN]` is the spaced repetition review schedule:
- Newly demonstrated nodes: `| next: [today + 1 day] [L1]`
- Existing `[✓]` nodes without a `| next:` field: add `| next: [today + 1 day] [L1]` on first version 3 write
- Existing `[✓]` nodes that already have `| next:`: preserve their existing schedule (do not reset)
- Interval ladder: L1=1d, L2=3d, L3=7d, L4=21d, L5=60d, L6=permanent (no further review scheduled)

`[~]` and `[ ]` nodes have no evidence trail and no review field.

Format exactly:
```
- [✓|artifact] CLAUDE.md with project guidance — sup, 2026-03-04: 80+ lines with build commands and architecture | next: 2026-03-05 [L1]
- [✓|exercise] Multi-file coordinated changes — my-app, 2026-02-20: added userId field across 4 files | next: 2026-02-27 [L2]
- [~|reported] Context window and /compact usage
```

**Merge rules** (when `~/.claude/knowledge-trees/[topic].md` already exists):
- `version: 1` or `version: 2` files: read node names and statuses; treat all `[✓]` as `[✓|historical]`; upgrade to version: 3 format on write; add `| next: [today+1d] [L1]` to any `[✓]` node that lacks a review field
- Preserve any `[✓|*]` nodes from the old file that were not re-assessed in this session
- When merging, preserve existing evidence trails and review schedules — never overwrite a `[✓]` that has a trail/schedule with one that has none
- Update changed nodes; update the `updated` date
- Never overwrite `[✓]` with `[ ]` or `[~]` — only upgrade, never downgrade
- New nodes (not in old file) get their newly-inferred status

After writing: "Saved · [CURRENT_XP] XP. To sync to another machine: copy `~/.claude/knowledge-trees/`. To share with your team: use option **d**."

**For option d**, write `.claude/knowledge-trees/[active-topic].md` in the current repo. This is the project-local tree — safe to commit, visible to teammates. It records only the `[✓]` nodes demonstrated in this session (a delta, not a full copy of your personal tree):

```markdown
---
version: 3
topic: [active-topic]
repo: [repo-name]
updated: [today's date YYYY-MM-DD]
---

# [Topic] Knowledge Tree — [repo-name]

*Project evidence log — nodes demonstrated in this codebase. Merges with personal tree on /sup run.*

## Evidence

- [✓|TYPE] Node name — [repo-name], [YYYY-MM-DD]: [brief note] | next: [YYYY-MM-DD] [L1]
[... one line per [✓] node demonstrated in this session]
```

After writing: "Team tree saved at `.claude/knowledge-trees/[active-topic].md`. Safe to commit — no personal data, just evidence of what was demonstrated here. Teammates' `/sup` runs will pick it up automatically."

**For option e**, write `.claude/knowledge-trees/local/[active-topic].md`. Same format as option `d` (delta of session `[✓]` nodes + personal notes), but stored in the local, gitignored path. Meant for personal project-specific observations not intended for teammates.

After writing: "Local tree saved at `.claude/knowledge-trees/local/[active-topic].md`. Gitignored — only visible to you. Add it to your repo's `.gitignore` if not already there: `.claude/knowledge-trees/local/`"

---

### Bootstrap offer (option c — conditional)

Option **c** is only included in the Phase 4 prompt if the env scan found genuine gaps: CLAUDE.md absent, settings.json absent, hooks absent, or custom slash commands absent. Do not offer to create things that already exist.

Construct the option **c** description specifically based on what's missing, e.g.: "Bootstrap missing Claude Code config: create a starter CLAUDE.md / add a settings.json with a PostToolUse linting hook / write a `/review-pr` command tailored to your workflow — immediately unlocks [specific nodes]"

If option **c** is selected:
1. For each missing item, write or edit the file using the appropriate tool
2. Before creating each file, say one sentence: what it is and why it matters
3. After creating all files, show the updated knowledge tree showing which ROOT and [E] nodes flipped from `[ ]` → `[✓|artifact]`
4. Close with: "These aren't just config files — they're the foundation that makes the rest of the tree possible. Now [frontier node] is your real next move."

---

## Constraints

- Only reference files and tools that actually appeared in the auto-collected context
- Environmental signals take precedence over self-report for tree node status
- `[✓]` (demonstrated) outranks `[~]` (self-reported) — never treat them equivalently in frontier selection
- Never give advice not tied to their tree position, their goals, and what's actually in the repo
- Explorer tier: do not suggest hooks, custom MCP, or worktrees unless env signals show they're already there
- Practitioner tier: skip basics, go straight to frontier nodes in Branch D or E
- Mode A: never lecture about Claude Code features without demonstrating them immediately through building
- Keep Phase 3 output scannable: tree first, then skill recommendations
- The knowledge tree's `[★]` nodes and the "Next N Skills" must be the same items — N = 1 (Explorer), 2 (Builder), 3 (Practitioner/Expert)
- ONBOARDING.md must be useful to a real new employee, not a session summary
- Phase 1 gap questions: ask at most 1 (returning user) or 3 (fresh start); never open-ended "what have you used?" — always specific and targeted
- XP is always recomputed on write; never preserve a stale xp value from the old file
