# ramp `v0.13.0`

Claude Code adoption stalls for a predictable reason: the documentation is complete, but it doesn't adapt to *you* — your codebase, your current level, what you've already demonstrated. Most developers plateau at basic edits and multi-file changes. Hooks, worktrees, custom agents, MCP servers, and pipeline integration remain unexplored. The capability gap compounds.

`/ramp:up` solves this. Run it in any repo. It scans your environment — not just the codebase, but your Claude Code configuration, git history, session history, and prior progress. It asks at most 2–3 targeted questions about things that can't be detected. Then it delivers a personalized, repo-grounded learning path and stays engaged as your co-pilot for the session.

It's not a report. It's a mode.

---

## Design principles

**Detect before interrogating.** Over 80 shell commands run at invocation: CLAUDE.md content, hook configurations, MCP servers, worktree count, session history, headless invocations. By the time you see a question, `/ramp:up` has already determined your level and identified your gaps. You answer at most 3 questions. They're specific.

**Demonstrated over claimed.** The knowledge graph distinguishes `[✓]` (demonstrated) from `[~]` (self-reported). A hook in settings.json is `[✓|artifact]`. Saying "yes I've used hooks" is `[~|reported]`. A `[✓]` requires at least one specific verifiable detail — a flag, an observed behavior, a tradeoff navigated. The difference between "I've heard of hooks" and "I have a PostToolUse hook that fires my linter" is the entire gap between knowledge and practice.

**Mastery missions, not checklists.** Every node has a falsifiable mastery criterion and a repo-grounded exercise. Not "run your tests" — "run `pytest tests/` on `auth_service.py` and interpret the failures."

**Dependency-gated progression.** You don't reach Agents until you've demonstrated Code Changes. The gates are the pedagogy.

**Session-persistent, topic-namespaced.** Graphs live at `~/.claude/knowledge-graphs/[topic].md` and follow you across every repo. Returning users with a fresh graph (≤7 days) skip questions entirely. Progress is never lost.

**Spaced repetition.** `[✓]` nodes carry a `| next: YYYY-MM-DD [LN]` review schedule (1d → 3d → 7d → 21d → 60d → permanent). `/review` steps through due nodes one at a time. Pass = advance + XP. Fail = reset to L1.

**Engine/curriculum separation.** `/ramp:up` is topic-agnostic. The curriculum — nodes, detection signals, gap questions, mastery criteria, doc links — lives in schema files (`topics/`). Adding a topic means writing one file. The engine doesn't change.

---

## Topics

| Topic | Command (plugin) | Nodes | Focus |
|-------|---------|-------|-------|
| `claude-code` (default) | `/ramp:up` | 71 | Claude Code features — meta-topic sourcing 5 sub-topics |
| `best-practices` | `/ramp:up best-practices` | 15 | CLAUDE.md design, configuration patterns, session hygiene |
| `mcp-development` | `/ramp:up mcp-development` | 20 | Building MCP servers: tools, resources, prompts, distribution |
| `anthropic-api` | `/ramp:up anthropic-api` | 18 | Claude API: completions, tool use, agentic loops, production patterns |
| *(your topic)* | `/ramp:up [topic]` | any | Install your schema → it works |

Future topics planned (not yet built): `bash`, `react`, `typescript`, `dsa`, `git`.

---

## Three modes

| Context | What happens |
|---------|-------------|
| **Existing repo** | Scans codebase + env + history → renders knowledge graph → delivers mastery missions → stays engaged as session co-pilot |
| **Empty/new repo** | Asks what to build → builds it with you → narrates every Claude Code capability as it's used → renders knowledge graph from what was demonstrated |
| **Directory of repos** | Surveys all repos (name, stack, last activity) → you pick focus → proceeds as single-repo mode |

---

## The knowledge graph (claude-code topic)

71 nodes across 5 sub-topics. Every node grounded in Claude Code's actual feature surface.

