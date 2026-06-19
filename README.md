<p align="center">
  <!-- LOGO: drop a hosted banner/glyph here later, e.g. <img src="docs/assets/ramp.png" width="120"> -->
</p>

<h1 align="center">ramp</h1>

<p align="center"><em>Adaptive, repo-grounded learning mode for Claude Code — it measures what you can <strong>do</strong>, not what you've clicked through.</em></p>

<p align="center">
  <a href="https://github.com/gf-labs/ramp"><img src="https://img.shields.io/badge/version-1.0.0-3b82f6?style=flat-square" alt="version"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-22c55e?style=flat-square" alt="license"></a>
  <img src="https://img.shields.io/badge/Claude_Code-plugin-d97757?style=flat-square&logo=anthropic&logoColor=white" alt="Claude Code plugin">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/topics-5-6366f1?style=flat-square" alt="topics">
</p>

<p align="center">Built by <a href="https://github.com/berniegreen">Bernie Green</a> · <a href="https://github.com/gf-labs">Greenfield Labs</a></p>

---

## Why this exists

Claude Code adoption stalls for a predictable reason: the documentation is complete, but it doesn't adapt to *you* — your codebase, your current level, what you've already demonstrated. Most developers plateau at basic edits and multi-file changes. Hooks, worktrees, custom agents, MCP servers, and pipeline integration stay unexplored. The capability gap compounds.

`/ramp:up` solves this. Run it in any repo. It scans your environment — not just the codebase, but your Claude Code configuration, git history, session history, and prior progress. It asks at most 2–3 targeted questions about things that can't be detected. Then it delivers a personalized, repo-grounded learning path and stays engaged as your co-pilot for the rest of the session.

**It's not a report. It's a mode.**

> **For teams, this is an onboarding engine.** Companies deploy `ramp` as a project-level command so new engineers ramp up on Claude Code, the codebase, *and* the team's workflows from day one — starting from what each person already knows. Solo devs use it to level up. See [Company deployment](#company-deployment).

---

## Quickstart

```
/plugin marketplace add gf-labs/gfl-marketplace
/plugin install ramp@gfl-marketplace
```

Then, in any repo:

```
/ramp:up
```

That's it. `ramp` detects your level, renders your personalized knowledge graph, and hands you your first mastery mission grounded in the actual files in front of you.

<!-- DEMO GIF: /ramp:up first run — scan → graph → first mission, ~25s asciinema -->

---

## The commands

Seven commands, all namespaced `/ramp:*`. `up` is the engine; the rest read, reinforce, and maintain your graph.

| Command | What it does |
|---------|--------------|
| `/ramp:up [topic]`        | **Learning mode.** Scans your environment, assesses your level, delivers a repo-grounded path, and co-pilots the session |
| `/ramp:tree [topic\|all]`  | Read-only view of your knowledge graph — no inference, no writes |
| `/ramp:review [topic]`    | Spaced-repetition review of `[✓]` nodes due today — pass to advance, fail to reset |
| `/ramp:cheatsheet [topic]`| A scannable personal reference built from your own evidence trails |
| `/ramp:pin [topic]`       | Mid-session checkpoint — status, save demonstrated nodes, optional MEMORY snapshot |
| `/ramp:wrap [topic]`      | End-of-session harvest — upgrade nodes, update the review schedule, optional snapshot |
| `/ramp:ingest [topic] [src]` | Generate a new topic schema from an external source — a course curriculum, API docs, or a spec (PDF / URL / file) |

```
/ramp:up                                            # default topic: claude-code
/ramp:up I'm a new backend engineer joining the team
/ramp:up mcp-development I'm building a server
/ramp:up which skills apply to writing a good hook? # consultant mode, mid-session
```

---

## Design principles

**Detect before interrogating.** Over 80 shell commands run at invocation — CLAUDE.md content, hook configs, MCP servers, worktree count, session history, headless invocations. By the time you see a question, `/ramp:up` has already determined your level and identified your gaps. You answer at most three questions, and they're specific.

