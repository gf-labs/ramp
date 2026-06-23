# Changelog

All notable changes to `ramp` are documented here. This project follows
[Semantic Versioning](https://semver.org).

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
