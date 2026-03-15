---
topic: build
version: 1
source_url: https://code.claude.com/docs/en/sub-agents
description: Building with Claude Code — subagents, agent teams, plugins, skills, hooks, headless mode, MCP, and output styles.
---

# Build Knowledge Graph Schema

This file defines the curriculum for the `build` topic. Covers the "Build with Claude Code" docs section: sub-agents, agent-teams, plugins, skills, output-styles, hooks-guide, headless, mcp, troubleshooting.

---

## Node definitions

31 nodes across 6 branches.

### [ROOT] Agents and orchestration (always unlocked — 5 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|-----------|
| Subagent basics: spawning and tool access | Has used a task where Claude spawned a subagent (via the Agent tool); can describe what tools subagents have access to and how they differ from the parent session | Historical / Exercise | subagent sessions > 3 → `[✓\|historical]`; > 0 → `[~\|historical]` | https://code.claude.com/docs/en/sub-agents |
| Foreground vs. background subagents | Can explain the difference: foreground subagents block the parent and return results; background subagents run concurrently and the parent continues; knows when each is appropriate | Qualitative | subagent sessions > 10 → `[~\|historical]` | https://code.claude.com/docs/en/sub-agents |
| Agent teams: orchestration patterns | Has set up or observed a task where multiple agents work in parallel on separate concerns; can describe the orchestrator/worker pattern | Historical / Exercise | subagent sessions > 20 → `[~\|historical]` | https://code.claude.com/docs/en/agent-teams |
| Custom subagent definitions (.claude/agents/) | Created at least one custom subagent in `.claude/agents/` or `~/.claude/agents/`; can describe its system prompt, tool restrictions, and when to invoke it | Artifact | custom agent definitions > 0 → `[✓\|artifact]` | https://code.claude.com/docs/en/sub-agents |
| Worktrees for parallel development | Ran two Claude sessions simultaneously on separate branches; knows `git worktree add` and how this enables isolation without context pollution | Historical / Exercise | git worktrees > 1 → `[✓\|historical]` | https://code.claude.com/docs/en/agent-teams |

### [A] Skills and plugins (9 nodes, unlocks when ROOT ≥ 2 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|-----------|
| Skills (slash commands): creation and syntax | Created a custom slash command file in `.claude/commands/`; knows frontmatter fields (description, allowed-tools, argument-hint) | Artifact | `.claude/commands/` count ≥ 1 → `[✓\|artifact]` | https://code.claude.com/docs/en/skills |
| Skill mechanics: $ARGUMENTS, !bash, @file | Has written a skill that uses at least two of: `$ARGUMENTS`, `!bash-command`, `@filename`; can describe what each injects into context | Artifact | skill files with bash injection > 0 → `[✓\|artifact]` | https://code.claude.com/docs/en/skills |
| Skill and command composition | Has composed skills: a skill that calls another, passes `$ARGUMENTS` through, or invokes a subagent; or chains multiple data sources in one command | Artifact | command files with both `!` and `@` usage → `[✓\|artifact]` | https://code.claude.com/docs/en/skills |
| Output styles: controlling response format | Has used output style configuration to change how Claude responds (concise, verbose, structured); knows `output-styles` frontmatter or prompt patterns | Exercise / Qualitative | None | https://code.claude.com/docs/en/output-styles |
| Plugin discovery and installation | Has installed a plugin via the marketplace (`/plugin marketplace add` or `--plugin-dir`); knows plugin namespacing (`/plugin-name:command`) | Historical / Exercise | `enabledPlugins` in settings → `[✓\|artifact]` | https://code.claude.com/docs/en/discover-plugins |
| Plugin manifest (plugin.json) | Has created or read a `plugin.json` manifest; understands name, version, commands, hooks, and the plugin directory structure | Artifact | `.claude-plugin/plugin.json` exists → `[✓\|artifact]` | https://code.claude.com/docs/en/plugins |
| context: fork for skill isolation | Knows that adding `context: fork` to a skill's frontmatter runs the skill in an isolated forked context, preventing verbose output or intermediate state from polluting the main session; can describe a case where fork is the right choice (e.g., long research skills, output-heavy scripts) | Qualitative / Artifact | skill files with `context: fork` → `[✓\|artifact]` | https://docs.anthropic.com/en/docs/claude-code/skills |
| argument-hint frontmatter for required parameter prompting | Has used `argument-hint:` in a skill's frontmatter to prompt the user for required input before the skill runs; knows what the hint text looks like in the Claude UI | Artifact | skill files with `argument-hint:` → `[✓\|artifact]` | https://docs.anthropic.com/en/docs/claude-code/skills |
| .claude/rules/ with YAML paths: glob patterns for conditional rule loading | Knows that files placed in `.claude/rules/` can include a `paths:` key with glob patterns so the rule is only injected into context when Claude is working in matching paths; understands the use case — database migration rules active only when editing `migrations/` | Qualitative / Artifact | `.claude/rules/` directory with YAML files → `[~\|artifact]` | https://docs.anthropic.com/en/docs/claude-code/memory |

