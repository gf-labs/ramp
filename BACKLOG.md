# ramp — Backlog

## In Progress
(nothing)

## Up Next

## Backlog

### `/ramp:wrap` — end-of-session knowledge harvest
- **Size:** S
- Scans the current conversation thread for demonstrated skills, decisions, and tool use patterns; synthesizes them into knowledge graph updates and an optional MEMORY.md snapshot
- Complements `/ramp:snapshot` (which is general-purpose) — wrap is ramp-aware: it specifically looks for evidence of knowledge graph nodes and upgrades `[~]` → `[✓|exercise]` where the session provides Feynman-level demonstration
- **Steps:**
  1. Reflect on this session's tool calls, exercises, and explanations — identify any node that was actively demonstrated (not just claimed)
  2. For each identified node: show proposed upgrade (`[ ]`/`[~]` → `[✓|exercise]`) with one-line evidence note
  3. Ask for confirmation before writing
  4. Write updates to `~/.claude/knowledge-graphs/[topic].md` via MCP or Write tool; reset SR schedule for newly demonstrated nodes (`next: today+1d [L1]`)
  5. Optionally append a `## Session snapshot — [date]` to the project MEMORY.md (same as `/tools:snapshot` but filtered to ramp-relevant context only)
- **Relationship to existing commands:** `/ramp:up` assesses at session start; `/ramp:wrap` harvests at session end; `/ramp:review` maintains nodes between sessions

### ramp: doctor extension
- **Size:** S
- Create `ramp/.claude/commands/doctor.md` — the ramp-specific extension of `/tools:doctor`
- Open with: "Run `/tools:doctor` first for environment health, then check ramp-specific items below."
- Ramp checks to add: `CLAUDE_PLUGIN_ROOT` set and valid, schema symlinks present and not broken, knowledge-graph file exists + is version 3, ramp MCP configured (`.mcp.json`), plugin cache drift for `ramp@gfl-marketplace`
- The generic doctor is now plugin-delivered (not at a hardcoded `@` path) — reference it by command name, not file path

### Schema symlinks should prefer live repo over plugin cache
- **Size:** S
- The SessionStart hook updates schema symlinks to point to `CLAUDE_PLUGIN_ROOT/topics/` — but when `CLAUDE_PLUGIN_ROOT` is the plugin cache, edits to the live repo's `topics/` are invisible to `/ramp:up` until the plugin version is bumped
- Root cause: global hook fires with cache as `CLAUDE_PLUGIN_ROOT`; project hook fires with live repo path; last writer wins (or race condition picks one)
- Fix options: (a) prefer live repo symlinks when both point to valid files, (b) don't update symlinks if target already valid (skip re-pointing to cache), or (c) separate env vars for cache vs. dev root

### Dynamic `.mcp.json` resolution
- **Size:** S
- Replace static `.mcp.json.example` + manual setup with a script that detects `.venv/`, generates `.mcp.json` from a template, and registers the MCP server automatically
- Triggered by: `scripts/setup-mcp.py` or a new `/ramp:setup` command

### MCP server logs
- **Size:** S
- Add `logging` module to `mcp/server.py`; write to `~/.claude/logs/knowledge-graph.log` or stderr
- Include: tool call name, topic, read/write result, timestamp

### Cleanup/simplify Python scripts
- **Size:** S
- `scripts/skill-observer.py` and `scripts/file-size-warn.py` — reduce duplication, improve readability
- Parallelizable with MCP logs (non-overlapping files)

### Define Python lint rules
- **Size:** S
- Add `pyproject.toml` with `[tool.ruff]` section
- Wire into `audit.md` Check 10: replace `py_compile` with `ruff check`
- Parallelizable with MCP logs and script cleanup

### Audit after every query (lightweight hook)
- **Size:** M
- Add PostToolUse hook that runs JSON/Python lint checks (Checks 9–10) after every Edit/Write
- Shell-only — no Claude invocation; fast enough for every tool use
- Full `/audit` remains on-demand

### Expand audit rules + underlying dependencies
- **Size:** M
- Add checks: `pyproject.toml` present, lint rules defined, `BACKLOG.md` exists, design-docs referenced
- Define explicit dependency graph between audit checks (e.g., Check 10 depends on lint rules)

### Per-command model configuration
- **Size:** S
- Set `model:` frontmatter in command files to right-size token usage: e.g., Haiku for `/ramp:tree` and `/ramp:cheatsheet` (read-only, no inference), full model for `/ramp:up` and `/ramp:review`
- Measure actual token usage per command to inform assignments

### Permissions policy for `~/.claude/knowledge-graphs/`
- **Size:** S
- Add allow rules to `~/.claude/settings.json` covering `~/.claude/knowledge-graphs/` read/write — currently this directory is accessed by the MCP server and skill-observer.py without explicit permission entries, unlike other governed paths
- Audit what rules currently cover it and fill any gaps

