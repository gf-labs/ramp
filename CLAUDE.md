# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Design philosophy

`ramp` measures **demonstrated mastery** (`[✓]`) over **self-reported engagement** (`[~]`) — capability growth, not activity metrics. The knowledge graph, spaced repetition, XP tiers, and Feynman-style verification all express that single thesis: a learning tool should track what you can *do*, not what you've *clicked through*.

It is also a working demonstration of Claude Code's extension model — built entirely from slash commands, hooks, an MCP server, a plugin manifest, and the settings hierarchy, with no application code.

When making prioritization decisions, ask: **what best advances that capability-over-engagement thesis while showcasing Claude Code's extension model?**

## Project

`ramp` activates a **learning mode** — Claude becomes a co-pilot for ramping developers up on Claude Code as an organizational tool, the codebase, and the team's workflows (commits, PRs, testing, CI). It scans the environment, assesses the user, delivers a personalized knowledge graph and learning path, then stays engaged to work through exercises together. Writes an `ONBOARDING.md` artifact and updates `~/.claude/knowledge-graphs/[topic].md`.

Companies deploy it as a project-level command for engineer onboarding. Solo devs use it to level up.

### Three operating modes

- **Mode A (empty repo)**: Claude asks what to build, then builds it while narrating every Claude Code capability it uses
- **Mode B (single repo)**: Scans codebase → assesses user → integrated learning path grounded in the actual repo
- **Mode C (multi-repo directory)**: Surveys all repos, user picks focus, then proceeds as Mode B

## Structure

```
commands/up.md               # Adaptive onboarding command — manages knowledge graph
commands/tree.md             # Read-only knowledge graph viewer
commands/review.md           # Spaced repetition review command
commands/cheatsheet.md       # Personal reference: demonstrated skills + evidence trails
commands/pin.md              # Mid-session checkpoint — status, node save, optional snapshot
commands/ingest.md           # Generate topic schemas from external sources (PDF, URL, file)
commands/wrap.md             # End-of-session knowledge harvest — node upgrades, SR schedule, snapshot
.claude-plugin/plugin.json   # Plugin manifest (name, version, description)
.claude-plugin/marketplace.json # Marketplace catalog (source, keywords, install metadata)
hooks/hooks.json             # Plugin hook config (PostToolUse + SessionStart)
.claude/settings.json        # Project hook config (file-size-warn + skill-observer, model settings)
topics/claude-code.md        # Claude Code meta-topic (sources 5 sub-topics, 81 nodes total)
topics/getting-started.md    # Getting started sub-topic (12 nodes)
topics/build.md              # Build sub-topic (32 nodes after v0.17.0)
topics/configuration.md      # Configuration sub-topic (13 nodes)
topics/deployment.md         # Deployment sub-topic (11 nodes)
topics/administration.md     # Administration sub-topic (13 nodes)
topics/best-practices.md     # Best practices topic schema (15 nodes)
topics/mcp-development.md    # MCP development topic schema (29 nodes after v0.16.0)
topics/anthropic-api.md      # Anthropic API topic schema (18 nodes)
topics/claude-code-internals.md # Empirically-verified Claude Code internals (5 nodes — undocumented behaviors)
scripts/skill-observer.py    # Passive observer hook (PostToolUse + SessionStart)
scripts/file-size-warn.py    # PostToolUse hook — warns when .md files exceed 600 lines
mcp/server.py                # knowledge-graph MCP server (read/write graphs; swappable backend)
docs/tree-format.md          # Annotated v3 knowledge graph format example
docs/docs-map.md             # Maps all doc pages to topics and nodes
BACKLOG.md                   # Prioritized work items — immediate, medium, icebox
.mcp.json.example            # MCP server config template (copy → .mcp.json, fill in paths)
README.md                    # Install instructions, modes, company deployment guide
```

*This listing is maintained manually — update it when files are added or renamed.*