**Demonstrated over claimed.** The graph distinguishes `[✓]` (demonstrated) from `[~]` (self-reported). A hook in `settings.json` is `[✓|artifact]`. Saying "yes, I've used hooks" is `[~|reported]`. A `[✓]` requires at least one verifiable detail — a flag, an observed behavior, a tradeoff navigated. The difference between "I've heard of hooks" and "I have a PostToolUse hook that fires my linter" is the entire gap between knowledge and practice.

**Mastery missions, not checklists.** Every node has a falsifiable mastery criterion and a repo-grounded exercise. Not "run your tests" — "run `pytest tests/` on `auth_service.py` and interpret the failures."

**Dependency-gated progression.** You don't reach Agents until you've demonstrated Code Changes. The gates *are* the pedagogy.

**Session-persistent, topic-namespaced.** Graphs live at `~/.claude/knowledge-graphs/[topic].md` and follow you across every repo. Returning users with a fresh graph (≤ 7 days) skip questions entirely. Progress is never lost.

**Spaced repetition.** `[✓]` nodes carry a `| next: YYYY-MM-DD [LN]` review schedule (1d → 3d → 7d → 21d → 60d → permanent). `/ramp:review` steps through due nodes one at a time. Pass = advance + XP. Fail = reset to L1.

**Engine / curriculum separation.** `/ramp:up` is topic-agnostic. The curriculum — nodes, detection signals, gap questions, mastery criteria, doc links — lives in schema files under `topics/`. Adding a topic means writing one file. The engine never changes.

---

## Topics

| Topic | Command | Nodes | Focus |
|-------|---------|-------|-------|
| `claude-code` *(default)*   | `/ramp:up`                  | 81  | Claude Code's feature surface — a meta-topic sourcing 5 sub-topics |
| `best-practices`            | `/ramp:up best-practices`   | 15  | CLAUDE.md design, configuration patterns, session hygiene |
| `mcp-development`           | `/ramp:up mcp-development`   | 29  | Building MCP servers: tools, resources, prompts, distribution |
| `anthropic-api`             | `/ramp:up anthropic-api`    | 18  | Claude API: completions, tool use, agentic loops, production patterns |
| `claude-code-internals`     | `/ramp:up claude-code-internals` | 5 | Empirically-verified, undocumented Claude Code behaviors |
| *(your topic)*              | `/ramp:up [topic]`          | any | Install a schema → it just works |

The `claude-code` meta-topic spans five sub-topics — **Getting Started · Build · Configuration · Deployment · Administration** — gated so you progress through them in order.

---

## Three modes

`/ramp:up` adapts to what it finds when you run it.

| Context | What happens |
|---------|-------------|
| **Existing repo** | Scans codebase + env + history → renders the graph → delivers mastery missions → stays engaged as session co-pilot |
| **Empty / new repo** | Asks what to build → builds it with you → narrates every Claude Code capability as it's used → renders the graph from what was demonstrated |
| **Directory of repos** | Surveys all repos (name, stack, last activity) → you pick a focus → proceeds as single-repo mode |

---

## The knowledge graph

81 nodes for `claude-code`, every one grounded in Claude Code's actual feature surface.

```
[Getting Started] Core Foundations
    [✓] What Claude Code does and when to use it
    [✓] How Claude Code uses computers (tool loop)
    [★] Memory types and scope hierarchy

[Build] Agents and Orchestration
    [✓] Subagent basics: spawning and tool access
    [~] Foreground vs. background subagents
    [★] Custom subagent definitions (.claude/agents/)

[Build] Hooks System
    [✓] PostToolUse hooks (linting, reactions)
    [★] PreToolUse hooks (validation, blocking)

[Build] Headless and MCP
    [~] Headless mode (-p flag, non-interactive)
    [ ] MCP: configure and use servers

[Configuration] Settings Fundamentals
    [✓] Settings scope hierarchy: global, project, local

[·] Deployment        (unlock: complete Configuration)
[·] Administration    (unlock: complete Deployment)

Your frontier: → Memory types [★]  → CLAUDE.md as living memory [★]  → PreToolUse hooks [★]
Level: Builder — hooks and commands demonstrated, moving into orchestration
```

