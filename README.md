# sup

Claude Code adoption stalls for a predictable reason: the documentation is complete, but it doesn't adapt to *you* — your codebase, your current level, what you've already demonstrated. Most developers plateau at basic edits and multi-file changes. Hooks, worktrees, custom agents, MCP servers, and pipeline integration remain unexplored. The capability gap compounds.

`/sup` solves this. Run it in any repo. It scans your environment — not just the codebase, but your Claude Code configuration, git history, session history, and prior progress. It asks at most 2–3 targeted questions about things that can't be detected. Then it delivers a personalized, repo-grounded learning path and stays engaged as your co-pilot for the session.

It's not a report. It's a mode.

---

## Design principles

These aren't just implementation details — they're the reason it works.

**Detect before interrogating.** Over 80 shell commands run at invocation to collect environmental signals: CLAUDE.md content, hook configurations, MCP servers, git worktree count, session transcript count, subagent usage, headless invocations in scripts. By the time you see your first question, `/sup` has already determined your level, identified your demonstrated skills, and selected the gaps worth asking about. You answer at most 3 questions. They're specific.

**Demonstrated over claimed.** The knowledge tree distinguishes `[✓]` (demonstrated) from `[~]` (self-reported). A hook in your settings.json is `[✓|artifact]`. Saying "yes I've used hooks" is `[~|reported]`. Both count toward branch unlock, but the rubric is explicit: a `[✓]` requires at least one specific verifiable detail that only someone who has done it would know — a flag, an observed behavior, a tradeoff navigated. Vague affirmations stay `[~]`. This matters: the difference between "I've heard of hooks" and "I have a PostToolUse hook that fires my linter" is the entire gap between knowledge and practice.

**Mastery missions, not checklists.** Every node in the knowledge tree has a mastery criterion and a repo-grounded exercise. The criterion is falsifiable. The exercise is grounded in what actually exists in this repo — real file names, your actual test framework, your configured MCP servers. There's no generic "run your tests." It's "run `pytest tests/` on `auth_service.py` and interpret the failures."

**Dependency-gated progression.** You don't reach Agents until you've demonstrated Code Changes. You don't reach Automation until you've demonstrated Agents. This isn't gatekeeping — it's sequencing. A developer who hasn't traced a call path across files or verified a refactor with tests isn't ready for parallel subagent coordination. The gates are the pedagogy.

**Session-persistent, topic-namespaced.** Your knowledge trees live at `~/.claude/knowledge-trees/[topic].md`. They follow you across every repo. Returning users with a fresh tree (updated within 7 days) go straight to Phase 3 — no gap questions, no friction. Running it in a new codebase imports your prior level as the starting point. Progress is never lost.

**Adaptive pacing.** Output length and depth scale with your level. Explorer = 1 skill exercise, compact tree, ~25 lines. Builder = 2 exercises, pruned tree, ~55 lines. Practitioner/Expert = full output, full tree, 3 exercises. The format matches your readiness.

**XP and progress tracking.** Each demonstrated `[✓]` node earns XP by branch (ROOT=10, A=15, B=20, C=25, D=35, E=50). `/sup` shows "Level: Builder · 240 XP". `/review` awards XP on pass. The number is a real reflection of what you've proven — not clicks.

**Three-layer trees mirroring Claude Code's scope model.** Your personal tree (`~/.claude/knowledge-trees/`) follows you everywhere (user scope). A project team tree (`.claude/knowledge-trees/`, committable) tracks what's been demonstrated in a specific codebase (project scope). A local tree (`.claude/knowledge-trees/local/`, gitignored) holds personal project-specific notes you don't want to share (local scope). `/sup` reads and merges all three — higher layers upgrade lower ones, never downgrade. Phase 4 options `a`/`d`/`e` write to each layer.