```
[Getting Started] Core Foundations
    [✓] What Claude Code does and when to use it
    [✓] How Claude Code uses computers (tool loop)
    [★] Memory types and scope hierarchy

[Getting Started] Working Effectively
    [✓] Common workflow patterns
    [~] Writing effective prompts for code tasks

[Getting Started] Best Practices
    [★] CLAUDE.md as living project memory

[Build] Agents and Orchestration
    [✓] Subagent basics: spawning and tool access
    [~] Foreground vs. background subagents
    [★] Custom subagent definitions (.claude/agents/)

[Build] Skills and Plugins
    [✓] Skills (slash commands): creation and syntax
    [✓] Skill mechanics: $ARGUMENTS, !bash, @file

[Build] Hooks System
    [✓] PostToolUse hooks (linting, reactions)
    [★] PreToolUse hooks (validation, blocking)

[Build] Headless and MCP
    [~] Headless mode (-p flag, non-interactive)
    [ ] MCP: configure and use servers

[Configuration] Settings Fundamentals
    [✓] Settings scope hierarchy: global, project, local
    [✓] Model selection and budget configuration

[Configuration] Permissions and Security
    [✓] Permissions: allow/deny rules and glob patterns

[·] Deployment   (unlock: complete Configuration)
[·] Administration   (unlock: complete Deployment)

Your frontier: → Memory types [★]  → CLAUDE.md as living memory [★]  → PreToolUse hooks [★]
Level: Builder — hooks and commands demonstrated, moving into orchestration
```

Marker key: `[✓]` demonstrated · `[~]` self-reported · `[ ]` not yet · `[★]` mastery target · `[·]` locked

Each `[★]` node becomes a **mastery mission** — a falsifiable criterion + a repo-grounded exercise using real file names and your actual toolchain.

---

## Company deployment

### Two tools, two purposes

| | ONBOARDING.md | Custom topic schema |
|--|---|---|
| **Format** | Static markdown doc | Active knowledge graph session |
| **When used** | Day 1: "how do I run this?" | First week: guided onboarding with exercises |
| **Personalized?** | No — same doc for everyone | Yes — starts from what the dev already knows |
| **Progress tracking** | No | Yes — evidence trails, XP, spaced repetition |
| **Generated by** | `/ramp:up` Phase 4 option b | `/ramp:up [your-topic]` |
| **Committed to repo?** | Yes (optional) | Schema yes; knowledge graphs are personal |

Use both: ONBOARDING.md for the quick-start reference, a custom topic for the active ramp-up.

### Step 1: Commit the commands

Copy command files to your team repo's `.claude/commands/`:

```bash
cp commands/ramp.md    /your-team-repo/.claude/commands/ramp.md
cp commands/tree.md    /your-team-repo/.claude/commands/tree.md
cp commands/review.md  /your-team-repo/.claude/commands/review.md
```

Engineers get the commands on clone. Knowledge graphs (`~/.claude/knowledge-graphs/`) remain personal — they live on each developer's machine, not in the repo.

### Step 2: Create a custom topic schema (optional but recommended)

Create `.claude/knowledge-graphs/schemas/[your-topic].md` in the team repo. This is the curriculum for onboarding to THIS codebase — nodes, detection signals, gap questions, and mastery criteria specific to your project.

```
.claude/
└── knowledge-graphs/
    └── schemas/
        └── acme-onboarding.md   ← commit this
```

Example nodes: `[ROOT] Environment setup` (make setup, .env, local run), `[A] Architecture` (data flow, service ownership), `[B] Dev workflow` (PR process, test suite, deploy), `[C] Team practices` (escalation, monitoring).

See `topics/claude-code.md` for the full schema format. When committed to `.claude/knowledge-graphs/schemas/`, the schema is available immediately — engineers clone and run `/ramp:up acme-onboarding`.

### Step 3: Add team context to CLAUDE.md

Add an `## Onboarding` section to your `CLAUDE.md`. `/ramp:up` reads it and incorporates it into every session and the generated `ONBOARDING.md`:

```markdown
## Onboarding
- Run `make setup` before anything else
- Read `docs/architecture.md` for system design context
- Auth system owned by @alice, data pipeline by @bob
- Ask in #dev-help — 30-minute rule before escalating
- Deploy process: PR → staging → 24h soak → prod
```

### What ONBOARDING.md is for

`/ramp:up` offers to generate `ONBOARDING.md` as Phase 4 option b. It's a static team-facing document: repo overview, tech stack, Claude Code setup, team notes, first-week steps checklist. Commit it to the repo so new hires have it before day 1. It's not the learning system — it's the pre-reading.

After the session, `/ramp:up` also offers to **bootstrap the repo's Claude Code setup** — create a CLAUDE.md, add starter hooks, write a custom command — if any of these are absent.

---

## Install

**From a local clone (recommended for now):**
```bash
git clone https://github.com/gf-labs/claude-code-slash-getting-started ~/path/to/sup
```
Then in any Claude Code session:
```
/plugin marketplace add ~/path/to/sup
/plugin install ramp@gfl-marketplace
```

**From GitHub (once public on the Anthropic marketplace):**
```
/plugin marketplace add gf-labs/claude-code-slash-getting-started
/plugin install ramp@gfl-marketplace
```

