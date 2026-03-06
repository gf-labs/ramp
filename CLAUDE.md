# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`sup` activates a **learning mode** — Claude becomes a co-pilot for ramping developers up on Claude Code as an organizational tool, the codebase, and the team's workflows (commits, PRs, testing, CI). It scans the environment, assesses the user, delivers a personalized knowledge tree and learning path, then stays engaged to work through exercises together. Writes an `ONBOARDING.md` artifact and updates `~/.claude/knowledge-trees/[topic].md`.

Companies deploy it as a project-level command for engineer onboarding. Solo devs use it to level up.

### Three operating modes

- **Mode A (empty repo)**: Claude asks what to build, then builds it while narrating every Claude Code capability it uses
- **Mode B (single repo)**: Scans codebase → assesses user → integrated learning path grounded in the actual repo
- **Mode C (multi-repo directory)**: Surveys all repos, user picks focus, then proceeds as Mode B

## Structure

```
commands/sup.md              # Adaptive onboarding command — manages knowledge tree
commands/tree.md             # Read-only knowledge tree viewer
commands/review.md           # Spaced repetition review command
commands/cheatsheet.md       # Personal reference: demonstrated skills + evidence trails
.claude-plugin/plugin.json   # Plugin manifest (name, version, description)
hooks/hooks.json             # Plugin hook config (PostToolUse + WorktreeCreate + SessionStart)
topics/claude-code.md        # Claude Code meta-topic (sources 5 sub-topics, 71 nodes total)
topics/getting-started.md    # Getting started sub-topic (12 nodes)
topics/build.md              # Build sub-topic (22 nodes)
topics/configuration.md      # Configuration sub-topic (13 nodes)
topics/deployment.md         # Deployment sub-topic (11 nodes)
topics/administration.md     # Administration sub-topic (13 nodes)
topics/best-practices.md     # Best practices topic schema (15 nodes)
topics/mcp-development.md    # MCP development topic schema (20 nodes)
topics/anthropic-api.md      # Anthropic API topic schema (18 nodes)
scripts/skill-observer.py    # Passive observer hook (PostToolUse + WorktreeCreate + SessionStart)
scripts/file-size-warn.py    # PostToolUse hook — warns when .md files exceed 600 lines
mcp/server.py                # knowledge-tree MCP server (read/write trees; swappable backend)
README.md                    # Install instructions, modes, company deployment guide
```

*This listing is maintained manually — update it when files are added or renamed.*