**Spaced repetition.** Demonstrated `[✓]` nodes don't just sit there — they're scheduled for review. Each node carries a `| next: YYYY-MM-DD [LN]` field using a 6-level interval ladder (1d → 3d → 7d → 21d → 60d → permanent). `/sup` surfaces due nodes alongside your frontier. `/review` runs a focused review session. Pass = advance a level + XP. Fail = reset to L1.

**Engine/curriculum separation.** `/sup` is a topic-agnostic learning engine. The curriculum — nodes, detection signals, gap questions, mastery criteria, doc links — lives in standalone schema files (`topics/`). Adding a new topic means writing one schema file. The engine doesn't change.

---

## Topics

| Topic | Command | Nodes | Focus |
|-------|---------|-------|-------|
| `claude-code` (default) | `/sup` | 36 | Claude Code features: navigation, code changes, agents, automation |
| `best-practices` | `/sup best-practices` | 15 | CLAUDE.md design, configuration patterns, session hygiene |
| `mcp-development` | `/sup mcp-development` | 20 | Building MCP servers: tools, resources, prompts, distribution |
| `anthropic-api` | `/sup anthropic-api` | 18 | Claude API: completions, tool use, agentic loops, production patterns |
| *(your topic)* | `/sup [topic]` | any | Install your schema → it works |

Future topics planned (not yet built): `bash`, `react`, `typescript`, `dsa`, `git`.

---

## Three modes

| Context | What happens |
|---------|-------------|
| **Existing repo** | Scans codebase + env + history → renders knowledge tree → delivers mastery missions → stays engaged as session co-pilot |
| **Empty/new repo** | Asks what to build → builds it with you → narrates every Claude Code capability as it's used → renders knowledge tree from what was demonstrated |
| **Directory of repos** | Surveys all repos (name, stack, last activity) → you pick focus → proceeds as single-repo mode |

---

## The knowledge tree (claude-code topic)

36 nodes across 6 branches. Every node grounded in Claude Code's actual feature surface.

```
[ROOT] Configure Claude
    [✓] CLAUDE.md with project guidance
    [✓] settings.json / settings.local.json exists
    [~] Model or budget settings configured
    [★] /memory audit and CLAUDE.md hierarchy
    [ ] CLI fundamentals (/help, /doctor, /usage)

[~] Memory and Context Management
    [★] Context window and /compact usage
    [ ] Session naming and resumption
    [ ] Rewind / checkpointing (Esc+Esc)
    [✓] @file references, images, piped input
    [✓] Plan mode (Shift+Tab)
    [~] Permissions system (/permissions, globs)

[✓] Codebase Navigation
    [✓] Read + Glob + Grep exploration
    [✓] Explain an unfamiliar module
    [~] Trace a call path across files
    [ ] Repo-wide pattern audit
    [ ] Verification patterns after changes

[~] Code Change Workflows
    [✓] Single-file edits with context
    [★] Multi-file coordinated changes
    [ ] Commit / PR description generation
    [ ] Test-first workflow
    [ ] Refactor with safety net
    [ ] Long-running agentic tasks
    [ ] Bash mode (!command) and -p

[·] Agents and Orchestration   (unlock: complete 4 Code Change skills)
[·] Automation and Extension   (unlock: complete 4 Agents skills)

Your frontier: → /memory audit [★]  → /compact usage [★]  → Multi-file changes [★]
Level: Builder — solid navigation, ready to go deeper on changes and context management
```

Marker key: `[✓]` demonstrated · `[~]` self-reported · `[ ]` not yet · `[★]` mastery target · `[·]` locked

Each `[★]` node becomes a **mastery mission**:

```
[Multi-file coordinated changes]
Why now: You're working in a Node/TypeScript repo with clear module boundaries — the ideal
  structure for practicing changes that span interfaces, implementations, and tests together.
What mastery looks like: A change requiring ≥3 files edited consistently; Claude maintains
  naming and style conventions across all of them without being corrected.
Try it now: Ask me to add a `userId` field to the User type in this repo. Watch which
  files I touch, in what order, and whether I catch the downstream effects without prompting.
Reference: official docs (https://docs.anthropic.com/en/docs/claude-code/common-tasks)
```

