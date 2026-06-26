# Changelog

All notable changes to `ramp` are documented here. This project follows
[Semantic Versioning](https://semver.org).

## [Unreleased]

**Honest contracts + discoverability tail.** Accumulating changes for the next
release (version intentionally not yet bumped): fixes that make existing promises
true (the Python-version floor; the review/XP claim), plus the knowledge-graph read
path is now single-sourced for the tree view.

### Added
- `ramp_core.graph_nodes` — the deep per-node read parser (status, type, XP, branch,
  section, schedule, evidence, and mastery-target), plus a `nodes` CLI verb exposing
  it: the no-MCP read path the tree view renders from.

### Changed
- `/ramp:tree` renders from the shared `ramp_core` read layer instead of parsing the
  graph in its own prompt — one parser, single-sourced; the raw file is kept only as
  a fallback.

### Fixed
- **Python floor is now truthful.** `ramp_core` enforces `MIN_PYTHON = (3, 8)` at the
  CLI boundary (`python_version_error`), and `skill-observer.py` gained
  `from __future__ import annotations` so its PEP-585 type hints no longer break import
  on Python 3.8 — the always-on passive observer runs on the version the badge
  advertises. The optional MCP server still requires Python 3.10+ (its `mcp`
  dependency), now documented as a caveat rather than the headline floor.
- `/ramp:list` and `/ramp:help` report a clear "python3 3.8+ missing" state instead of
  silently rendering a fake fresh-user view.
- Docs no longer claim a `/ramp:review` pass awards XP. A pass advances the
  spaced-repetition schedule; XP rises only when a node first reaches `[✓]` (including a
  `[~]→[✓]` upgrade during review). (README, CLAUDE.md)

## [1.2.0] — 2026-06-25

**Discoverability.** Two read-only commands make ramp self-explaining for a
newcomer, backed by a shared read layer in the kernel so the topic catalog and
per-graph summaries are computed once, not re-derived per command.

### Added
- `/ramp:list` — grouped catalog of every topic (core · sub · standalone) with
  node counts and your per-topic progress.
- `/ramp:help` — a 60-second orientation: what ramp is and the full command map.
- `ramp_core.py` read layer — `parse_frontmatter`, `summarize_graph`,
  `schema_node_count`, and `list_catalog`, plus a `catalog` / `summary` CLI: the
  no-MCP read path the new commands call.
- `node_count:` frontmatter on all ten topic schemas, single-sourcing the count
  shown by `/ramp:list`.

### Changed
- `up`, `review`, and `cheatsheet` show a first-run banner / empty-state redirect
  pointing newcomers at `/ramp:help` and `/ramp:list`.

### Tests
- Suite grown to 51 — read-layer and CLI coverage in `test_ramp_core.py`.

## [1.1.0] — 2026-06-22

**Reliability core.** The deterministic transforms now live in one stdlib-only
kernel that both runtimes share, so the Markdown commands *render* results instead
of recomputing them.

### Added
- `ramp_core.py` — single source of truth for XP, the spaced-repetition ladder and
  its date math, knowledge-graph validation (`validate_tree`), cross-process file
  locking, and the never-downgrade merge (`preserve_demonstrated`).
- MCP server: validated `save_graph` and `advance_review`, both routed through the kernel.

### Changed
- `skill-observer.py` (passive-observer hook) and `mcp/server.py` (MCP server) now
  both import `ramp_core` — one implementation, two consumers.
- `review`, `up`, `wrap`, and `pin` defer XP and review-date math to code rather than
  computing it inline.
- Topic schemas carry consistent TIER headers across all topics, giving XP and
  validation a uniform substrate.

### Tests
- Suite grown from 17 to 37 (adds `test_ramp_core.py`, `test_normalization.py`,
  `test_server.py`).

## [1.0.0] — 2026-06-17

Initial public release under `gf-labs`: adaptive, repo-grounded learning mode —
knowledge graphs, spaced repetition, XP tiers, the passive-observer hook, and the
optional knowledge-graph MCP server.