**Note:** `commands/` at root is the source of truth for command files — used by the plugin system and company deployment (copy to team repo's `.claude/commands/`). `.claude/commands/` is gitignored.

No build steps, no dependencies, no runtime. Commands are pure prompt engineering in Markdown files.

## Customization

**Two layers of company customization:**

**1. `## Onboarding` in CLAUDE.md** — team context injected into every `/sup` session and the generated `ONBOARDING.md`:
```markdown
## Onboarding
- Run `make setup` before anything else
- Read `docs/architecture.md` for system design context
- Auth system owned by @alice, data pipeline by @bob
- Ask in #dev-help — 30-minute rule before escalating
```

**2. Custom topic schema** — a full project-specific curriculum committed to `.claude/knowledge-trees/schemas/[topic].md`. Engineers run `/sup [topic]` and get a personalized onboarding path grounded in the actual codebase, with exercises, evidence tracking, and spaced repetition. No separate install step — the schema is discovered automatically from the project-local path. See `topics/claude-code.md` for the schema format.

## Knowledge tree

Both `/sup` and `/tree` render and update a knowledge tree — a structured map of a developer's Claude Code capabilities.

**Tree structure (71 nodes across 5 sub-topics):**
- **[Getting Started]** Core Foundations, Working Effectively, Best Practices — what Claude Code is, tool loop, memory, workflow patterns (12 nodes)
- **[Build]** Agents and Orchestration, Skills and Plugins, Hooks System, Headless and MCP — subagents, slash commands, hooks, headless mode (22 nodes)
- **[Configuration]** Settings Fundamentals, Permissions and Security, Interface Customization — settings hierarchy, allow/deny rules, keybindings (13 nodes)
- **[Deployment]** Cloud Provider Integration, Network and Infrastructure, Deployment Patterns — Bedrock, Vertex, Foundry, LLM gateways, CI/CD (11 nodes)
- **[Administration]** Setup and Authentication, Data and Compliance, Cost and Usage Management — org setup, ZDR, analytics, chargeback (13 nodes)

**Status markers:**
- `[✓]` **Demonstrated** — artifact found, exercise completed, or historical evidence verified
- `[~]` **Self-reported** — claimed but not corroborated by artifact or exercise (weaker signal)
- `[ ]` not yet · `[★]` mastery target (frontier) · `[·]` locked

**Spaced repetition:** `[✓]` nodes carry a `| next: YYYY-MM-DD [LN]` field (interval ladder: L1=1d, L2=3d, L3=7d, L4=21d, L5=60d, L6=permanent). `/sup` surfaces due nodes in Phase 3. `/review` runs focused review sessions.

**Per-node doc links:** Each node in topic schemas has a `source_url` column. `/sup` surfaces these as `**Reference:** [official docs](url)` in mastery mission exercises.

**XP system:** Each demonstrated `[✓]` node earns XP by branch tier (ROOT=10, A=15, B=20, C=25, D=35, E=50). `[~]` = half XP. Total stored as `xp:` in frontmatter. Displayed as "Level: Builder · 240 XP". `/review` pass awards a per-node XP bonus.

**Adaptive pacing:** Phase 3 output scales with tier. Explorer (~20-30 lines, 1 skill), Builder (~50-60 lines, 2 skills), Practitioner/Expert (~80-100+ lines, 3 skills). Returning users with a fresh tree (≤7 days) skip gap questions entirely — straight to Phase 3.

**Demonstration types** (each node has one or more):
- **Artifact** — a file/config exists, auto-detected by bash scan
- **Exercise** — do something live in the session
- **Qualitative** — answer a targeted question; Claude applies an explicit rubric
- **Historical** — evidence from past work (git log, session files, worktree directories)

**Inference priority (highest to lowest, used only by `/sup`):**
1. Environmental signals — CLAUDE.md content, hooks/MCP in settings.json, commands in `.claude/commands/`, history scans
2. Saved tree file — `~/.claude/knowledge-trees/[topic].md` persists progress from prior sessions; `[✓]` nodes are never downgraded
3. Self-reported assessment — fills gaps via targeted gap questions using Feynman framing ("explain X as you'd teach it") — teaching-level answers earn `[✓]`, surface-level answers stay `[~]`

**`/tree`** is a dumb read-only viewer. It reads `~/.claude/knowledge-trees/[topic].md` and displays it. No inference, no writes.

**`/review`** is a focused spaced repetition command. It reads due `[✓]` nodes, steps through them one at a time, applies the qualitative rubric, updates `| next:` fields, and awards XP for passes.

**Three-layer tree architecture** (maps to Claude Code's native scope model):

| Tree layer | Claude Code scope | Location | Git? | Phase 4 |
|-----------|------------------|----------|------|---------|
| **Personal global** | User | `~/.claude/knowledge-trees/[topic].md` | No | option `a` |
| **Team** | Project | `.claude/knowledge-trees/[topic].md` | Yes | option `d` |
| **Local** | Local | `.claude/knowledge-trees/local/[topic].md` | No (gitignored) | option `e` |

Merge priority: Local → Team → Personal. A local `[✓]` upgrades anything; nothing downgrades a `[✓]`. `/sup` reads all three layers in Phase 2 and merges before output. Note: Claude Code does not walk up the directory tree — a `.claude/` at a parent level is treated as the project scope for sessions launched there.

## Topics

| Topic | File | Nodes | Focus |
|-------|------|-------|-------|
| `claude-code` | `topics/claude-code.md` | 71 | Claude Code features — meta-topic sourcing 5 sub-topics |
| ↳ `getting-started` | `topics/getting-started.md` | 12 | Foundations: tool loop, memory, workflow patterns |
| ↳ `build` | `topics/build.md` | 22 | Agents, skills, hooks, headless mode, MCP |
| ↳ `configuration` | `topics/configuration.md` | 13 | Settings hierarchy, permissions, interface customization |
| ↳ `deployment` | `topics/deployment.md` | 11 | Bedrock, Vertex, Foundry, network, CI/CD |
| ↳ `administration` | `topics/administration.md` | 13 | Org setup, auth, security, data, costs, analytics |
| `best-practices` | `topics/best-practices.md` | 15 | CLAUDE.md design, config, session hygiene |
| `mcp-development` | `topics/mcp-development.md` | 20 | Building MCP servers from fundamentals to production |
| `anthropic-api` | `topics/anthropic-api.md` | 18 | Claude API from basic completions to tool use loops |

## Knowledge tree file

**Location:** `~/.claude/knowledge-trees/[topic].md` (global, personal — follows the developer across all projects)

**Format:** YAML frontmatter (machine-parseable) + Markdown body (human-readable):

```markdown
---
version: 3
topic: claude-code
user: [Your Name]
email: [your@email.com]
updated: 2026-03-04
level: Builder
---

# Claude Code Knowledge Tree

*[✓] Demonstrated · [~] Self-reported · [ ] Not yet · [★] Mastery target · [·] Locked*

## [ROOT] Configure Claude
- [✓|artifact] CLAUDE.md with project guidance — sup, 2026-03-04: 80+ lines | next: 2026-03-05 [L1]
- [✓|artifact] settings.json / settings.local.json exists — sup, 2026-03-04: global + project | next: 2026-03-05 [L1]
- [~|reported] Model or budget settings configured
- [ ] /memory audit and CLAUDE.md hierarchy
...

## Frontier
- Context window and /compact usage — has used /compact deliberately; can explain difference

## Notes
<!-- personal notes -->
```

**Status + TYPE fields:** `[✓|artifact]`, `[✓|exercise]`, `[✓|historical]`, `[~|reported]`, `[ ]`. Type records how mastery was demonstrated.

**Review field:** `| next: YYYY-MM-DD [LN]` on `[✓]` nodes only. Encodes spaced repetition schedule.

**Version migration:** v1 files have all `[✓]` treated as `[✓|historical]`; v2 files get `| next:` fields added. Both upgrade to version 3 on next write with `xp:` computed.

## How slash commands work

Claude Code discovers `.md` files in `.claude/commands/` (project-level) or `~/.claude/commands/` (global) and exposes them as `/` commands. The filename becomes the command name. YAML frontmatter sets `description`, `argument-hint`, `allowed-tools`, and `model`.

Key mechanisms used in `sup.md`:
- `$ARGUMENTS`: replaced with whatever the user types after `/sup`
- `!bash-command`: executes shell commands at invocation and injects their output into the prompt (used for context collection: git log, file listing, tech stack detection, hooks/MCP config, etc.)
- `@filename`: injects file contents (alternative to `!cat filename`)
- `allowed-tools`: grants Claude permission to use Read, Glob, Grep, Bash, Write, Edit during the session