Marker key: `[✓]` demonstrated · `[~]` self-reported · `[ ]` not yet · `[★]` mastery target · `[·]` locked

Each `[★]` becomes a **mastery mission** — a falsifiable criterion plus a repo-grounded exercise using your real file names and toolchain.

> View it any time with `/ramp:tree` (read-only), or build a personal reference from your evidence trails with `/ramp:cheatsheet`. See [`docs/tree-format.md`](docs/tree-format.md) for the annotated graph format.

### Spaced-repetition review

`/ramp:review` runs a focused session over demonstrated `[✓]` nodes that are due today — no assessment, no new skills, just reinforcement.

- Finds all `[✓]` nodes where `next: YYYY-MM-DD ≤ today`
- Asks one targeted question per node
- **Pass** (specific detail) → advance one level, next date from the interval ladder
- **Fail** (vague or none) → reset to L1, review again tomorrow

Interval ladder: L1 = 1d · L2 = 3d · L3 = 7d · L4 = 21d · L5 = 60d · L6 = permanent.

---

## Company deployment

`ramp` is built to onboard engineers. Two artifacts work together — one static, one active.

### Two tools, two purposes

| | `ONBOARDING.md` | Custom topic schema |
|--|---|---|
| **Format** | Static markdown doc | Active knowledge-graph session |
| **When used** | Day 1: "how do I run this?" | First week: guided onboarding with exercises |
| **Personalized?** | No — same doc for everyone | Yes — starts from what the dev already knows |
| **Progress tracking** | No | Yes — evidence trails, XP, spaced repetition |
| **Generated by** | `/ramp:up` Phase 4 option b | `/ramp:up [your-topic]` |
| **Committed to repo?** | Yes (optional) | Schema yes; knowledge graphs stay personal |

Use both: `ONBOARDING.md` as the quick-start reference, a custom topic for the active ramp-up.

### Step 1 — Commit the commands

Copy the command files into your team repo's `.claude/commands/` so engineers get them on clone:

```bash
cp commands/up.md     /your-team-repo/.claude/commands/ramp.md
cp commands/tree.md   /your-team-repo/.claude/commands/tree.md
cp commands/review.md /your-team-repo/.claude/commands/review.md
```

Knowledge graphs (`~/.claude/knowledge-graphs/`) stay personal — they live on each developer's machine, not in the repo.

### Step 2 — Create a custom topic schema *(recommended)*

Add `.claude/knowledge-graphs/schemas/[your-topic].md` to the team repo. This is the curriculum for onboarding to *this* codebase — nodes, detection signals, gap questions, and mastery criteria specific to your project.

```
.claude/
└── knowledge-graphs/
    └── schemas/
        └── acme-onboarding.md   ← commit this
```

Example nodes: `[ROOT] Environment setup` (make setup, .env, local run), `[A] Architecture` (data flow, service ownership), `[B] Dev workflow` (PR process, test suite, deploy), `[C] Team practices` (escalation, monitoring). See [`topics/claude-code.md`](topics/claude-code.md) for the full schema format — once committed, engineers clone and run `/ramp:up acme-onboarding`.

### Step 3 — Add team context to `CLAUDE.md`

`/ramp:up` reads an `## Onboarding` section and folds it into every session and the generated `ONBOARDING.md`:

```markdown
## Onboarding
- Run `make setup` before anything else
- Read `docs/architecture.md` for system design context
- Auth system owned by @alice, data pipeline by @bob
- Ask in #dev-help — 30-minute rule before escalating
- Deploy: PR → staging → 24h soak → prod
```

After a session, `/ramp:up` also offers to **bootstrap the repo's Claude Code setup** — create a `CLAUDE.md`, add starter hooks, write a custom command — if any are missing.

---

## Install

