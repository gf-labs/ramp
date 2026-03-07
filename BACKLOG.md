# ramp — Backlog

## In Progress
(nothing)

## Up Next

## Backlog

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

### XP / knowledge-graph / levels / spaced repetition — integrated ecosystem
- **Size:** L
- All four systems (XP, knowledge graphs, levels, spaced repetition) should form a coherent, integrated loop — progress in one updates the others
- Currently: XP is computed from tree status, levels are a label, spaced repetition is a `| next:` field, and graphs are flat files; no cross-system feedback
- Goal: modular design — each subsystem has a defined interface; changes to one don't require touching the others
- Example integrations: SR pass → XP bonus + level recalc; level threshold → unlock new graph branches; graph node upgrade → SR schedule reset
- Prerequisite: backend server (or well-defined local storage contract) to hold shared state

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
