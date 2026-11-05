# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Design philosophy

`ramp` measures **demonstrated mastery** (`[✓]`) over **self-reported engagement** (`[~]`) — capability growth, not activity metrics. The knowledge graph, spaced repetition, XP tiers, and Feynman-style verification all express that single thesis: a learning tool should track what you can *do*, not what you've *clicked through*.

It is also a working demonstration of Claude Code's extension model — built entirely from slash commands, hooks, an MCP server, a plugin manifest, and the settings hierarchy, with no application code.

When making prioritization decisions, ask: **what best advances that capability-over-engagement thesis while showcasing Claude Code's extension model?**

## Project

`ramp` activates a **learning mode** — Claude becomes a co-pilot for ramping developers up on Claude Code as an organizational tool, the codebase, and the team's workflows (commits, PRs, testing, CI). It scans the environment, assesses the user, delivers a personalized knowledge graph and learning path, then stays engaged to work through exercises together. Writes an `ONBOARDING.md` artifact and updates `~/.claude/ramp/graphs/[topic].md`.

Companies deploy it as a project-level command for engineer onboarding. Solo devs use it to level up.

### Three operating modes

- **Mode A (empty repo)**: Claude asks what to build, then builds it while narrating every Claude Code capability it uses
- **Mode B (single repo)**: Scans codebase → assesses user → integrated learning path grounded in the actual repo
- **Mode C (multi-repo directory)**: Surveys all repos, user picks focus, then proceeds as Mode B

## Structure

Directory-level orientation: README.md § Repo structure. The exhaustive, CI-asserted
file-by-file manifest: [`docs/repo-manifest.md`](docs/repo-manifest.md).

