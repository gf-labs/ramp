# Changelog

All notable changes to `ramp` are documented here. This project follows
[Semantic Versioning](https://semver.org).

## [Unreleased]

**Honest contracts, discoverability tail, and the legible workspace.** Accumulating
changes for the next release (version intentionally not yet bumped): fixes that make
existing promises true (the Python-version floor; the review/XP claim), the
single-sourced knowledge-graph read path, and the workspace slice — learning state
moves out of chat scrollback into two inspectable homes.

### Added
- `~/.claude/ramp/` global home (`graphs/` + `schemas/`), with automatic byte-for-byte
  migration of legacy `~/.claude/knowledge-graphs/` files on session start.
- `./.ramp/` per-repo session workspace — five fixed files (`worksheet` · `current` ·
  `calibrate` · `scan` · `lessons`), gitignored and regenerable; the canonical format
  contract lives in `up.md`.
- `/ramp:calibrate` — placement-worksheet front door: scan rows pre-filled from the
  schema's detection table, claims recorded as `[~|reported]` through the validated
  writer; new users running `/ramp:up` with no (or an unknown) topic are routed here.
- `/ramp:check` — explicit check-back: grades the active worksheet, persists through
  `save_graph`, and reports the XP delta (`/ramp:up`'s natural-language **done**
  handler runs the same protocol).
- `ramp_core.save_graph` + CLI `save` verb (full tree on stdin; exit 0 saved / 2
  rejected) — the validated no-MCP write path; the MCP server delegates to it.
- `ramp_core.graph_nodes` — the deep per-node read parser (status, type, XP, branch,
  section, schedule, evidence, and mastery-target), plus a `nodes` CLI verb exposing
  it: the no-MCP read path the tree view renders from.
- Kernel `due` and `advance` CLI verbs — review's SR queue and its schedule writes are
  kernel-computed on every install (no MCP required).
- CI: a pytest matrix proving the Python 3.8 floor, a manifest↔CHANGELOG↔tag release
  gate for `main`, and Dependabot for the SHA-pinned actions.

### Changed
- `/ramp:up` delivers exactly **one task at a time** to `.ramp/worksheet.md` (no
  menus in the lesson phase) and persists its scan scope + findings to `.ramp/scan.md`.
- Terminology sweep: bracket letter codes are hidden from user-facing output (plain
  section titles and position instead of labels), "Feynman" became teach-back, and
  cross-plugin `tools:*` references are gone.
- Every non-MCP graph save routes through the kernel CLI `save` verb — no Write- or
  Edit-simulated saves anywhere; when no writer is reachable, commands stop honestly.
- `/ramp:tree` renders from the shared `ramp_core` read layer instead of parsing the
  graph in its own prompt — one parser, single-sourced; the raw file is kept only as
  a fallback.
- `/ramp:review` renders its due queue from the kernel `due` verb and persists SR
  outcomes via MCP or the CLI `advance` verb — the hand-edited date fallback is gone.
- Write-path honesty: every graph write says which writer ran (MCP tool or kernel
  CLI), commands treat deferred MCP tools as loadable rather than absent, check-back
  verifies factual corrections against the node's reference before teaching them,
  and the tier label derives strictly from the active topic's tree.

### Fixed
- `/ramp:up`'s MCP scan read `settings.json`, where Claude Code never registers MCP
  servers — it now reads the real registries (project `.mcp.json`; `~/.claude.json`
  project + user scope), so configured servers are detected instead of silently
  falling back to the CLI writer.
- The best-practices schema taught wrong memory-scope facts: project memory lives at
  `./CLAUDE.md` (or `./.claude/CLAUDE.md`) and the personal layer is
  `./CLAUDE.local.md` at the repo root. The old `.claude/CLAUDE.md.local` never
  existed, so its detection signal could never fire — the up scan now checks the
  real file. (Facts verified against the live memory docs.)
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
- `compute_xp` counts a duplicated node name once (first occurrence) — a misfiled
  duplicate can no longer inflate XP; `validate_tree` still flags it for repair.
- `advance_review` honors the `permanent [L6]` field — a pass can no longer demote a
  retired node back into the review cycle.
- The `file-size-warn` hook's warning now reaches the session (exit-2 stderr);
  previously it only ever printed to the debug log.

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