---

## Company deployment

### Two tools, two purposes

| | ONBOARDING.md | Custom topic schema |
|--|---|---|
| **Format** | Static markdown doc | Active knowledge tree session |
| **When used** | Day 1: "how do I run this?" | First week: guided onboarding with exercises |
| **Personalized?** | No — same doc for everyone | Yes — starts from what the dev already knows |
| **Progress tracking** | No | Yes — evidence trails, XP, spaced repetition |
| **Generated by** | `/sup` Phase 4 option b | `/sup [your-topic]` |
| **Committed to repo?** | Yes (optional) | Schema yes; knowledge trees are personal |

Use both: ONBOARDING.md for the quick-start reference, a custom topic for the active ramp-up.

### Step 1: Commit the commands

Copy command files to your team repo's `.claude/commands/`:

```bash
cp commands/sup.md     /your-team-repo/.claude/commands/sup.md
cp commands/tree.md    /your-team-repo/.claude/commands/tree.md
cp commands/review.md  /your-team-repo/.claude/commands/review.md
```

Engineers get the commands on clone. Knowledge trees (`~/.claude/knowledge-trees/`) remain personal — they live on each developer's machine, not in the repo.

### Step 2: Create a custom topic schema (optional but recommended)

Create `.claude/knowledge-trees/schemas/[your-topic].md` in the team repo. This is the curriculum for onboarding to THIS codebase — nodes, detection signals, gap questions, and mastery criteria specific to your project.

```
.claude/
└── knowledge-trees/
    └── schemas/
        └── acme-onboarding.md   ← commit this
```

Example node structure:

```
[ROOT] Environment setup
  - make setup completes without errors
  - .env configured and local server runs
  - Can explain what each required env var does

[A] Architecture
  - Read docs/architecture.md and can explain the data flow
  - Knows which service owns auth vs. data pipeline
  - Can locate the entry point for a new API request

[B] Development workflow
  - Created a test PR through the full review process
  - Ran the test suite and interpreted a failure
  - Understands the deploy process (staging → prod)

[C] Team practices
  - Knows the 30-minute rule and how to use #dev-help
  - Can explain the monitoring setup and how to read dashboards
```

See `topics/claude-code.md` for the full schema format (node definitions, detection signals, gap questions, mastery criteria, doc links).

When committed to `.claude/knowledge-trees/schemas/`, the schema is available immediately — no separate install step. Engineers clone the repo and run:

```
/sup acme-onboarding
```

They get a personalized onboarding session grounded in the actual repo, with exercises using real file names and real workflows, evidence tracking, and spaced repetition on the things that matter.

### Step 3: Add team context to CLAUDE.md

Add an `## Onboarding` section to your `CLAUDE.md`. `/sup` reads it and incorporates it into every session and the generated `ONBOARDING.md`:

```markdown
## Onboarding
- Run `make setup` before anything else
- Read `docs/architecture.md` for system design context
- Auth system owned by @alice, data pipeline by @bob
- Ask in #dev-help — 30-minute rule before escalating
- Deploy process: PR → staging → 24h soak → prod
```

### What ONBOARDING.md is for

`/sup` offers to generate `ONBOARDING.md` as Phase 4 option b. It's a static team-facing document: repo overview, tech stack, Claude Code setup, team notes, first-week steps checklist. Commit it to the repo so new hires have it before day 1. It's not the learning system — it's the pre-reading.

After the session, `/sup` also offers to **bootstrap the repo's Claude Code setup** — create a CLAUDE.md, add starter hooks, write a custom command — if any of these are absent.

---

## Install

**Standalone install (recommended — clean command names):**
```bash
git clone https://github.com/[user]/sup && cd sup && bash install.sh
```