**Note:** `commands/` at root is the source of truth for command files — used by the plugin system and company deployment (copy to team repo's `.claude/commands/`). `.claude/commands/` is gitignored.

No build steps, no dependencies, no runtime. Commands are pure prompt engineering in Markdown files.

**MCP server gotcha:** `mcp/server.py` requires the `.venv` in the repo root — system `python3` has a conflicting `mcp` stub. `setup-mcp.py` uses `.venv/bin/python3` explicitly; if running manually, activate with `source .venv/bin/activate` first.

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
- **[Build]** Agents and Orchestration, Skills and Plugins, Hooks System, Headless and MCP — subagents, slash commands, hooks, headless mode (32 nodes after v0.17.0 additions)
- **[Configuration]** Settings Fundamentals, Permissions and Security, Interface Customization — settings hierarchy, allow/deny rules, keybindings (13 nodes)
- **[Deployment]** Cloud Provider Integration, Network and Infrastructure, Deployment Patterns — Bedrock, Vertex, Foundry, LLM gateways, CI/CD (11 nodes)
- **[Administration]** Setup and Authentication, Data and Compliance, Cost and Usage Management — org setup, ZDR, analytics, chargeback (13 nodes)

**Status markers:**
- `[✓]` **Demonstrated** — artifact found, exercise completed, or historical evidence verified
- `[~]` **Self-reported** — claimed but not corroborated by artifact or exercise (weaker signal)
- `[ ]` not yet · `[★]` mastery target (frontier) · `[·]` locked

**Spaced repetition:** `[✓]` nodes carry a `| next: YYYY-MM-DD [LN]` field (interval ladder: L1=1d, L2=3d, L3=7d, L4=21d, L5=60d, L6=permanent). `/ramp:up` surfaces due nodes in Phase 3. `/ramp:review` runs focused review sessions.

**Per-node doc links:** Each node in topic schemas has a `source_url` column. `/ramp:up` surfaces these as `**Reference:** [official docs](url)` in mastery mission exercises.

**XP system:** Each demonstrated `[✓]` node earns XP by branch tier (ROOT=10, A=15, B=20, C=25, D=35, E=50). `[~]` = half XP. Total stored as `xp:` in frontmatter. Displayed as "Level: Builder · 240 XP". `/review` pass awards a per-node XP bonus.

**Adaptive pacing:** Phase 3 output scales with tier. Explorer (~20-30 lines, 1 skill), Builder (~50-60 lines, 2 skills), Practitioner/Expert (~80-100+ lines, 3 skills). Returning users with a fresh tree (≤7 days) skip gap questions entirely — straight to Phase 3.

**Demonstration types** (each node has one or more):
- **Artifact** — a file/config exists, auto-detected by bash scan
- **Exercise** — do something live in the session
- **Qualitative** — answer a targeted question; Claude applies an explicit rubric
- **Historical** — evidence from past work (git log, session files, worktree directories)

**Inference priority (highest to lowest, used only by `/ramp:up`):**
1. Environmental signals — CLAUDE.md content, hooks/MCP in settings.json, commands in `.claude/commands/`, history scans
2. Saved graph file — `~/.claude/knowledge-graphs/[topic].md` persists progress from prior sessions; `[✓]` nodes are never downgraded
3. Self-reported assessment — fills gaps via targeted gap questions using Feynman framing ("explain X as you'd teach it") — teaching-level answers earn `[✓]`, surface-level answers stay `[~]`

**`/ramp:tree`** is a dumb read-only viewer. It reads `~/.claude/knowledge-graphs/[topic].md` and displays it. No inference, no writes.

**`/ramp:review`** is a focused spaced repetition command. It reads due `[✓]` nodes, steps through them one at a time, applies the qualitative rubric, updates `| next:` fields, and awards XP for passes.

**Three-layer tree architecture** (maps to Claude Code's native scope model):

| Tree layer | Claude Code scope | Location | Git? | Phase 4 |
|-----------|------------------|----------|------|---------|
| **Personal global** | User | `~/.claude/knowledge-graphs/[topic].md` | No | option `a` |
| **Team** | Project | `.claude/knowledge-graphs/[topic].md` | Yes | option `d` |
| **Local** | Local | `.claude/knowledge-graphs/local/[topic].md` | No (gitignored) | option `e` |

Merge priority: Local → Team → Personal. A local `[✓]` upgrades anything; nothing downgrades a `[✓]`. `/ramp:up` reads all three layers in Phase 2 and merges before output. Note: Claude Code does not walk up the directory tree — a `.claude/` at a parent level is treated as the project scope for sessions launched there.

## Topics

Topic schemas live in `topics/` — `/ramp:up` discovers them at runtime by scanning that directory. To add a custom topic: create `topics/[name].md` following the format in any existing file.

**Core (meta-topic + sub-topics):**
`claude-code` (81 nodes) — full Claude Code curriculum, sources all five sub-topics:
`getting-started` · `build` · `configuration` · `deployment` · `administration`

**Standalone:**
`best-practices` (15 nodes) — CLAUDE.md design, config, session hygiene
`mcp-development` (29 nodes) — building MCP servers from fundamentals to production
`anthropic-api` (18 nodes) — Claude API from basic completions to tool use loops
`claude-code-internals` (5 nodes) — empirically-verified Claude Code behaviors not in official docs

## Knowledge graph file

**Location:** `~/.claude/knowledge-graphs/[topic].md` (global, personal — follows the developer across all projects)

**Format:** YAML frontmatter (machine-parseable) + Markdown body (human-readable).
Full annotated example: `docs/tree-format.md`

**Status + TYPE fields:** `[✓|artifact]`, `[✓|exercise]`, `[✓|historical]`, `[~|reported]`, `[ ]`. Type records how mastery was demonstrated.

**Review field:** `| next: YYYY-MM-DD [LN]` on `[✓]` nodes only. Encodes spaced repetition schedule.

**Version migration:** v1 files have all `[✓]` treated as `[✓|historical]`; v2 files get `| next:` fields added. Both upgrade to version 3 on next write with `xp:` computed.