### [B] Hooks system (6 nodes, unlocks when Branch A ≥ 3 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|-----------|
| PreToolUse hooks (validation, blocking) | Has configured a PreToolUse hook; knows exit code protocol: 0 = allow, 2 = block with message to Claude; has observed a blocked tool call | Artifact | `hooks.PreToolUse` in settings → `[✓\|artifact]` | https://code.claude.com/docs/en/hooks |
| PostToolUse hooks (linting, reactions) | Has a PostToolUse hook that fires after edits or commands; knows its stdout is injected back into Claude's context as a new observation | Artifact | `hooks.PostToolUse` in settings → `[✓\|artifact]` | https://code.claude.com/docs/en/hooks |
| Stop and Notification hooks (session alerts) | Has a Stop or Notification hook; can explain when each fires (Stop = Claude done, Notification = idle alert); has received a notification from it | Artifact | `hooks.Stop` or `hooks.Notification` in settings → `[✓\|artifact]` | https://code.claude.com/docs/en/hooks |
| Hook handler scripts (stdin, exit codes, response) | Has written a hook handler script that reads JSON from stdin, parses the tool event, processes it, and exits with the correct code; knows the full stdin schema (hook_event_name, tool_name, tool_input) | Artifact / Exercise | repo has a hook handler script with stdin JSON parsing → `[~\|artifact]` | https://code.claude.com/docs/en/hooks |
| Scoped hooks (in skill or agent frontmatter) | Has defined a `hooks:` block inside a `.claude/commands/*.md` or `.claude/agents/*.md` file — not just in global settings; knows how scope affects which sessions the hook fires in | Artifact | `hooks:` key in any command or agent file → `[✓\|artifact]` | https://code.claude.com/docs/en/hooks-guide |
| Hooks guide: design patterns and gotchas | Can describe at least two hooks design patterns (e.g., auto-linting, cost guardrails, notification on stop); knows the main gotchas (async execution, stdout injection timing) | Qualitative | Any hook in settings → `[~\|historical]` | https://code.claude.com/docs/en/hooks-guide |

