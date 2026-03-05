---
topic: claude-code
version: 1
source_url: https://docs.anthropic.com/en/docs/claude-code/
description: Anthropic's CLI-based AI coding tool for professional developers — navigate codebases, write code, run tests, commit, manage sessions, and automate workflows.
---

# Claude Code Knowledge Tree Schema

This file defines the curriculum for the `claude-code` topic. It is loaded by `/sup` at invocation time. To create a new topic, copy this file, change the frontmatter, and replace the sections below.

---

## Node definitions

36 nodes across 6 branches. Every node grounded in Claude Code's actual feature surface.

### [ROOT] Configure Claude (always unlocked — 5 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|-----------|
| CLAUDE.md with project guidance | Project CLAUDE.md exists with >5 lines of substantive content (build commands, conventions, architecture, workflows) | Artifact | CLAUDE.md line count > 5 | https://docs.anthropic.com/en/docs/claude-code/memory |
| settings.json / settings.local.json exists | At least one settings file exists at project or global level with non-default content | Artifact | settings file exists with keys | https://docs.anthropic.com/en/docs/claude-code/settings |
| Model or budget settings configured | Has explicitly configured a model preference, effort level, or token budget; can explain the tradeoff | Qualitative | `defaultModel`, `maxTokens`, or `budget` key in settings | https://docs.anthropic.com/en/docs/claude-code/settings |
| /memory audit and CLAUDE.md hierarchy | Has run `/memory`; understands global (`~/.claude/CLAUDE.md`) vs. project vs. local scope; reviewed auto-memory | Exercise | auto-memory files > 0 (weak signal → `[~]`) | https://docs.anthropic.com/en/docs/claude-code/memory |
| CLI fundamentals (/help, /doctor, /usage) | Has run `/help` to see all commands; `/doctor` to verify environment; `/usage` to check token spend and session/weekly limits; can interpret `/doctor` output | Exercise / Qualitative | None (ask via gap question) | https://docs.anthropic.com/en/docs/claude-code/cli-reference |

### [A] Memory and Context Management (unlocks when ROOT ≥ 2 `[✓]` — 6 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|-----------|
| Context window and /compact usage | Has used `/compact` or `/clear` deliberately; can explain: compact summarizes history, clear wipes it | Exercise / Qualitative | None (ask via gap question) | https://docs.anthropic.com/en/docs/claude-code/cli-reference |
| Session naming and resumption | Has named a session with `/rename` and resumed it with `--continue` or `--resume`; knows the session picker | Historical / Exercise | total Claude sessions > 5 (weak → `[~]`) | https://docs.anthropic.com/en/docs/claude-code/cli-reference |
| Rewind / checkpointing (Esc+Esc) | Has used `Esc+Esc` or `/rewind` to restore state; can compare to `git checkout` | Exercise / Qualitative | None (ask via gap question) | https://docs.anthropic.com/en/docs/claude-code/interactive-mode |
| @file references, images, piped input | Has used `@filename` syntax to inject a file; knows image paste and `cat file \| claude -p` | Exercise | None (ask via gap question) | https://docs.anthropic.com/en/docs/claude-code/cli-reference |
| Plan mode (Shift+Tab) | Has activated plan mode; used it before a non-trivial change; can describe what plan mode prevents Claude from doing | Exercise / Qualitative | `defaultMode: plan` in settings → `[✓]` | https://docs.anthropic.com/en/docs/claude-code/interactive-mode |
| Permissions system (/permissions, globs) | Has run `/permissions`; written a glob allow rule (e.g., `Bash(npm run *)`); understands precedence hierarchy | Exercise / Qualitative | global permission rules > 0 → `[✓]` | https://docs.anthropic.com/en/docs/claude-code/settings |