Commands are namespaced: `/ramp:up`, `/ramp:tree`, `/ramp:review`, `/ramp:cheatsheet`. Hooks (passive observer) and schemas are set up automatically on first session start. Update with `/plugin update ramp@gfl-marketplace`.

**Submit to the official Anthropic marketplace:**

Once the repo is public on GitHub, submit at [claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit) or [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit). The official marketplace (`claude-plugins-official`) is pre-registered in Claude Code — no `/plugin marketplace add` needed for installed plugins.

**Adding a community topic:**
```bash
cp your-topic.md ~/.claude/knowledge-graphs/schemas/your-topic.md
# Then use it: /ramp:up your-topic
```

---

## MCP server (`knowledge-graph`)

`mcp/server.py` is an optional MCP server that gives `/ramp:up` structured read/write access to your knowledge graphs — atomic saves, cross-device sync, and a clear upgrade path to team and org layers.

**Why use it:** Without the MCP, `/ramp:up` reads graphs via a bash `cat` at session start and writes via the Write tool. With the MCP, reads and writes go through structured tools — enabling swappable backends (local files → hosted API) without changing `ramp.md`.

**Setup:**

```bash
pip install mcp
```

Add to `~/.claude/.mcp.json` (global, all repos):
```json
{
  "mcpServers": {
    "knowledge-graph": {
      "command": "python3",
      "args": ["/absolute/path/to/sup/mcp/server.py"]
    }
  }
}
```

Or project-local (`.mcp.json` in the repo root):
```json
{
  "mcpServers": {
    "knowledge-graph": {
      "command": "python3",
      "args": ["./mcp/server.py"]
    }
  }
}
```

**Tools exposed:**

| Tool | Description |
|------|-------------|
| `read_graph(topic)` | Read a knowledge graph — returns markdown |
| `save_graph(topic, content)` | Atomic write + optional backend sync |
| `list_topics()` | All topics with level and XP — returns JSON |
| `get_benchmarks(topic)` | Personal stats; team/org when backend configured |
| `export_delta(topic, since_date)` | Demonstrated nodes since a date — for team sharing |

**Hosted backend (team/org):**

Set `KNOWLEDGE_GRAPH_API_URL` to point the MCP at a backend API:
```bash
export KNOWLEDGE_GRAPH_API_URL=https://your-backend.example.com
```

The server proxies `read_graph` and `save_graph` to `GET/PUT /graphs/{topic}` and `get_benchmarks` to `GET /benchmarks/{topic}`. The backend enables cross-device sync, team skill matrices, org dashboards, and the global curriculum feedback loop. Falls back to local files if the backend is unreachable.

---

## How it's structured

Three categories of files in this repo — they serve different purposes and go different places:

| Category | Source | After install | Scope |
|----------|--------|---------------|-------|
| **Commands** | `commands/` | Plugin cache (namespaced `/ramp:*`) or team repo's `.claude/commands/` (clean names) | Plugin: every repo · Company deploy: that repo only |
| **Schemas** | `topics/` | `~/.claude/knowledge-graphs/schemas/` (auto-symlinked on first session start) or `.claude/knowledge-graphs/schemas/` | Global or project-local — `/ramp:up` checks project-local first |
| **Observer + hooks** | `scripts/skill-observer.py`, `hooks/hooks.json` | Plugin cache — auto-registered on install | Plugin path only |

`commands/` at root is the source of truth — used by the plugin and company deploy. `.claude/commands/` in this repo is gitignored.

---

## Schemas and knowledge graphs

These are two different things in `~/.claude/knowledge-graphs/`:

| | Location | What it contains | Created by |
|--|----------|-----------------|------------|
| **Schema** | `~/.claude/knowledge-graphs/schemas/[topic].md` | Curriculum blueprint: all nodes, detection signals, gap questions, mastery criteria, doc links | Plugin install (auto-symlinked from `topics/` on first session start) |
| **Knowledge graph** | `~/.claude/knowledge-graphs/[topic].md` | Your personal progress: node statuses, evidence trails, review schedule, XP | `/ramp:up` (written on Phase 4) |

One schema per topic. `topics/claude-code.md` → `schemas/claude-code.md` → used by `/ramp:up`. Your personal progress lives at `~/.claude/knowledge-graphs/claude-code.md`.

To build a new topic schema, see `topics/claude-code.md` for the format.

---

## Dev setup (for working on sup itself)

**Plugin mode (load for any repo, namespaced commands):**
```bash
claude --plugin-dir /path/to/sup
```