### Add design docs (`docs/`)
- **Size:** M
- Architecture docs for: knowledge-graph file format, hook system design, MCP server architecture, plugin install flow
- One doc per subsystem; linked from CLAUDE.md `## Structure`

### Global `/doctor` command — base + project extension pattern
- **Size:** S
- Create `~/.claude/commands/doctor.md` — a global base command that defines the check framework: environment health, tool availability, config validity
- Each repo extends it via a local `.claude/commands/doctor.md` that sources the global base with `@~/.claude/commands/doctor.md` and adds project-specific checks (e.g., venv present, `.mcp.json` configured, dependencies installed)
- No native command inheritance in Claude Code — purely prompt engineering convention
- Open question: per-command extension via `@file` injection vs. per-section override; pick one approach and document as the pattern
- Prototype in `dotfiles` or `sup` first; generalize after

### Global command toolbox — audit, abstract, and extend
- **Size:** M
- Evaluate all commands across all projects (`~/.claude/commands/`, `.claude/commands/` in each repo, plugin commands) for abstraction opportunities
- Pattern to consider: a "base" command in `~/.claude/commands/` defines shared behavior; a project-local `.claude/commands/` file extends or overrides it — similar to class inheritance. Example: a global `/doctor` defines the check framework; each repo's `/doctor` adds project-specific checks.
- Questions to resolve: does Claude Code support command inheritance natively, or is this purely a prompt-engineering convention? What's the right granularity (per-command extension vs. per-section injection via `@file`)?
- Candidates for promotion to global scope: `doctor`, `audit`, `phase-status` (currently dotfiles-only)
- Candidates for base+extend pattern: `audit` (global base checks + per-repo additions)

### Integrated learning system — unified capability loop
- **Size:** L
- **Vision:** ramp's learning components should form a single coherent system — a capability loop where progress through one component feeds all others. Currently each component is implemented independently with no cross-system feedback.
- **The five components:**
  1. **Knowledge graph** — structured map of demonstrated vs. claimed skills; the shared state all other components read and write
  2. **Passive observer** (`skill-observer.py`) — detects skill signals from tool use; upgrades nodes to `[✓|artifact]` or `[✓|historical]` silently
  3. **XP + levels** — computed from graph node status and branch tier; represents cumulative capability
  4. **Spaced repetition** (`/ramp:review` Step 2a) — surfaces due `[✓]` nodes; advances interval ladder on pass; resets on fail
  5. **Feynman verification** (`/ramp:review` Step 2b) — upgrades `[~]` (claimed) → `[✓|exercise]` through teaching-level demonstration
- **Currently missing feedback loops:**
  - SR pass → XP bonus + level recalc
  - Feynman pass → SR schedule initialized at L1 (partially implemented)
  - Level threshold → unlock new graph branches (frontier nodes)
  - Passive observer upgrade → SR schedule reset (newly demonstrated nodes should enter SR)
  - Graph node upgrade (any path) → consistent XP recompute + level display update
- **Goal:** modular design with a defined interface per component — changes to one don't require touching the others. Each component reads/writes a shared graph contract; no component owns the full pipeline.
- **Why this matters:** the distinction between `[✓]` (demonstrated) and `[~]` (claimed) is the core product thesis — capability over engagement. The loop is what makes that distinction durable over time, not just meaningful at first run.
- **Prerequisite:** well-defined local storage contract (or backend). The MCP server (`mcp/server.py`) is the natural integration point — read/write operations should enforce the contract and trigger cross-component updates.

### Company deployment and onboarding model — reevaluate
- **Size:** M
- Current model: ONBOARDING.md (static doc) + custom topic schema (active learning path); both generated by `/ramp:up`
- Questions to resolve: what does a company actually install? what do engineers run on day 1? how does the knowledge graph integrate with team onboarding vs. personal ramp-up? is the two-tool model (doc + session) the right split?
- Review the full Phase 4 options (a–e) for coherence; check README company deployment section against current plugin arch

## Icebox (large / future sessions)

### Backend server for knowledge-graphs
- **Size:** L
- REST/GraphQL API to store knowledge-graphs for all users; replaces local `~/.claude/knowledge-graphs/`
- Powers org-level curricula, team skill matrices, cross-device sync
- `KNOWLEDGE_GRAPH_API_URL` env var (currently `KNOWLEDGE_GRAPH_API_URL` in `mcp/server.py`)

### Expertise comparison across users
- **Size:** L — depends on backend
- Aggregate demonstrated nodes by org/team — a "skill matrix" view
- Show relative expertise: who has demonstrated what, at what level

### Live topic updater (agent + backend service)
- **Size:** L
- Crawls Claude/Anthropic docs on a schedule; diffs against `topics/` schemas; proposes node additions/removals
- Likely a separate backend service with a `/ramp:sync-topics` trigger command