### [B] Codebase Navigation (unlocks when Branch A ≥ 3 `[✓]` — 5 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|-----------|
| Read + Glob + Grep exploration | Has used all three tools in one session; can describe when to use each vs. the others | Exercise | None — infer from codebase size (repo has source files → exercise is possible) | https://docs.anthropic.com/en/docs/claude-code/tools |
| Explain an unfamiliar module | Asked Claude to explain a module; Claude read files first, explained with real function names and data flows | Exercise | None | https://docs.anthropic.com/en/docs/claude-code/tools |
| Trace a call path across files | Traced an entry point to leaves across multiple files; response named real files and function hops at each step | Exercise | None | https://docs.anthropic.com/en/docs/claude-code/tools |
| Repo-wide pattern audit | Found a quality concern across the entire codebase; received structured report with file locations | Exercise | repo has >5 source files (exercise is meaningful) | https://docs.anthropic.com/en/docs/claude-code/tools |
| Verification patterns after changes | After a code change, Claude ran tests or linter and interpreted the output | Exercise / Historical | test framework detected → `[~]` (can do it); max files in recent commit > 0 → weak signal | https://docs.anthropic.com/en/docs/claude-code/tools |

### [C] Code Change Workflows (unlocks when Branch B ≥ 3 `[✓]` — 7 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|-----------|
| Single-file edits with context | Claude read the file before editing, matched existing style; edit integrated (not just appended) | Historical / Exercise | git history exists → reasonable to assume | https://docs.anthropic.com/en/docs/claude-code/common-tasks |
| Multi-file coordinated changes | Made a change requiring ≥3 files edited consistently; Claude maintained consistency across all | Historical / Exercise | max files in recent commit ≥ 3 → `[~]` | https://docs.anthropic.com/en/docs/claude-code/common-tasks |
| Commit / PR description generation | Let Claude write a commit message from actual diffs; reviewed it, pushed back on one aspect, iterated | Historical / Exercise | structured git commit messages (>2 lines) → `[~]` | https://docs.anthropic.com/en/docs/claude-code/common-tasks |
| Test-first workflow | Wrote a test before implementation; or added tests for existing code and ran them | Exercise / Historical | test framework detected + test files in repo → exercise is possible | https://docs.anthropic.com/en/docs/claude-code/common-tasks |
| Refactor with safety net | Claude refactored code; ran tests before and after; all tests stayed green | Exercise | test framework detected → exercise is possible | https://docs.anthropic.com/en/docs/claude-code/common-tasks |
| Long-running agentic tasks | Gave Claude a multi-step task (>3 tool calls); let it run with minimal interruption | Historical / Exercise | subagent sessions > 0 → `[~]`; total sessions > 10 → `[~]` | https://docs.anthropic.com/en/docs/claude-code/how-claude-code-uses-computers |
| Bash mode (!command) and -p | Used `!bash-command` syntax in a session; knows `claude -p "prompt"` for non-interactive pipelines | Exercise | headless invocations in repo → `[✓]` | https://docs.anthropic.com/en/docs/claude-code/cli-reference |

### [D] Agents and Orchestration (unlocks when Branch C ≥ 4 `[✓]` — 6 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|-----------|
| Parallel subagents | Given Claude a task where it spawned multiple subagents; can describe foreground vs. background subagents | Historical / Exercise | subagent sessions > 3 → `[✓]`; > 0 → `[~]` | https://docs.anthropic.com/en/docs/claude-code/sub-agents |
| Worktrees for parallel development | Ran two Claude sessions simultaneously on separate branches using `--worktree`; knows when it's useful vs. overhead | Historical / Exercise | git worktrees > 1 → `[✓]`; project worktree dirs > 0 → `[✓]` | https://docs.anthropic.com/en/docs/claude-code/how-claude-code-uses-computers |
| Custom subagent definitions (.claude/agents/) | Created at least one custom subagent in `.claude/agents/` or `~/.claude/agents/`; has invoked it | Artifact | custom agent definitions > 0 → `[✓]` | https://docs.anthropic.com/en/docs/claude-code/sub-agents |
| Custom slash commands (.claude/commands/) | Created a custom slash command; knows `$ARGUMENTS`, `!bash`, and `@file` syntax work in command files | Artifact | `.claude/commands/` count ≥ 2 → `[✓]` | https://docs.anthropic.com/en/docs/claude-code/slash-commands |
| MCP servers configured and used | Has ≥1 MCP server configured; has actually made a query using an MCP tool (not just configured it) | Artifact + Exercise | MCP servers listed in settings → `[~]` (configured but not verified as used) | https://docs.anthropic.com/en/docs/claude-code/mcp |
| Agent teams and headless mode | Ran `cat file \| claude -p "..."` or `claude -p` in a script; knows CI pipeline integration pattern | Exercise | headless invocations in repo → `[✓]` | https://docs.anthropic.com/en/docs/claude-code/cli-reference |