`commands/` at root is the source of truth for command files — used by the plugin system
and company deployment (copy to a team repo's `.claude/commands/`). `.claude/commands/`
is gitignored.

No *application* is built — the engine is prompts. The deterministic kernel (the `scripts/`
hooks, `mcp/server.py`, and `ramp_core.py`) is code: it single-sources XP, spaced-repetition
scheduling, validation and locking so the pedagogy cannot silently drift. Commands remain
pure prompt engineering and propose status/evidence only.

**Engine and curriculum are separate, and must stay separate.** `commands/up.md` is
topic-agnostic; a topic's whole curriculum — nodes, detection signals, gap questions, mastery
criteria — lives in its `topics/<name>.md` schema. **Adding a topic is adding one file**; the
engine never changes for it. `commands/up.md` front-loads `!bash` scans that inject
environment context before the model reads a token; prefer moving a new probe into a
schema-declared probe over adding another injected line.

**MCP server gotcha:** `mcp/server.py` requires the repo-root `.venv` — system `python3` has
a conflicting `mcp` stub. `setup-mcp.py` uses `.venv/bin/python3` explicitly; running it by
hand needs `source .venv/bin/activate` first.

## Customization

ramp adapts at three levels of scope:

**1. Session context** — add `## Onboarding` to CLAUDE.md in any repo:
```markdown
## Onboarding
- Run `make setup` before anything else
- Read `docs/architecture.md` for system design context
- Auth system owned by @alice, data pipeline by @bob
- Ask in #dev-help — 30-minute rule before escalating
```
Injected into every `/ramp:up` session and the generated `ONBOARDING.md`.

**2. Project curriculum** — commit a schema to `.claude/knowledge-graphs/schemas/[topic].md`:
Engineers run `/ramp:up [topic]` and get a codebase-grounded learning path with exercises, evidence tracking, and spaced repetition. Auto-discovered from the project-local path — no install step. See `topics/claude-code.md` for the schema format.

**3. Backend / org-wide** — set `KNOWLEDGE_GRAPH_API_URL` (via `mcp/server.py`):
Graphs are loaded from a central backend at session start and synced back on save. Enables org-level curricula, team skill matrices, and cross-device sync. Without this env var, ramp runs fully local — no setup required.

## Knowledge graph

Both `/ramp:up` and `/ramp:tree` render and update a knowledge graph — a structured map of a developer's Claude Code capabilities.

**Tree structure (81 nodes across 5 sub-topics — claude-code topic):**
- **[Getting Started]** Core Foundations, Working Effectively, Best Practices — what Claude Code is, tool loop, memory, workflow patterns (12 nodes)
- **[Build]** Agents and Orchestration, Skills and Plugins, Hooks System, Headless and MCP — subagents, slash commands, hooks, headless mode (32 nodes)
- **[Configuration]** Settings Fundamentals, Permissions and Security, Interface Customization — settings hierarchy, allow/deny rules, keybindings (13 nodes)
- **[Deployment]** Cloud Provider Integration, Network and Infrastructure, Deployment Patterns — Bedrock, Vertex, Foundry, LLM gateways, CI/CD (11 nodes)
- **[Administration]** Setup and Authentication, Data and Compliance, Cost and Usage Management — org setup, ZDR, analytics, chargeback (13 nodes)

**Status markers:**
- `[✓]` **Demonstrated** — artifact found, exercise completed, or historical evidence verified
- `[~]` **Self-reported** — claimed but not corroborated by artifact or exercise (weaker signal)
- `[ ]` not yet · `[★]` mastery target (frontier) · `[·]` locked

**Spaced repetition:** `[✓]` nodes carry a `| next: YYYY-MM-DD [LN]` field (interval ladder: L1=1d, L2=3d, L3=7d, L4=21d, L5=60d, L6=permanent). `/ramp:up` surfaces due nodes in Phase 3. `/ramp:review` runs focused review sessions.

**Per-node doc links:** Each node in topic schemas has a `source_url` column. `/ramp:up` surfaces these as `**Reference:** [official docs](url)` in mastery mission exercises.

**XP system:** Each demonstrated `[✓]` node earns XP by branch tier (ROOT=10, A=15, B=20, C=25, D=35, E=50). `[~]` = half XP. Total stored as `xp:` in frontmatter. Displayed as "Level: Builder · 240 XP". A `/review` pass advances the schedule without changing XP; XP rises only when a node first reaches `[✓]` (including a `[~]→[✓]` upgrade earned during review).

**Adaptive pacing:** Phase 3 output scales with tier. Explorer (~20-30 lines, 1 skill), Builder (~50-60 lines, 2 skills), Practitioner/Expert (~80-100+ lines, 3 skills). Returning users with a fresh tree (≤7 days) skip gap questions entirely — straight to Phase 3.

**Demonstration types** (each node has one or more):
- **Artifact** — a file/config exists, auto-detected by bash scan
- **Exercise** — do something live in the session
- **Qualitative** — answer a targeted question; Claude applies an explicit rubric
- **Historical** — evidence from past work (git log, session files, worktree directories)

**Inference priority (highest to lowest, used only by `/ramp:up`):**
1. Environmental signals — CLAUDE.md content, hooks/MCP in settings.json, commands in `.claude/commands/`, history scans
2. Saved graph file — `~/.claude/ramp/graphs/[topic].md` persists progress from prior sessions; `[✓]` nodes are never downgraded
3. Self-reported assessment — fills gaps via targeted gap questions using teach-back framing ("explain X as you'd teach it") — teaching-level answers earn `[✓]`, surface-level answers stay `[~]`

**`/ramp:tree`** is a dumb read-only viewer. It reads `~/.claude/ramp/graphs/[topic].md` and displays it. No inference, no writes.

**`/ramp:review`** is a focused spaced repetition command. It reads due `[✓]` nodes, steps through them one at a time, applies the qualitative rubric, updates `| next:` fields. Passing advances the schedule; XP is unchanged unless a node is upgraded `[~]→[✓]`.

**Three-layer tree architecture** (maps to Claude Code's native scope model):

| Tree layer | Claude Code scope | Location | Git? | Phase 4 |
|-----------|------------------|----------|------|---------|
| **Personal global** | User | `~/.claude/ramp/graphs/[topic].md` | No | option `a` |
| **Team** | Project | `.claude/knowledge-graphs/[topic].md` | Yes | option `d` |
| **Local** | Local | `.claude/knowledge-graphs/local/[topic].md` | No (gitignored) | option `e` |

Merge priority: Local → Team → Personal. A local `[✓]` upgrades anything; nothing downgrades a `[✓]`. `/ramp:up` reads all three layers in Phase 2 and merges before output. Note: Claude Code does not walk up the directory tree — a `.claude/` at a parent level is treated as the project scope for sessions launched there.

## Topics

Topic schemas live in `topics/` and are symlinked into `~/.claude/ramp/schemas/` by a SessionStart hook (`skill-observer.py`'s `provision_schema_symlinks`); `/ramp:up` resolves the *single requested* topic from there — it does not scan or enumerate the directory. To add a custom topic: create `topics/[name].md` following the format in any existing file.

**Core (meta-topic + sub-topics):**
`claude-code` (81 nodes) — full Claude Code curriculum, sources all five sub-topics:
`getting-started` · `build` · `configuration` · `deployment` · `administration`

**Standalone:**
`best-practices` (15 nodes) — CLAUDE.md design, config, session hygiene
`mcp-development` (29 nodes) — building MCP servers from fundamentals to production
`anthropic-api` (18 nodes) — Claude API from basic completions to tool use loops
`claude-code-internals` (5 nodes) — empirically-verified Claude Code behaviors not in official docs
`git` (27 nodes) — version control from the snapshot model through branching, recovery, and internals (Pro Git-sourced; first breadth topic beyond Claude Code)
`bash` (29 nodes) — shell scripting from the language model through control flow, functions, robustness (strict mode, quoting, traps, ShellCheck), redirection and pipelines, and expansions (GNU Bash Reference Manual-sourced)
`python` (31 nodes) — the language from the object model through control flow and iteration, functions and scope, the workhorse containers, classes and the object protocol, and robustness (exceptions, context managers, generators, decorators) (Python Tutorial + Language Reference-sourced)
`object-oriented-design` (29 nodes) — designing with objects: responsibilities and encapsulation, turning a requirement into a model with CRC cards, structural relationships, designing for change, patterns as vocabulary, and repairing decayed design. First topic grounded in a **source set** rather than a single spine (OORP CC-BY-SA · Wirfs-Brock RDD · Nystrom · Fowler), because a design discipline has canonical literature, not a reference manual

## Knowledge graph file

**Location:** `~/.claude/ramp/graphs/[topic].md` (global, personal — follows the developer across all projects; schemas are symlinked beside it at `~/.claude/ramp/schemas/`)

**Per-repo workspace:** `./.ramp/` in the host repo (gitignored, regenerable) — five fixed files: `worksheet.md` · `current.md` · `calibrate.md` · `scan.md` · `lessons.md`. The canonical format contract is `commands/up.md` § *The ./.ramp/ workspace*; other commands reference it, never duplicate it.

**Format:** YAML frontmatter (machine-parseable) + Markdown body (human-readable).
Full annotated example: `docs/tree-format.md`

**Status + TYPE fields:** `[✓|artifact]`, `[✓|exercise]`, `[✓|historical]`, `[~|reported]`, `[ ]`. Type records how mastery was demonstrated.

**Review field:** `| next: YYYY-MM-DD [LN]` on `[✓]` nodes only. Encodes spaced repetition schedule.

**Version migration:** v1 files have all `[✓]` treated as `[✓|historical]`; v2 files get `| next:` fields added. Both upgrade to version 3 on next write with `xp:` computed.