`install.sh` copies:
1. `commands/sup.md`, `tree.md`, `review.md`, `cheatsheet.md` → `~/.claude/commands/` (clean names: `/sup`, `/tree`, etc.)
2. `topics/*.md` (schema files) → `~/.claude/knowledge-trees/schemas/`

After this, `/sup`, `/tree`, `/review`, `/cheatsheet` are available in every repo.

**Optional — passive observer (auto-updates your tree as you work):**
```bash
bash scripts/install-hook.sh
```

See [Passive observer](#passive-observer) below.

**Plugin install (namespaced commands, auto-updates):**
```bash
/plugin marketplace add berniegreen/sup
/plugin install sup@sup-marketplace
```

Commands are namespaced: `/sup:sup`, `/sup:tree`, `/sup:review`, `/sup:cheatsheet`. Hooks are auto-registered — no `install-hook.sh` needed. Updates via `/plugin update sup@sup-marketplace`.

On first session start after install, `skill-observer.py` detects `CLAUDE_PLUGIN_ROOT` and automatically symlinks `topics/*.md` → `~/.claude/knowledge-trees/schemas/`. No manual schema installation needed. On plugin update, symlinks are refreshed to the new plugin cache path on next session start.

**Submit to the official Anthropic marketplace:**

Once the repo is public on GitHub, submit at [claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit) or [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit). The official marketplace (`claude-plugins-official`) is pre-registered in Claude Code — no `/plugin marketplace add` needed for installed plugins.

**Adding a community topic:**
```bash
cp your-topic.md ~/.claude/knowledge-trees/schemas/your-topic.md
# Then use it: /sup your-topic
```

---

## How it's structured

Three categories of files in this repo — they serve different purposes and go different places:

| Category | Source location | After install | Scope |
|----------|----------------|---------------|-------|
| **Commands** | `commands/` | `~/.claude/commands/` | Global — every repo |
| **Schemas** (topic curricula) | `topics/` | `~/.claude/knowledge-trees/schemas/` or `.claude/knowledge-trees/schemas/` | Global or project-local — `/sup` checks project-local first |
| **Observer** | `scripts/skill-observer.py` | `~/.claude/hooks/` | Global — runs on every CC event |
| **Plugin hooks** | `hooks/hooks.json` | Plugin cache (auto via `/plugin install`) | Plugin path only — auto-symlinks schemas on first session start |
| **Dev scripts** | `scripts/` | Not installed | Repo-only utilities |

**`commands/` at root** is the source of truth for command files — used by both `install.sh` (standalone path) and the plugin system. `.claude/commands/` is gitignored; `dev-setup.sh` creates symlinks there for project-scope testing.

**`topics/` and `scripts/` are not CC config** — they're project source files. `.claude/` is for what CC reads; `topics/` and `scripts/` are for what you edit and install from.

---

## Schemas and knowledge trees

These are two different things in `~/.claude/knowledge-trees/`:

| | Location | What it contains | Created by |
|--|----------|-----------------|------------|
| **Schema** | `~/.claude/knowledge-trees/schemas/[topic].md` | Curriculum blueprint: all nodes, detection signals, gap questions, mastery criteria, doc links | `install.sh` (from `topics/`) |
| **Knowledge tree** | `~/.claude/knowledge-trees/[topic].md` | Your personal progress: node statuses, evidence trails, review schedule, XP | `/sup` (written on Phase 4) |

One schema per topic, exactly. `topics/claude-code.md` → `schemas/claude-code.md` → used by `/sup claude-code`. Your progress lives next to it: `~/.claude/knowledge-trees/claude-code.md`.

**Schema file format** (for building a new topic):
A schema is a Markdown file with YAML frontmatter (`topic`, `version`, `description`) and sections for: Node definitions (with `source_url` column), Detection signals, Gap questions, Unlock thresholds, Tier definitions, Tree render template, Saved tree file template. See `topics/claude-code.md` for a complete example.

---

## Dev setup (for working on sup itself)

Two scripts manage the connection between the repo and your global `~/.claude/` install:

Two dev workflows — pick the one that fits your task:

**Option A — Project-scope (clean names, in this repo only):**
```bash
bash scripts/dev-setup.sh
```

Creates:
```
repo/.claude/commands/sup.md         → repo/commands/sup.md   (project-scope symlinks)
repo/.claude/commands/tree.md        → repo/commands/tree.md
repo/.claude/commands/review.md      → repo/commands/review.md
repo/.claude/commands/cheatsheet.md  → repo/commands/cheatsheet.md
~/.claude/knowledge-trees/schemas/claude-code.md     → repo/topics/claude-code.md
~/.claude/knowledge-trees/schemas/best-practices.md  → repo/topics/best-practices.md
~/.claude/knowledge-trees/schemas/mcp-development.md → repo/topics/mcp-development.md
~/.claude/knowledge-trees/schemas/anthropic-api.md   → repo/topics/anthropic-api.md
```

Effect: `/sup`, `/tree`, `/review`, `/cheatsheet` work in this repo with clean names. Edit `commands/` or `topics/` — changes reflected immediately. Schema symlinks are global, so updated schemas work in any repo.

**Option B — Plugin mode (any repo, namespaced):**
```bash
claude --plugin-dir /path/to/sup
```

Loads the plugin for the current session in any repo. Commands are namespaced (`/sup:sup`, `/sup:tree`). Use `/reload-plugins` to pick up changes without restarting.

**`bash scripts/dev-teardown.sh`** — removes `.claude/commands/` symlinks; replaces global schema symlinks with real copies. `~/.claude/knowledge-trees/schemas/` is back to independent copies — edits to `topics/` no longer affect installed schemas.

Note: when using `--plugin-dir ./sup`, `CLAUDE_PLUGIN_ROOT` is set to the repo path. `SessionStart` fires and symlinks `topics/` → `~/.claude/knowledge-trees/schemas/` automatically — no manual schema step needed.

---

## Passive observer

The passive observer is a hook that watches all Claude Code sessions and updates `~/.claude/knowledge-trees/claude-code.md` whenever it detects skill evidence — without you having to run `/sup`.

**How hooks work:** Claude Code fires hook events during the session lifecycle. `skill-observer.py` listens to three event types:

- **PostToolUse** — fires after every tool call (Bash, Edit, Write, etc.). Pattern-matches tool inputs for skill evidence.
- **WorktreeCreate** — fires when a git worktree is created. Direct evidence of worktree usage.
- **SessionStart** — fires at session start with a `source` field (`startup`, `resume`, `clear`, or `compact`). Detects `/compact` usage and session resumption.

What it detects:
- Bash `git worktree add` or WorktreeCreate event → Worktrees `[✓|historical]`
- Bash `claude -p` → Bash mode / headless mode `[✓|historical]`
- Writes to `.claude/agents/*.md` → Custom subagent definitions `[✓|historical]`
- Writes to `.claude/commands/*.md` → Custom slash commands `[✓|historical]`
- Writes to `~/.claude/settings.json` with `hooks` key → PostToolUse hooks `[✓|historical]`
- Writes to `~/.claude/settings.json` with `mcpServers` key → MCP servers `[✓|historical]`
- SessionStart `source: compact` → Context window / /compact usage `[~|reported]`
- SessionStart `source: resume` → Session naming and resumption `[~|reported]`

**What the observer cannot detect:** Built-in CLI commands (`/help`, `/compact`, `/usage`, `/doctor`) are handled by the Claude Code CLI itself — they never enter the tool loop and fire **no hook events**. This is an architectural constraint, not a bug. Mastery of these is captured via `/sup`'s assessment. The observer catches what you *do*; `/sup` captures what you *understand*. SessionStart `[~|reported]` nodes can be upgraded to `[✓]` by running `/sup`.

Install:
```bash
# From the sup repo — copies the script and registers all three hooks in one step:
bash scripts/install-hook.sh

# Verify — run any Claude Code session, then check your tree:
cat ~/.claude/knowledge-trees/claude-code.md
```

`install-hook.sh` copies `skill-observer.py` to `~/.claude/hooks/` and edits `~/.claude/settings.json` to register PostToolUse, WorktreeCreate, and SessionStart hooks. After that, `skill-observer.py` runs automatically on every relevant CC event — no further action needed. The two files have separate roles: `install-hook.sh` is a one-time setup script you run; `skill-observer.py` is the persistent handler CC runs automatically.

---

## Usage

```
/sup
```

With context to personalize from the start:
```
/sup I'm a new backend engineer joining the team
/sup I want to focus on the auth system
/sup just installed Claude Code, never used it before
```

With a specific topic:
```
/sup best-practices
/sup best-practices I want to improve my CLAUDE.md
/sup mcp-development
/sup anthropic-api I'm building a pipeline
```

Consultant mode (mid-session, any topic):
```
/sup which skills apply to writing a good hook?
/sup best-practices what should go in a project vs. global CLAUDE.md?
```

---

## `/review` — spaced repetition review

`/review` runs a focused review session for demonstrated `[✓]` nodes that are due today. No assessment, no new skills — just reinforcement.

```
/review                    # Review due nodes for claude-code (default)
/review best-practices     # Review a specific topic
```

How it works:
- Finds all `[✓]` nodes where `next: YYYY-MM-DD` ≤ today
- Asks one targeted question per node
- **Pass** (specific detail): advance one level, new date computed from interval ladder
- **Fail** (vague or no): reset to L1, review again tomorrow
- Updates the saved file with new dates

Interval ladder: L1=1 day · L2=3 days · L3=7 days · L4=21 days · L5=60 days · L6=permanent

---

## `/cheatsheet` — personal reference from your evidence trails

`/cheatsheet` reads your knowledge tree and renders a scannable personal reference — all demonstrated `[✓]` nodes with their actual evidence trails, formatted as "how I did this" documentation.

```
/cheatsheet                   # Cheat sheet for claude-code (default)
/cheatsheet best-practices    # Cheat sheet for a specific topic
```

Example output:

```
## [C] Code Change Workflows

**Multi-file coordinated changes**
- *my-app, 2026-02-20*: added userId field across 4 files
- Reference: Common tasks (docs.anthropic.com)

**Commit / PR description generation**
- *sup, 2026-03-01*: generated PR description from git diff for auth refactor
- Reference: Common tasks (docs.anthropic.com)
```

No inference, no questions, no writes. The evidence trails come from what you've actually demonstrated — so the cheat sheet improves every time you run `/sup` and complete an exercise.

---

## `/tree` — view your knowledge tree

`/tree` is a read-only companion command. No inference, no questions, no writes.

```
/tree                     # Show claude-code tree (default)
/tree best-practices      # Show a specific topic
/tree mcp-development     # Show MCP development tree
/tree all                 # Show all topics
```

To share your knowledge tree: copy the contents of `~/.claude/knowledge-trees/[topic].md`.

---

## Repo structure

**The sup repo:**

```
sup/
├── .claude-plugin/
│   └── plugin.json        ← Plugin manifest (name, version, description)
├── commands/              ← Command source — source of truth for both install paths
│   ├── sup.md, tree.md, review.md, cheatsheet.md
├── hooks/
│   └── hooks.json         ← Plugin hook config (auto-registered via /plugin install)
├── topics/                ← Schema source files → installed to ~/.claude/knowledge-trees/schemas/
│   ├── claude-code.md, best-practices.md, mcp-development.md, anthropic-api.md
├── scripts/               ← Developer utilities (never installed as CC config)
│   ├── skill-observer.py  → installed to ~/.claude/hooks/ (via install-hook.sh)
│   ├── dev-setup.sh, dev-teardown.sh, install-hook.sh
├── .claude/
│   ├── commands/          ← Gitignored; created by dev-setup.sh as project-scope symlinks
│   ├── settings.json      ← Project-level CC settings
│   └── settings.local.json ← Personal (gitignored)
└── install.sh
```

**After `bash install.sh`:**

```
~/.claude/
├── commands/
│   └── sup.md, tree.md, review.md, cheatsheet.md  ← available in every repo
├── knowledge-trees/
│   ├── schemas/            ← topic curricula (from topics/)
│   ├── claude-code.md      ← your personal tree (created by /sup)
│   └── [topic].md ...
├── hooks/
│   └── skill-observer.py   ← optional, via install-hook.sh
└── settings.json
```

---

## Roadmap

Topics planned but not yet built:

| Topic | Focus |
|-------|-------|
| `claude-cli` | CLI flags: `-p`, `--model`, `--output-format`, `--resume`, headless scripting, CI |
| `claude-settings` | settings.json, permissions, hooks syntax, MCP config, CLAUDE.md hierarchy |
| `claude-features` | In-app modes: plan mode, /compact, /help, memory, subagents, skills |
| `claude-plugins` | Plugin system (deferred — not yet stable) |
| `claude-cowork` | Collaboration features (deferred) |
| `bash` | Bash scripting fundamentals |
| `react` | React patterns and best practices |
| `typescript` | TypeScript type system and patterns |

To contribute a schema: see `topics/claude-code.md` for the full format.

---

## How it's built

`/sup`, `/tree`, and `/review` are single Markdown files in `commands/`. Three command files, no runtime, no dependencies. Claude Code discovers them and exposes them as `/` commands (via `~/.claude/commands/` after install, or namespaced as `/sup:*` via the plugin).

Topic schemas live in `topics/` — one Markdown file per topic. They're loaded at invocation time via `!bash-command` injection. The engine (sup.md) contains zero topic-specific content.

The technical mechanisms at work:

- **`!bash-command` syntax**: Shell commands execute at invocation time and inject their output into the prompt as static text. The 80+ scanning commands run before Claude processes a single token. This is pre-computation, not agentic tool use — it's fast, deterministic, and produces structured data Claude reasons over.
- **Topic schema loading**: A bash command detects the requested topic from `$ARGUMENTS`, then `cat`s the appropriate schema file. The schema is injected as static text alongside all other collected context. Claude uses it as the node/signal/question reference for all inference.
- **`$ARGUMENTS`**: Replaced with whatever the user types after `/sup` — topic keyword + free-form context.
- **`allowed-tools`**: `Read, Glob, Grep, Bash, Write, Edit` — controlled access that lets Claude navigate the repo, run exercises, write ONBOARDING.md, create config files, and update the knowledge tree without unlimited tool access.
- **Persistent file I/O**: `~/.claude/knowledge-trees/[topic].md` is written by `/sup` and read by both commands. YAML frontmatter + Markdown body — human-readable, machine-parseable, shareable by copy-paste.
- **Spaced repetition**: `| next: YYYY-MM-DD [LN]` fields on `[✓]` nodes encode the review schedule. `/review` reads these, steps through due nodes, and updates the file. Pure file I/O — no external state, no database.
- **Branch logic in natural language**: The phase structure (detect → assess → infer → output → artifacts) is expressed entirely as instructions to Claude. There's no interpreter, no state machine, no parser. The prompt is the program.

This is what good Claude Code tooling looks like: extend the system where it's designed to be extended, let Claude do the reasoning, and constrain scope to what's actually needed.

This project is a demo of Claude Code's [custom slash commands](https://docs.anthropic.com/en/docs/claude-code/slash-commands) feature — specifically how `!` command execution, YAML frontmatter, `allowed-tools`, `$ARGUMENTS`, and persistent file I/O combine to create a stateful, adaptive, curriculum-aware learning system from a handful of Markdown files.