### [E] Automation and Extension (unlocks when Branch D ≥ 4 `[✓]` — 7 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|-----------|
| PreToolUse hooks (validation, blocking) | Has a PreToolUse hook that fires; knows exit code protocol (0=allow, 2=block with message) | Artifact | `hooks.PreToolUse` in settings → `[✓]` | https://docs.anthropic.com/en/docs/claude-code/hooks |
| PostToolUse hooks (linting, reactions) | Has a PostToolUse hook that fires after edits; knows its output is injected back into Claude's context | Artifact | `hooks.PostToolUse` in settings → `[✓]` | https://docs.anthropic.com/en/docs/claude-code/hooks |
| Notification hooks (Stop, idle alerts) | Has a Stop or Notification hook that alerts on session end or idle; can explain when each fires | Artifact | `hooks.Stop` or `hooks.Notification` in settings → `[✓]` | https://docs.anthropic.com/en/docs/claude-code/hooks |
| Hooks scoped to skills/subagents | Has defined a `hooks:` block in a skill or agent frontmatter (not just in global settings) | Artifact | `hooks:` key in any `.claude/commands/*.md` or `.claude/agents/*.md` → `[✓]` | https://docs.anthropic.com/en/docs/claude-code/hooks |
| !bash context injection in skill files | Has written a skill that uses `!` syntax to inject live data at invocation (git log, test results, API output) | Artifact | skill files with bash injection > 0 → `[✓]` | https://docs.anthropic.com/en/docs/claude-code/slash-commands |
| Custom MCP server (build or extend) | Has built or extended an MCP server that exposes ≥1 tool Claude can call; knows stdio vs. HTTP transport | Artifact / Historical | repo contains MCP server implementation patterns → `[~]` | https://modelcontextprotocol.io/quickstart |
| Claude Code SDK (custom agent apps) | Has used the Claude Agent SDK or Anthropic API to build a custom agent or pipeline; understands how tool use works programmatically | Artifact / Historical | repo contains `from anthropic` + agent-like imports OR `@anthropic-ai` in package.json → `[~]` | https://docs.anthropic.com/en/docs/claude-code/sdk |

---

## Detection signals

Apply these at inference Step 1 (environmental signals — highest priority):

| Collected evidence | Node → status |
|--------------------|---------------|
| CLAUDE.md line count > 5 | ROOT: "CLAUDE.md with project guidance" → `[✓\|artifact]` |
| settings.json exists with non-empty content | ROOT: "settings.json exists" → `[✓\|artifact]` |
| `defaultModel`, `maxTokens`, or `budget` key in settings | ROOT: "Model or budget settings configured" → `[✓\|artifact]` |
| auto-memory files > 0 | ROOT: "/memory audit" → `[~\|historical]` |
| hooks detected (any hook type) | E: "PreToolUse/PostToolUse/Notification hooks" → `[✓\|artifact]` (for applicable types) |
| MCP servers listed in settings | D: "MCP servers configured and used" → `[~\|artifact]` (configured; not verified as queried) |
| `.claude/commands/` count ≥ 2 | D: "Custom slash commands" → `[✓\|artifact]` |
| `defaultMode: plan` in settings | A: "Plan mode" → `[✓\|artifact]` |
| global permission rules > 0 | A: "Permissions system" → `[✓\|artifact]` |
| git worktrees > 1 OR project worktree dirs > 0 | D: "Worktrees" → `[✓\|historical]` |
| subagent sessions > 3 | D: "Parallel subagents" → `[✓\|historical]` |
| subagent sessions > 0 (≤3) | D: "Parallel subagents" → `[~\|historical]` |
| custom agent definitions > 0 | D: "Custom subagent defs" → `[✓\|artifact]` |
| headless invocations in repo > 0 | C: "Bash mode / -p" → `[✓\|artifact]`; D: "Agent teams" → `[✓\|artifact]` |
| skill files with bash injection > 0 | E: "!bash injection in skill files" → `[✓\|artifact]` |
| max files in recent commit ≥ 3 | C: "Multi-file changes" → `[~\|historical]` |
| scripts/ directory has files | C: "Long-running agentic tasks" → `[~\|historical]` |
| `from anthropic` import + agent patterns OR `@anthropic-ai` in package.json | E: "Claude Code SDK" → `[~\|artifact]` |

