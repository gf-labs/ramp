# Changelog

All notable changes to `ramp` are documented here. This project follows
[Semantic Versioning](https://semver.org).

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