### [C] Headless and MCP (7 nodes, unlocks when Branch B ≥ 3 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|-----------|
| Headless mode (-p flag, non-interactive) | Has run `claude -p "prompt"` or `claude --print` from a script or terminal; knows it outputs to stdout and exits; can describe when headless beats interactive | Historical / Exercise | headless invocations > 0 → `[✓\|artifact]` | https://code.claude.com/docs/en/headless |
| Piped input and CI integration | Has piped content into claude (`cat file | claude -p "..."`) or used it in a CI step; understands stdin/stdout contract | Exercise / Historical | CI workflow with claude command → `[✓\|artifact]`; headless invocations > 0 → `[~\|historical]` | https://code.claude.com/docs/en/headless |
| --output-format json and --json-schema for structured headless output | Knows the `--output-format json` flag makes headless invocations return structured JSON; knows `--json-schema <file>` constrains the output schema (guaranteed valid against the schema); can describe the CI pipeline pattern: `claude -p "..." --output-format json \| jq '.field'` | Qualitative / Exercise | CI workflows with `--output-format` flag → `[✓\|artifact]` | https://docs.anthropic.com/en/docs/claude-code/cli-reference |
| Built-in tool selection for codebase tasks | Can explain the right tool for each codebase operation: Grep for content patterns (what's in files), Glob for path patterns (which files exist), Read for specific files (when path is known), Edit for targeted changes (smallest diff), Bash only when no dedicated tool applies; knows the incremental understanding pattern — Glob → Read → Grep sequence for unfamiliar codebases | Qualitative | None | https://docs.anthropic.com/en/docs/claude-code/built-in-tools |
| MCP: configure and use servers | Has ≥1 MCP server configured in settings or `.mcp.json`; has made at least one query using an MCP tool; can describe what the server provides | Artifact + Exercise | MCP servers in settings → `[~\|artifact]` | https://code.claude.com/docs/en/mcp |
| MCP project config (.mcp.json) | Has created or used a `.mcp.json` at repo root; understands it is project-scoped (committable, shared with team) vs. personal `settings.json` mcpServers | Artifact | `.mcp.json` exists at repo root → `[✓\|artifact]` | https://code.claude.com/docs/en/mcp |
| Troubleshooting: diagnose and recover | Has used `/doctor` to check environment; can interpret its output; knows how to diagnose a stuck tool call, permission error, or context overflow | Exercise / Qualitative | None | https://code.claude.com/docs/en/troubleshooting |

### [D] Skills distribution and enterprise (2 nodes, unlocks when Branch C ≥ 2 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|-----------|
| Skills distribution via plugins and managed_settings.json | Can explain how to distribute skills org-wide: bundle in a plugin (plugin.json + commands/), distribute via marketplace or --plugin-dir; knows that `managed_settings.json` allows enterprise admins to push settings (including enabledPlugins) to all users without individual configuration | Qualitative / Artifact | `managed_settings.json` in repo → `[✓\|artifact]` | https://docs.anthropic.com/en/docs/claude-code/plugins |
| Skills as custom subagent delegation targets | Can describe wiring a SKILL.md as the target of a custom subagent: the agent's system prompt invokes the skill by name, and the skill's allowed-tools and context constraints apply to that subagent invocation; knows the use case — a specialist subagent that always runs a specific research skill | Qualitative / Artifact | custom agent definitions that reference skills → `[~\|artifact]` | https://docs.anthropic.com/en/docs/claude-code/sub-agents |

### [E] Iterative refinement workflows (2 nodes, unlocks when Branch D ≥ 1 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|-----------|
| Iterative refinement: sequential subagent pattern for test-driven iteration | Can describe the iterative refinement pattern: subagent 1 writes code → subagent 2 runs tests → on failure, coordinator re-delegates to subagent 1 with test output as feedback → repeat until green; knows why sequential ordering is required here (each step depends on the previous result, not parallelizable); contrasts with parallel subagents for independent concerns | Qualitative | None | https://docs.anthropic.com/en/docs/claude-code/sub-agents |
| Interview pattern: structured questions for ambiguous analysis tasks | Can describe the interview pattern: instead of an open-ended "analyze X" task, the coordinator prompts a subagent with structured interview questions ("What are the top 3 risks? What dependencies are involved? What would you need to verify?"); knows that constraint improves output quality in ambiguous analysis tasks by preventing the model from defaulting to the most obvious surface answer | Qualitative | None | https://docs.anthropic.com/en/docs/build-with-claude/agents |

---

## Detection signals

| Collected evidence | Node → status |
|--------------------|---------------|
| subagent sessions > 3 | ROOT: "Subagent basics" → `[✓\|historical]` |
| subagent sessions > 0 (≤3) | ROOT: "Subagent basics" → `[~\|historical]` |
| subagent sessions > 10 | ROOT: "Foreground vs. background subagents" → `[~\|historical]` |
| subagent sessions > 20 | ROOT: "Agent teams: orchestration patterns" → `[~\|historical]` |
| custom agent definitions > 0 | ROOT: "Custom subagent definitions" → `[✓\|artifact]` |
| git worktrees > 1 | ROOT: "Worktrees for parallel development" → `[✓\|historical]` |
| `.claude/commands/` count ≥ 1 | A: "Skills: creation and syntax" → `[✓\|artifact]` |
| skill files with bash injection > 0 | A: "Skill mechanics: $ARGUMENTS, !bash, @file" → `[✓\|artifact]` |
| command files with both `!` and `@` usage | A: "Skill and command composition" → `[✓\|artifact]` |
| `enabledPlugins` in settings | A: "Plugin discovery and installation" → `[✓\|artifact]` |
| `.claude-plugin/plugin.json` exists | A: "Plugin manifest (plugin.json)" → `[✓\|artifact]` |
| `hooks.PreToolUse` in settings | B: "PreToolUse hooks" → `[✓\|artifact]` |
| `hooks.PostToolUse` in settings | B: "PostToolUse hooks" → `[✓\|artifact]` |
| `hooks.Stop` or `hooks.Notification` in settings | B: "Stop and Notification hooks" → `[✓\|artifact]` |
| hook handler script with stdin JSON parsing in repo | B: "Hook handler scripts" → `[~\|artifact]` |
| `hooks:` key in any command or agent file | B: "Scoped hooks" → `[✓\|artifact]` |
| Any hook configured in settings | B: "Hooks guide: design patterns" → `[~\|historical]` |
| headless invocations > 0 | C: "Headless mode" → `[✓\|artifact]`; C: "Piped input and CI" → `[~\|historical]` |
| CI workflow file with `claude` command | C: "Piped input and CI integration" → `[✓\|artifact]` |
| CI workflow or script with `--output-format json` | C: "--output-format json and --json-schema" → `[✓\|artifact]` |
| MCP servers in settings | C: "MCP: configure and use servers" → `[~\|artifact]` |
| `.mcp.json` exists at repo root | C: "MCP project config (.mcp.json)" → `[✓\|artifact]` |
| skill files with `context: fork` | A: "context: fork for skill isolation" → `[✓\|artifact]` |
| skill files with `argument-hint:` | A: "argument-hint frontmatter" → `[✓\|artifact]` |
| `.claude/rules/` directory with YAML files | A: ".claude/rules/ with paths: glob patterns" → `[~\|artifact]` |
| `managed_settings.json` in repo | D: "Skills distribution via plugins and managed_settings.json" → `[✓\|artifact]` |

---

## Gap questions

| Branch | Gap | Ask this |
|--------|-----|----------|
| [ROOT] | No subagent evidence | "Have you used a task where Claude spawned multiple subagents in parallel? Walk me through what the task was and how you could tell subagents were involved." |
| [ROOT] | No worktree evidence | "Have you ever run two Claude sessions simultaneously on separate git branches? If so, what were you doing in each?" |
| [A] | No skill evidence | "Have you written any custom slash commands? Walk me through one — what does it do, what syntax does it use, and what does invoking it feel like vs. typing the same prompt?" |
| [A] | No plugin evidence | "Have you installed any plugins? How did you discover them and what did the plugin add to your workflow?" |
| [B] | No hook evidence | "Have you configured any hooks — automation that fires before or after Claude uses a tool? Walk me through what the hook does and when it fires." |
| [B] | No handler evidence | "Have you written the actual hook handler script — the Python or shell code that reads stdin JSON and responds? Walk me through how your handler works." |
| [C] | No headless evidence | "Have you run `claude -p` or `claude --print` outside of an interactive session? What was the use case?" |
| [C] | No MCP evidence | "Do you have any MCP servers configured? What do they expose to Claude and how do you invoke them?" |

### Qualitative rubric

- **`[✓]` Demonstrated**: Contains a specific behavior, flag, scenario, or tradeoff only someone who has done it would know.
- **`[~]` Self-reported**: Affirmative but vague. No distinguishing detail.
- **`[ ]` Not yet**: Negative, uncertain, or no exposure.

### Answer → node mapping

| Answer contains | Node → status |
|-----------------|---------------|
| Specific description of parallel subagents with task detail | ROOT: "Subagent basics" → `[✓\|reported]`; ROOT: "Agent teams" → `[~\|reported]` |
| Specific description of foreground vs. background behavior | ROOT: "Foreground vs. background" → `[✓\|reported]` |
| Description of worktree usage with two branches | ROOT: "Worktrees" → `[✓\|reported]` (if specific) or `[~\|reported]` (if vague) |
| Description of a slash command with syntax detail | A: "Skills: creation and syntax" → `[✓\|reported]` |
| Description of !bash, @file, or $ARGUMENTS in a skill | A: "Skill mechanics" → `[✓\|reported]` |
| Description of plugin install or usage | A: "Plugin discovery" → `[✓\|reported]` |
| Description of hook firing with specific tool or pattern | B: "PostToolUse hooks" or "PreToolUse hooks" → `[✓\|reported]` |
| Description of hook handler with stdin JSON parsing | B: "Hook handler scripts" → `[✓\|reported]` |
| Description of `claude -p` use case | C: "Headless mode" → `[✓\|reported]` |
| Description of MCP server and its tools | C: "MCP: configure and use servers" → `[✓\|reported]` |
| Description of .mcp.json at project root | C: "MCP project config" → `[✓\|reported]` |

---

## Unlock thresholds

- Branch A unlocks when ROOT ≥ 2 `[✓]`
- Branch B unlocks when Branch A ≥ 3 `[✓]`
- Branch C unlocks when Branch B ≥ 3 `[✓]`
- Branch D unlocks when Branch C ≥ 2 `[✓]`
- Branch E unlocks when Branch D ≥ 1 `[✓]`

Both `[✓]` and `[~]` count toward unlock thresholds.

---

## Tier definitions

| Tier | Criterion |
|------|-----------|
| Explorer | ROOT incomplete or early ROOT only |
| Builder | Branch A in progress, hooks not yet started |
| Practitioner | Branch B active, headless/MCP being explored |
| Expert | Branch C complete |

---

## Tree render template

```
[ROOT] Agents and Orchestration
    [?] Subagent basics: spawning and tool access
    [?] Foreground vs. background subagents
    [?] Agent teams: orchestration patterns
    [?] Custom subagent definitions (.claude/agents/)
    [?] Worktrees for parallel development

[A] Skills and Plugins   [if locked: "(unlock: complete 2 Agents & Orchestration skills)"]
    [?] Skills (slash commands): creation and syntax
    [?] Skill mechanics: $ARGUMENTS, !bash, @file
    [?] Skill and command composition
    [?] Output styles: controlling response format
    [?] Plugin discovery and installation
    [?] Plugin manifest (plugin.json)
    [?] context: fork for skill isolation
    [?] argument-hint frontmatter for required parameter prompting
    [?] .claude/rules/ with YAML paths: glob patterns for conditional rule loading

[B] Hooks System   [if locked: "(unlock: complete 3 Skills & Plugins)"]
    [?] PreToolUse hooks (validation, blocking)
    [?] PostToolUse hooks (linting, reactions)
    [?] Stop and Notification hooks (session alerts)
    [?] Hook handler scripts (stdin, exit codes, response)
    [?] Scoped hooks (in skill or agent frontmatter)
    [?] Hooks guide: design patterns and gotchas

[C] Headless and MCP   [if locked: "(unlock: complete 3 Hooks System skills)"]
    [?] Headless mode (-p flag, non-interactive)
    [?] Piped input and CI integration
    [?] --output-format json and --json-schema for structured headless output
    [?] Built-in tool selection for codebase tasks
    [?] MCP: configure and use servers
    [?] MCP project config (.mcp.json)
    [?] Troubleshooting: diagnose and recover

[D] Skills Distribution and Enterprise   [if locked: "(unlock: complete 2 Headless & MCP skills)"]
    [?] Skills distribution via plugins and managed_settings.json
    [?] Skills as custom subagent delegation targets

[E] Iterative Refinement Workflows   [if locked: "(unlock: complete 1 Distribution skill)"]
    [?] Iterative refinement: sequential subagent pattern for test-driven iteration
    [?] Interview pattern: structured questions for ambiguous analysis tasks
```

---

## Saved tree file template

```markdown
---
version: 3
topic: build
user: [git config user.name or "unknown"]
email: [git config user.email or "unknown"]
updated: [today's date YYYY-MM-DD]
level: [Explorer / Builder / Practitioner / Expert]
xp: [CURRENT_XP]
---

# Build Knowledge Graph

*[✓] Demonstrated · [~] Self-reported · [ ] Not yet · [★] Mastery target · [·] Locked*

## [ROOT] Agents and Orchestration
- [STATUS|TYPE] Subagent basics: spawning and tool access
- [STATUS|TYPE] Foreground vs. background subagents
- [STATUS|TYPE] Agent teams: orchestration patterns
- [STATUS|TYPE] Custom subagent definitions (.claude/agents/)
- [STATUS|TYPE] Worktrees for parallel development

## [A] Skills and Plugins
- [STATUS|TYPE] Skills (slash commands): creation and syntax
- [STATUS|TYPE] Skill mechanics: $ARGUMENTS, !bash, @file
- [STATUS|TYPE] Skill and command composition
- [STATUS|TYPE] Output styles: controlling response format
- [STATUS|TYPE] Plugin discovery and installation
- [STATUS|TYPE] Plugin manifest (plugin.json)
- [STATUS|TYPE] context: fork for skill isolation
- [STATUS|TYPE] argument-hint frontmatter for required parameter prompting
- [STATUS|TYPE] .claude/rules/ with YAML paths: glob patterns for conditional rule loading

## [B] Hooks System
- [STATUS|TYPE] PreToolUse hooks (validation, blocking)
- [STATUS|TYPE] PostToolUse hooks (linting, reactions)
- [STATUS|TYPE] Stop and Notification hooks (session alerts)
- [STATUS|TYPE] Hook handler scripts (stdin, exit codes, response)
- [STATUS|TYPE] Scoped hooks (in skill or agent frontmatter)
- [STATUS|TYPE] Hooks guide: design patterns and gotchas

## [C] Headless and MCP
- [STATUS|TYPE] Headless mode (-p flag, non-interactive)
- [STATUS|TYPE] Piped input and CI integration
- [STATUS|TYPE] --output-format json and --json-schema for structured headless output
- [STATUS|TYPE] Built-in tool selection for codebase tasks
- [STATUS|TYPE] MCP: configure and use servers
- [STATUS|TYPE] MCP project config (.mcp.json)
- [STATUS|TYPE] Troubleshooting: diagnose and recover

## [D] Skills Distribution and Enterprise
- [STATUS|TYPE] Skills distribution via plugins and managed_settings.json
- [STATUS|TYPE] Skills as custom subagent delegation targets

## [E] Iterative Refinement Workflows
- [STATUS|TYPE] Iterative refinement: sequential subagent pattern for test-driven iteration
- [STATUS|TYPE] Interview pattern: structured questions for ambiguous analysis tasks

## Frontier
- [frontier node name] — [criterion one-liner]

## Notes
<!-- Add personal notes here -->
```