---

## Gap questions

Select based on what env signals did NOT detect. Rank by branch priority — ROOT and [A] gaps first.

| Branch | Gap | Ask this |
|--------|-----|----------|
| [ROOT] | No CLI fundamentals evidence | "Have you run `/help` or `/doctor` inside Claude Code? If so, what did `/doctor` show — any missing tools or environment issues?" |
| [A] | No context management evidence | "Have you used `/compact` or `/clear` deliberately — not by accident? If so, what triggered it and what happened?" |
| [A] | No session resumption evidence | "Have you ever resumed a named Claude session from a previous day? If so, how did you find it — session picker, `--resume`?" |
| [A] | No rewind evidence | "Have you ever used `Esc+Esc` or `/rewind` to undo what Claude just did? If so, what did you revert?" |
| [A] | No @file evidence | "Have you typed `@filename` in the chat box to inject a file directly into context? If so, what were you referencing?" |
| [A] | No plan mode evidence (not artifact-detected) | "Have you used plan mode — where Claude reads and reasons but doesn't modify files? If so, what kind of task was it for?" |
| [A] | No permissions evidence | "Have you configured what Bash commands Claude can run without asking for approval? If so, how?" |
| [C] | No commit/PR generation evidence | "Have you let Claude write a commit message or PR description from your actual diff? If so, did it capture the right context?" |
| [C] | No test-first evidence | "Have you asked Claude to write tests before implementation, or to add tests to existing code? What happened?" |
| [D] | No worktree evidence | "Have you ever run two Claude sessions simultaneously on separate branches? If so, what were you working on in each?" |
| [E] | No hooks detected | "Have you set up any automation that fires before or after Claude uses a tool — like a linter after edits or a notification when Claude finishes?" |
| [D] | No custom commands detected | "Have you built any slash commands you reuse? If so, what does one of them do?" |

### Qualitative rubric for answers

- **`[✓]` Demonstrated**: The answer contains at least one specific, verifiable detail only someone who has done it would know — a specific flag, an observed behavior, a tradeoff they navigated, or a concrete description of what happened.
- **`[~]` Self-reported**: Affirmative but vague. "Yes I've used /compact" without any specifics.
- **`[ ]` Not yet**: Negative, "not sure," or "heard of it but haven't tried."

### Answer → node mapping

