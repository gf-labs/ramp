# Repo manifest — every tracked path, annotated

File-level inventory of the repo. **Maintained manually** — update it when files are
added or renamed. `scripts/check-docs.py` asserts that every path token in the `## Files`
block below exists, so a stale entry fails CI (`test.yml` lint job).

For a directory-level orientation read README.md § Repo structure instead; this file is
the exhaustive version.

## Files

```
commands/up.md               # Adaptive onboarding command — manages knowledge graph
commands/calibrate.md        # Placement worksheet front door — writes .ramp/calibrate.md; claims seed the graph
commands/check.md            # Check back the active task — grade the worksheet, persist via save_graph, report the XP delta
commands/list.md             # Read-only topic catalog (CLI-backed) — what exists, where you've started
commands/help.md             # 60-second orientation — what ramp is + the command map
commands/tour.md             # Guided single-pass tour of the loop — read-only, try-it beats, dynamic next step
commands/tree.md             # Read-only knowledge graph viewer
commands/review.md           # Spaced repetition review command
commands/cheatsheet.md       # Personal reference: demonstrated skills + evidence trails
commands/pin.md              # Mid-session checkpoint — status, node save, optional snapshot
commands/ingest.md           # Generate topic schemas from external sources (PDF, URL, file)
commands/wrap.md             # End-of-session knowledge harvest — node upgrades, SR schedule, snapshot
.claude-plugin/plugin.json   # Plugin manifest (name, version, description)
.claude-plugin/marketplace.json # Marketplace catalog (source, category, install metadata)
hooks/hooks.json             # Plugin hook config (PostToolUse + SessionStart)
.github/workflows/test.yml   # CI — ruff lint + pytest matrix (3.8 floor + current) on develop/main + PRs
.github/workflows/release-gate.yml # CI — manifest ↔ CHANGELOG ↔ tag consistency for → main
.github/workflows/release.yml # CD — on a v* tag: lint+test gate, manifest↔tag assert, GitHub Release from the CHANGELOG section
.github/dependabot.yml       # Weekly SHA-pin bumps for GitHub Actions
.claude/settings.json        # Project hook config (file-size-warn + skill-observer)
topics/claude-code.md        # Claude Code meta-topic (sources 5 sub-topics, 81 nodes total)
topics/getting-started.md    # Getting started sub-topic (12 nodes)
topics/build.md              # Build sub-topic (32 nodes)
topics/configuration.md      # Configuration sub-topic (13 nodes)
topics/deployment.md         # Deployment sub-topic (11 nodes)
topics/administration.md     # Administration sub-topic (13 nodes)
topics/best-practices.md     # Best practices topic schema (15 nodes)
topics/mcp-development.md    # MCP development topic schema (29 nodes)
topics/anthropic-api.md      # Anthropic API topic schema (18 nodes)
topics/claude-code-internals.md # Empirically-verified Claude Code internals (5 nodes — undocumented behaviors)
topics/git.md                # Git version control topic schema (27 nodes — standalone, Pro Git-sourced; first breadth topic)
topics/bash.md               # Bash scripting topic schema (29 nodes — standalone, GNU Bash Reference Manual-sourced)
topics/python.md             # Python language topic schema (31 nodes — standalone, Python Tutorial + Language Reference-sourced)
topics/object-oriented-design.md # Object-oriented design topic schema (29 nodes — standalone; source set, not a single spine: OORP CC-BY-SA + Wirfs-Brock RDD + Nystrom + Fowler)
scripts/skill-observer.py    # Passive observer hook (PostToolUse + SessionStart)
scripts/file-size-warn.py    # PostToolUse hook — warns when .md files exceed 600 lines
scripts/setup-mcp.py         # Provisions .venv + registers MCP server (opt-in — run manually, not on SessionStart)
scripts/check-docs.py        # Docs-consistency gate — README tables/badges ↔ tree; CI step in test.yml lint job
mcp/server.py                # knowledge-graph MCP server (read/write graphs; swappable backend)
mcp/start.sh                 # MCP launch wrapper — .venv python; avoids macOS symlink trap
ramp_core.py                 # stdlib-only kernel — write side (XP · SR dates · validate · lock) + read side (catalog · summary · node_count · graph_nodes) + detect side (schema ## Probes → run_detection) + lint side (schema conformance — problems vs advisories) + resolve side (topic argument → topic name, single source for every command); imported by skill-observer + mcp/server; CLI-backed for list/help/tree/detect/lint/resolve
tests/                       # stdlib pytest suite (ramp_core, xp, detection, schema-lint, resolve-topic, normalization, symlinks, setup-mcp, file-size-warn, check-docs) + server tests under .venv — importlib-loaded
requirements.txt             # MCP server deps — only to run mcp/server.py, not to test
requirements-dev.txt         # pytest (test suite) — installed by the matrix, incl. the 3.8 leg
requirements-lint.txt        # ruff pin — shared by test.yml's lint job and release.yml, kept out of the 3.8 leg
pyproject.toml               # Tooling config — ruff lint rules (target py38; no packaging, kernel is stdlib-only)
docs/tree-format.md          # Annotated v3 knowledge graph format example
docs/docs-map.md             # Maps all doc pages to topics and nodes
docs/topic-authoring.md      # Normative topic-authoring contract — skill definition, schema anatomy, probe/reference grammar, validation gate (lint-checked)
docs/design-notes.md         # Why: kernel, evidence-over-declaration, schema-declared probes
BACKLOG.md                   # Open product work, curated — bugs, features, topics, maintenance
CONTRIBUTING.md              # Branch flow, CI gates, topic authoring entry point
GETTING-STARTED.md           # Guided pre-install walk of the loop — the doc twin of /ramp:tour
.mcp.json.example            # MCP server config template (copy → .mcp.json, fill in paths)
README.md                    # Install instructions, modes, company deployment guide
LICENSE                      # MIT license
.gitignore                   # Ignores .venv/, .claude/commands/, docs/superpowers/, .mcp.json, .ramp/
```
