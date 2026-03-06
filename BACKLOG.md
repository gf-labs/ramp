# sup — Backlog

## In Progress
(nothing)

## Up Next

### Rename `knowledge-tree` → `knowledge-graph`
- **Size:** M — 101 occurrences across 18 files
- 5 change types: directory paths, MCP tool names, MCP server config key, human-readable text, plugin metadata
- MCP tool names are breaking (`mcp__knowledge-tree__*` → `mcp__knowledge-graph__*`)
- Requires migrating `~/.claude/knowledge-trees/` on local machine
- Must be done as a single coordinated session (touches everything)

## Backlog

### Dynamic `.mcp.json` resolution
- **Size:** S
- Replace static `.mcp.json.example` + manual setup with a script that detects `.venv/`, generates `.mcp.json` from a template, and registers the MCP server automatically
- Triggered by: `scripts/setup-mcp.py` or a new `/sup:setup` command

### MCP server logs
- **Size:** S
- Add `logging` module to `mcp/server.py`; write to `~/.claude/logs/knowledge-tree.log` or stderr
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
- Full `/sup:audit` remains on-demand

### Expand audit rules + underlying dependencies
- **Size:** M
- Add checks: `pyproject.toml` present, lint rules defined, `BACKLOG.md` exists, design-docs referenced
- Define explicit dependency graph between audit checks (e.g., Check 10 depends on lint rules)

### Add design docs (`docs/`)
- **Size:** M
- Architecture docs for: knowledge-graph file format, hook system design, MCP server architecture, plugin install flow
- One doc per subsystem; linked from CLAUDE.md `## Structure`

## Icebox (large / future sessions)

### Backend server for knowledge-graphs
- **Size:** L
- REST/GraphQL API to store knowledge-graphs for all users; replaces local `~/.claude/knowledge-graphs/`
- Powers org-level curricula, team skill matrices, cross-device sync
- `KNOWLEDGE_GRAPH_API_URL` env var (currently `KNOWLEDGE_TREE_API_URL` in `mcp/server.py`)

### Expertise comparison across users
- **Size:** L — depends on backend
- Aggregate demonstrated nodes by org/team — a "skill matrix" view
- Show relative expertise: who has demonstrated what, at what level

### Live topic updater (agent + backend service)
- **Size:** L
- Crawls Claude/Anthropic docs on a schedule; diffs against `topics/` schemas; proposes node additions/removals
- Likely a separate backend service with a `/sup:sync-topics` trigger command