| Answer contains | Node → status |
|-----------------|---------------|
| Specific detail about `/doctor` output or `/help` commands seen | ROOT: "CLI fundamentals" → `[✓\|reported]` |
| Vague "yes" to /help or /doctor | ROOT: "CLI fundamentals" → `[~\|reported]` |
| Specific detail about `/compact` or `/clear` behavior | A: "Context window and /compact usage" → `[✓\|reported]` |
| Vague "yes" to compact/clear | A: "Context window and /compact usage" → `[~\|reported]` |
| Specific detail about `--resume` or session picker | A: "Session naming and resumption" → `[✓\|reported]` |
| Specific detail about `Esc+Esc` or `/rewind` behavior | A: "Rewind / checkpointing" → `[✓\|reported]` |
| Specific description of @file or piped input usage | A: "@file references" → `[✓\|reported]` |
| Specific description of plan mode behavior | A: "Plan mode" → `[✓\|reported]` |
| Specific description of allow/deny rule or permissions UI | A: "Permissions system" → `[✓\|reported]` |
| "basic edits" or similar | C: "Single-file edits" → `[✓\|reported]`, B: "Read/Glob/Grep" → `[~\|reported]` |
| "multi-file changes" | C: "Multi-file changes" → `[✓\|reported]` |
| "agents" or "subagents" | D: "Parallel subagents" → `[~\|reported]`, C: "Long-running tasks" → `[✓\|reported]` |
| "hooks" (no env evidence) | E: hooks (all types) → `[~\|reported]` |
| "MCP" or "mcp servers" (no env evidence) | D: "MCP servers" → `[~\|reported]` |
| "custom slash commands" or "custom commands" (no env evidence) | D: "Custom slash commands" → `[~\|reported]` |
| "CLAUDE.md" (no env evidence) | ROOT: "CLAUDE.md" → `[~\|reported]` |
| "worktrees" or "parallel sessions" | D: "Worktrees" → `[✓\|reported]` (if specific) or `[~\|reported]` (if vague) |
| "commit message" or "PR description" | C: "Commit / PR generation" → `[✓\|reported]` |
| "test writing" or "test-first" | C: "Test-first workflow" → `[✓\|reported]` |

---

## Unlock thresholds

- Branch A unlocks when ROOT ≥ 2 `[✓]`
- Branch B unlocks when Branch A ≥ 3 `[✓]`
- Branch C unlocks when Branch B ≥ 3 `[✓]`
- Branch D unlocks when Branch C ≥ 4 `[✓]`
- Branch E unlocks when Branch D ≥ 4 `[✓]`

Both `[✓]` and `[~]` count toward unlock thresholds.

---

## Tier definitions

| Tier | Criterion |
|------|-----------|
| Explorer | ROOT incomplete OR ROOT + early Branch A only |
| Builder | Branch A mostly done, Branch B or C in progress |
| Practitioner | Branch C mostly done, Branch D active |
| Expert | Branch D complete or Branch E in progress |

---

## Tree render template

Use this exact layout when rendering the tree in Phase 3:

```
[ROOT] Configure Claude
    [?] CLAUDE.md with project guidance
    [?] settings.json / settings.local.json exists
    [?] Model or budget settings configured
    [?] /memory audit and CLAUDE.md hierarchy
    [?] CLI fundamentals (/help, /doctor, /usage)

[A] Memory and Context Management
    [?] Context window and /compact usage
    [?] Session naming and resumption
    [?] Rewind / checkpointing (Esc+Esc)
    [?] @file references, images, piped input
    [?] Plan mode (Shift+Tab)
    [?] Permissions system (/permissions, globs)

[B] Codebase Navigation   [if locked: "(unlock: complete 3 Memory & Context skills)"]
    [?] Read + Glob + Grep exploration
    [?] Explain an unfamiliar module
    [?] Trace a call path across files
    [?] Repo-wide pattern audit
    [?] Verification patterns after changes

[C] Code Change Workflows   [if locked: "(unlock: complete 3 Navigation skills)"]
    [?] Single-file edits with context
    [?] Multi-file coordinated changes
    [?] Commit / PR description generation
    [?] Test-first workflow
    [?] Refactor with safety net
    [?] Long-running agentic tasks
    [?] Bash mode (!command) and -p

[D] Agents and Orchestration   [if locked: "(unlock: complete 4 Code Change skills)"]
    [?] Parallel subagents
    [?] Worktrees for parallel development
    [?] Custom subagent definitions
    [?] Custom slash commands
    [?] MCP servers configured and used
    [?] Agent teams and headless mode

[E] Automation and Extension   [if locked: "(unlock: complete 4 Agents skills)"]
    [?] PreToolUse hooks
    [?] PostToolUse hooks
    [?] Notification hooks (Stop, idle)
    [?] Hooks scoped to skills/subagents
    [?] !bash context injection in skill files
    [?] Custom MCP server
    [?] Claude Code SDK (custom agent apps)
```