Loads the plugin for the current session in any repo. Commands are namespaced (`/ramp:up`, `/ramp:tree`). Use `/reload-plugins` to pick up changes without restarting.

When using `--plugin-dir ./sup`, `CLAUDE_PLUGIN_ROOT` is set to the repo path. `SessionStart` fires and symlinks `topics/` → `~/.claude/knowledge-graphs/schemas/` automatically — no manual schema step needed.

**Refreshing the installed plugin after command changes:**

`/plugin install` skips silently if the plugin is already installed — the cache is not updated. After adding or removing files from `commands/`, you must force a cache refresh:

1. Open `/plugin` menu → remove the marketplace
2. `/plugin marketplace add ~/repos/sup`
3. `/plugin install ramp@gfl-marketplace`

`/reload-plugins` alone is not sufficient — it reloads from the existing cache, not from the source repo. The `--plugin-dir` dev workflow always reads live from the source and avoids this issue entirely.

---

## Passive observer

The passive observer is a hook that watches all Claude Code sessions and updates `~/.claude/knowledge-graphs/claude-code.md` whenever it detects skill evidence — without you having to run `/ramp:up`.

`skill-observer.py` listens to three hook events (`PostToolUse`, `WorktreeCreate`, `SessionStart`) and detects:
- Bash `git worktree add` or WorktreeCreate event → Worktrees `[✓|historical]`
- Bash `claude -p` → Bash mode / headless mode `[✓|historical]`
- Writes to `.claude/agents/*.md` → Custom subagent definitions `[✓|historical]`
- Writes to `.claude/commands/*.md` → Custom slash commands `[✓|historical]`
- Writes to `~/.claude/settings.json` with `hooks` key → PostToolUse hooks `[✓|historical]`
- Writes to `~/.claude/settings.json` with `mcpServers` key → MCP servers `[✓|historical]`
- SessionStart `source: compact` → Context window / /compact usage `[~|reported]`
- SessionStart `source: resume` → Session naming and resumption `[~|reported]`

**What the observer cannot detect:** Built-in CLI commands (`/help`, `/compact`, `/usage`, `/doctor`) never enter the tool loop — no hook events fire. Mastery of these is captured via `/ramp:up`'s assessment. `[~|reported]` nodes can be upgraded to `[✓]` by running `/ramp:up`.

**Install (via plugin — automatic):**

The passive observer is bundled in the plugin. Hooks are auto-registered when you install via `/plugin install`. No separate setup needed.

**Verify:**
```bash
cat ~/.claude/knowledge-graphs/claude-code.md
```

Run any Claude Code session, then check your graph to confirm the observer is active. `skill-observer.py` runs automatically on every relevant CC event from the plugin cache.

---

## Usage

Plugin commands are namespaced: `/ramp:up`, `/ramp:tree`, `/ramp:review`, `/ramp:cheatsheet`. Company-deployed commands use clean names. Examples use clean names for readability.

```
/ramp:up
/ramp:up I'm a new backend engineer joining the team
/ramp:up best-practices
/ramp:up mcp-development I'm building a server
```

Consultant mode (mid-session):
```
/ramp:up which skills apply to writing a good hook?
/ramp:up best-practices what should go in a project vs. global CLAUDE.md?
```

---

## `/ramp:review` — spaced repetition review

`/ramp:review` runs a focused review session for demonstrated `[✓]` nodes that are due today. No assessment, no new skills — just reinforcement.

```
/ramp:review                    # Review due nodes for claude-code (default)
/ramp:review best-practices     # Review a specific topic
```

How it works:
- Finds all `[✓]` nodes where `next: YYYY-MM-DD` ≤ today
- Asks one targeted question per node
- **Pass** (specific detail): advance one level, new date computed from interval ladder
- **Fail** (vague or no): reset to L1, review again tomorrow
- Updates the saved file with new dates

Interval ladder: L1=1 day · L2=3 days · L3=7 days · L4=21 days · L5=60 days · L6=permanent

---

## `/ramp:cheatsheet` — personal reference from your evidence trails

`/ramp:cheatsheet` reads your knowledge graph and renders a scannable personal reference — all demonstrated `[✓]` nodes with their actual evidence trails, formatted as "how I did this" documentation.

```
/ramp:cheatsheet                   # Cheat sheet for claude-code (default)
/ramp:cheatsheet best-practices    # Cheat sheet for a specific topic
```

No inference, no questions, no writes. The cheat sheet is built from your evidence trails — it improves every time you run `/ramp:up` and complete an exercise.

---

## `/ramp:tree` — view your knowledge graph

`/ramp:tree` is a read-only companion command. No inference, no questions, no writes.