**From the GFL marketplace (recommended).** `ramp` is published through the [`gf-labs/gfl-marketplace`](https://github.com/gf-labs/gfl-marketplace) catalog, alongside `tools`:

```
/plugin marketplace add gf-labs/gfl-marketplace
/plugin install ramp@gfl-marketplace
```

**From a local clone (dev / offline).** `ramp` is also its own single-plugin marketplace, so you can add the clone directly — note the install name is `ramp@ramp` here, not `@gfl-marketplace`:

```bash
git clone https://github.com/gf-labs/ramp ~/path/to/ramp
```
```
/plugin marketplace add ~/path/to/ramp
/plugin install ramp@ramp
```

Hooks (the passive observer) and topic schemas are set up automatically on first session start. Update with `/plugin update ramp@gfl-marketplace`.

**Add a community topic:**
```bash
cp your-topic.md ~/.claude/knowledge-graphs/schemas/your-topic.md
/ramp:up your-topic
```

---

## The passive observer

A hook watches every Claude Code session and upgrades `~/.claude/knowledge-graphs/claude-code.md` whenever it detects skill evidence — no need to run `/ramp:up`. `scripts/skill-observer.py` listens on three events (`PostToolUse`, `WorktreeCreate`, `SessionStart`) and detects, for example:

- `git worktree add` (or a `WorktreeCreate` event) → Worktrees `[✓|historical]`
- `claude -p` → Headless mode `[✓|historical]`
- Writes to `.claude/agents/*.md` → Custom subagent definitions `[✓|historical]`
- Writes to `settings.json` with a `hooks` key → PostToolUse hooks `[✓|historical]`
- Writes to `settings.json` with an `mcpServers` key → MCP servers `[✓|historical]`

> **What it can't see:** built-in CLI commands (`/help`, `/compact`, `/usage`, `/doctor`) never enter the tool loop, so no hook fires. Those are captured through `/ramp:up`'s assessment, which can promote a `[~|reported]` node to `[✓]`.

The observer ships in the plugin and registers automatically on install. Verify it with `cat ~/.claude/knowledge-graphs/claude-code.md` after a session.

---

## MCP server — `knowledge-graph`

`mcp/server.py` is an optional MCP server that gives `/ramp:up` structured read/write access to your graphs — atomic saves, cross-device sync, and a clean upgrade path to team and org layers.

**Why use it.** Without the MCP, `/ramp:up` reads graphs via a bash `cat` and writes via the `Write` tool. With it, reads and writes go through structured tools — enabling swappable backends (local files → hosted API) without changing `up.md`.

| Tool | Description |
|------|-------------|
| `read_graph(topic)`               | Read a knowledge graph — returns markdown |
| `save_graph(topic, content)`      | Atomic write + optional backend sync |
| `list_topics()`                   | All topics with level and XP — returns JSON |
| `get_benchmarks(topic)`           | Personal stats; team/org when a backend is configured |
| `export_delta(topic, since_date)` | Demonstrated nodes since a date — for team sharing |

**Setup.** Create the repo-local virtualenv (the system `python3` ships a conflicting `mcp` stub, so the server must run from `.venv`):

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

> In a normal plugin install, the `setup-mcp.py` SessionStart hook registers the server for you (`claude mcp add -s user`). The block below is for manual registration.

Add to `~/.claude/.mcp.json` (global) — point `command` at the venv python, or use `./mcp/start.sh`, which resolves it for you:

```json
{
  "mcpServers": {
    "knowledge-graph": {
      "type": "stdio",
      "command": "/absolute/path/to/ramp/.venv/bin/python3",
      "args": ["/absolute/path/to/ramp/mcp/server.py"]
    }
  }
}
```

**Hosted backend (team / org).** Set `KNOWLEDGE_GRAPH_API_URL` and the server proxies `read_graph`/`save_graph` to `GET/PUT /graphs/{topic}` and `get_benchmarks` to `GET /benchmarks/{topic}`. That unlocks cross-device sync, team skill matrices, and org dashboards — and it falls back to local files if the backend is unreachable.

---

## Schemas vs. knowledge graphs

Two different things live in `~/.claude/knowledge-graphs/`:

| | Location | Contains | Created by |
|--|----------|----------|------------|
| **Schema** | `…/schemas/[topic].md` | Curriculum blueprint: nodes, detection signals, gap questions, mastery criteria, doc links | Plugin install (auto-symlinked from `topics/` on first session start) |
| **Knowledge graph** | `…/[topic].md` | *Your* progress: node statuses, evidence trails, review schedule, XP | `/ramp:up` |

One schema per topic. `topics/claude-code.md` → `schemas/claude-code.md` → used by `/ramp:up`; your progress lands at `~/.claude/knowledge-graphs/claude-code.md`.

---

## Repo structure

```
ramp/
├── .claude-plugin/
│   ├── plugin.json        # Plugin manifest (name, version, description)
│   └── marketplace.json   # Single-plugin marketplace catalog
├── commands/              # Command source — up, tree, review, cheatsheet, pin, wrap, ingest
├── topics/                # Schema source → symlinked to ~/.claude/knowledge-graphs/schemas/
├── hooks/hooks.json       # Plugin hooks (PostToolUse + WorktreeCreate + SessionStart)
├── scripts/               # skill-observer.py, file-size-warn.py, setup-mcp.py
├── mcp/                   # knowledge-graph MCP server (server.py, start.sh)
└── docs/                  # tree-format.md, docs-map.md, tools-wrap-reference.md
```

### Working on ramp itself

Load the plugin live from the source repo — no install, no cache rebuild:

```bash
claude --plugin-dir /path/to/ramp
```

`SessionStart` fires and symlinks `topics/` → `~/.claude/knowledge-graphs/schemas/` automatically. Use `/reload-plugins` to pick up minor changes. To refresh the *installed* (cached) version after editing commands, remove and re-add the marketplace, then reinstall — `/plugin install` skips silently if the plugin is already present, and `/reload-plugins` reads the cache, not the source. The `--plugin-dir` workflow always reads live and sidesteps this entirely.

---

## Built with Claude Code

`ramp` is a working demonstration of Claude Code's extension model — a stateful, adaptive, curriculum-aware learning system built **entirely from Markdown and a little Python**, with no application runtime. The mechanisms at work:

- **`!bash` injection** — the 80+ scanning commands run *before* Claude reads a single token, injecting structured context. Pre-computation, not agentic tool use: fast, deterministic, cheap.
- **Topic-schema loading** — a bash command reads the requested topic from `$ARGUMENTS` and `cat`s the matching schema as static text. The engine (`up.md`) holds zero topic-specific content.
- **`$ARGUMENTS`** — the topic keyword plus free-form context the user types after `/ramp:up`.
- **`allowed-tools`** — scoped to `Read, Glob, Grep, Bash, Write, Edit` so Claude can navigate the repo, run exercises, write `ONBOARDING.md`, and update the graph — without unlimited access.
- **Persistent file I/O** — `~/.claude/knowledge-graphs/[topic].md` is YAML frontmatter + Markdown: human-readable, machine-parseable, shareable by copy-paste.
- **Spaced repetition as pure file I/O** — `| next: YYYY-MM-DD [LN]` fields encode the schedule. No database, no external state.
- **Hooks** — a passive observer across `PostToolUse`, `WorktreeCreate`, and `SessionStart` updates the graph with zero user action.
- **MCP server** — an optional structured backend that makes the storage layer swappable.
- **Branch logic in natural language** — the phase structure (detect → assess → infer → output → artifacts) is expressed as instructions. There's no interpreter, no state machine. The prompt *is* the program.

This is the [custom slash commands](https://docs.anthropic.com/en/docs/claude-code/slash-commands) feature pushed to its edge.

---

## Roadmap

Topics planned but not yet built:

| Topic | Focus |
|-------|-------|
| `claude-cli`      | CLI flags (`-p`, `--model`, `--output-format`, `--resume`), headless scripting, CI |
| `claude-settings` | settings.json, permissions, hook syntax, MCP config, CLAUDE.md hierarchy |
| `claude-features` | In-app modes: plan mode, `/compact`, memory, subagents, skills |
| `bash` · `react` · `typescript` · `git` · `dsa` | General developer topics |

To contribute a schema, follow the format in [`topics/claude-code.md`](topics/claude-code.md) — or generate a first draft with `/ramp:ingest`.

---

## License

[MIT](./LICENSE) © 2026 Greenfield Labs