Replace every `[?]` with: `[✓]`, `[~]`, `[ ]`, `[★]`, or `[·]`.
If a branch is fully locked (`[·]`), collapse it to just the branch header line.

---

## Saved tree file template

When writing to `~/.claude/knowledge-trees/claude-code.md`, use this format:

```markdown
---
version: 3
topic: claude-code
user: [git config user.name or "unknown"]
email: [git config user.email or "unknown"]
updated: [today's date YYYY-MM-DD]
level: [Explorer / Builder / Practitioner / Expert]
xp: [CURRENT_XP]
---

# Claude Code Knowledge Tree

*[✓] Demonstrated · [~] Self-reported · [ ] Not yet · [★] Mastery target · [·] Locked*

## [ROOT] Configure Claude
- [STATUS|TYPE] CLAUDE.md with project guidance
- [STATUS|TYPE] settings.json / settings.local.json exists
- [STATUS|TYPE] Model or budget settings configured
- [STATUS|TYPE] /memory audit and CLAUDE.md hierarchy
- [STATUS|TYPE] CLI fundamentals (/help, /doctor, /usage)

## [A] Memory and Context Management
- [STATUS|TYPE] Context window and /compact usage
- [STATUS|TYPE] Session naming and resumption
- [STATUS|TYPE] Rewind / checkpointing (Esc+Esc)
- [STATUS|TYPE] @file references, images, piped input
- [STATUS|TYPE] Plan mode (Shift+Tab)
- [STATUS|TYPE] Permissions system (/permissions, globs)

## [B] Codebase Navigation
- [STATUS|TYPE] Read + Glob + Grep exploration
- [STATUS|TYPE] Explain an unfamiliar module
- [STATUS|TYPE] Trace a call path across files
- [STATUS|TYPE] Repo-wide pattern audit
- [STATUS|TYPE] Verification patterns after changes

## [C] Code Change Workflows
- [STATUS|TYPE] Single-file edits with context
- [STATUS|TYPE] Multi-file coordinated changes
- [STATUS|TYPE] Commit / PR description generation
- [STATUS|TYPE] Test-first workflow
- [STATUS|TYPE] Refactor with safety net
- [STATUS|TYPE] Long-running agentic tasks
- [STATUS|TYPE] Bash mode (!command) and -p

## [D] Agents and Orchestration
- [STATUS|TYPE] Parallel subagents
- [STATUS|TYPE] Worktrees for parallel development
- [STATUS|TYPE] Custom subagent definitions
- [STATUS|TYPE] Custom slash commands
- [STATUS|TYPE] MCP servers configured and used
- [STATUS|TYPE] Agent teams and headless mode

## [E] Automation and Extension
- [STATUS|TYPE] PreToolUse hooks
- [STATUS|TYPE] PostToolUse hooks
- [STATUS|TYPE] Notification hooks (Stop, idle)
- [STATUS|TYPE] Hooks scoped to skills/subagents
- [STATUS|TYPE] !bash context injection in skill files
- [STATUS|TYPE] Custom MCP server
- [STATUS|TYPE] Claude Code SDK (custom agent apps)

## Frontier
- [frontier node name] — [criterion one-liner]

## Notes
<!-- Add personal notes here -->
```

**Demonstration evidence trail:** For `[✓]` nodes only, append `— [repo-name], [YYYY-MM-DD]: [brief note] | next: [YYYY-MM-DD] [L1]`.
The `| next: YYYY-MM-DD [LN]` field is the spaced repetition review schedule:
- Newly demonstrated nodes start at L1 (review in 1 day): `| next: [today+1d] [L1]`
- Levels: L1=1d, L2=3d, L3=7d, L4=21d, L5=60d, L6=permanent (no further review)
- Example: `- [✓|artifact] CLAUDE.md with project guidance — sup, 2026-03-04: 80+ lines | next: 2026-03-05 [L1]`

**Merge rules:** Never overwrite `[✓]` with `[ ]` or `[~]`. Preserve existing evidence trails. New nodes get their newly-inferred status. Existing `[✓]` nodes without a `| next:` field get `| next: [today+1d] [L1]` added on first version 3 write.