```
/ramp:tree                     # Show claude-code graph (default)
/ramp:tree best-practices      # Show a specific topic
/ramp:tree mcp-development     # Show MCP development graph
/ramp:tree all                 # Show all topics
```

To share your knowledge graph: copy the contents of `~/.claude/knowledge-graphs/[topic].md`.

---

## Repo structure

**The ramp repo:**

```
sup/
├── .claude-plugin/
│   ├── plugin.json        ← Plugin manifest (name, version, description)
│   └── marketplace.json   ← Marketplace catalog (for /plugin marketplace add)
├── commands/              ← Command source files (used by plugin and company deploy)
│   ├── ramp.md, tree.md, review.md, cheatsheet.md
├── hooks/
│   └── hooks.json         ← Plugin hook config (auto-registered via /plugin install)
├── topics/                ← Schema source files → symlinked to ~/.claude/knowledge-graphs/schemas/ on session start
│   ├── claude-code.md, best-practices.md, mcp-development.md, anthropic-api.md
├── scripts/
│   └── skill-observer.py  ← Passive observer — invoked via hooks.json from plugin cache
└── .claude/
    ├── settings.json      ← Project-level CC settings
    └── settings.local.json ← Personal (gitignored)
```

**After `/plugin install`:**

```
~/.claude/
├── plugins/cache/ramp/
│   ├── commands/          ← ramp.md, tree.md, etc. (namespaced as /ramp:*)
│   ├── hooks/hooks.json   ← hook registrations (auto-active)
│   ├── scripts/           ← skill-observer.py (invoked by hooks)
│   └── topics/            ← schema source files (symlinked to schemas/ on session start)
├── knowledge-graphs/
│   ├── schemas/           ← topic curricula (symlinked from plugin cache topics/)
│   ├── claude-code.md     ← your personal graph (created by /ramp:up)
│   └── [topic].md ...
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
| `claude-cowork` | Collaboration features (deferred) |
| `bash` | Bash scripting fundamentals |
| `react` | React patterns and best practices |
| `typescript` | TypeScript type system and patterns |

To contribute a schema: see `topics/claude-code.md` for the full format.

---

## How it's built

`/ramp:up`, `/ramp:tree`, and `/ramp:review` are single Markdown files in `commands/`. Three command files, no runtime, no dependencies. Claude Code discovers them and exposes them as `/` commands (via `~/.claude/commands/` after install, or namespaced as `/ramp:*` via the plugin).

Topic schemas live in `topics/` — one Markdown file per topic. They're loaded at invocation time via `!bash-command` injection. The engine (ramp.md) contains zero topic-specific content.

The technical mechanisms at work:

- **`!bash-command` syntax**: Shell commands execute at invocation time and inject their output into the prompt as static text. The 80+ scanning commands run before Claude processes a single token. This is pre-computation, not agentic tool use — it's fast, deterministic, and produces structured data Claude reasons over.
- **Topic schema loading**: A bash command detects the requested topic from `$ARGUMENTS`, then `cat`s the appropriate schema file. The schema is injected as static text alongside all other collected context. Claude uses it as the node/signal/question reference for all inference.
- **`$ARGUMENTS`**: Replaced with whatever the user types after `/ramp:up` — topic keyword + free-form context.
- **`allowed-tools`**: `Read, Glob, Grep, Bash, Write, Edit` — controlled access that lets Claude navigate the repo, run exercises, write ONBOARDING.md, create config files, and update the knowledge graph without unlimited tool access.
- **Persistent file I/O**: `~/.claude/knowledge-graphs/[topic].md` is written by `/ramp:up` and read by both commands. YAML frontmatter + Markdown body — human-readable, machine-parseable, shareable by copy-paste.
- **Spaced repetition**: `| next: YYYY-MM-DD [LN]` fields on `[✓]` nodes encode the review schedule. `/review` reads these, steps through due nodes, and updates the file. Pure file I/O — no external state, no database.
- **Branch logic in natural language**: The phase structure (detect → assess → infer → output → artifacts) is expressed entirely as instructions to Claude. There's no interpreter, no state machine, no parser. The prompt is the program.

This project is a demo of Claude Code's [custom slash commands](https://docs.anthropic.com/en/docs/claude-code/slash-commands) feature — specifically how `!` command execution, YAML frontmatter, `allowed-tools`, `$ARGUMENTS`, and persistent file I/O combine to create a stateful, adaptive, curriculum-aware learning system from a handful of Markdown files.

---

*Plugin: `ramp@gfl-marketplace` · v0.13.0*
