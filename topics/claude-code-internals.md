---
topic: claude-code-internals
node_count: 5
version: 1
source_url: *(empirically verified — no official doc)*
description: Empirically-verified Claude Code internal behaviors not covered by official documentation. Each node was discovered through observation and is sourced by session/date rather than doc URL. Supplemental to the main claude-code topic.
---

# Claude Code Internals Knowledge Graph Schema

This schema captures **Claude Code behaviors that are undocumented but consequential** — the kind of gotcha that causes silent failures, confusing results, or unexpected scoping. Because these have no official doc, each node is sourced with the session/date it was discovered and marked as empirically verified.

**Supplemental to:** `claude-code` and `build` topics. Nodes here overlap thematically with `build.md` (Skills and Plugins, Hooks System branches) but go deeper on the internal mechanics.

---

## Node definitions

5 nodes across 2 branches.

### [ROOT] Execution Environment (always unlocked — 3 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|-----------|
| !bash vs Bash tool env var inheritance | Can explain: `!bash-command` in a skill/command runs in a fresh subshell that does NOT inherit `settings.json["env"]` vars; the Bash tool runs as a subprocess of Claude Code's process and DOES inherit them; knows that silent failure (empty var, no error) is the primary symptom | Qualitative | None | *(empirically verified — 2026-03-14)* |
| Hook stdin contract (JSON shape and exit code semantics) | Can describe the exact stdin shape a hook handler receives: `{ "hook_event_name": "...", "tool_name": "...", "tool_input": {...}, "tool_response": {...} }`; knows exit code semantics: 0 = success (stdout goes to the debug log, NOT Claude's context — except for `UserPromptSubmit`/`SessionStart`, where exit-0 stdout is added to context); 2 = block, with **stderr** fed back to Claude as the message; any other non-zero = non-blocking error with stderr surfaced to the user | Qualitative / Artifact | hook handler script with stdin JSON parsing in repo → `[~\|artifact]` | *(empirically verified — 2026-03-09)* |
| settings.json["env"] injection scope | Can explain exactly which execution contexts receive vars from `settings.json["env"]`: only the Bash tool subprocess — NOT `!bash` skill commands, NOT hook shell commands, NOT MCP server startup env; knows to use shell-level env export or wrapper scripts for hooks that need env vars | Qualitative | None | *(empirically verified — 2026-03-14)* |

### [A] Plugin and Hook Registration (unlocks when ROOT ≥ 2 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|-----------|
| --plugin-dir hook registration limitation | Can explain: when a plugin is loaded via `--plugin-dir` (local dev), the plugin's `hooks.json` is NOT registered — only `hooks.json` from the installed plugin cache path fires; the workaround is to install the plugin properly or register hooks separately in `~/.claude/settings.json` | Qualitative | None | *(empirically verified — 2026-03-15)* |
| SessionStart hook idempotency pattern | Can describe the pattern for a self-healing SessionStart hook: check the target state directly (e.g., read `~/.claude.json` and inspect `mcpServers` key) rather than running a registration command blindly; only register if not already present; use `claude mcp add -s user` for MCP registration; this avoids duplicates and is safe to run on every session | Qualitative / Artifact | `setup-mcp.py` or similar idempotency script in hooks → `[✓\|artifact]` | *(empirically verified — 2026-03-15)* |

---

## Detection signals

| Collected evidence | Node → status |
|--------------------|---------------|
| Hook handler script with stdin JSON parsing | ROOT: "Hook stdin contract" → `[~\|artifact]` |
| `setup-mcp.py` or idempotency script in SessionStart hooks | A: "SessionStart hook idempotency pattern" → `[✓\|artifact]` |

---

## Gap questions

| Branch | Gap | Ask this |
|--------|-----|----------|
| [ROOT] | No env signal | "You need an env var available inside a PostToolUse hook handler and also inside a `!bash` command in a skill. You've set it in `settings.json['env']`. Where does it actually show up, and where doesn't it?" |
| [ROOT] | Hook stdin | "Walk me through the exact shape of JSON your hook handler reads from stdin, and what exit code you'd use to block a tool call vs. let it through." |
| [A] | Plugin dev | "You're developing a plugin locally with `--plugin-dir`. Your plugin's `hooks.json` defines a PostToolUse hook. Does the hook fire? Why or why not?" |

### Qualitative rubric

- **`[✓]` Demonstrated**: Names the specific gotcha — fresh subshell, silent failure, exact JSON field names, or the `--plugin-dir` limitation by name.
- **`[~]` Self-reported**: Affirmative but vague ("I think it has to do with the shell environment").
- **`[ ]` Not yet**: No exposure or negative.

### Answer → node mapping

| Answer contains | Node → status |
|-----------------|---------------|
| "fresh subshell" + "does not inherit" + env var failure scenario | ROOT: "!bash vs Bash tool env var inheritance" → `[✓\|reported]` |
| Affirmative on env difference but without fresh-subshell detail | ROOT: "!bash vs Bash tool env var inheritance" → `[~\|reported]` |
| Exact stdin JSON field names (hook_event_name, tool_name, tool_input) | ROOT: "Hook stdin contract" → `[✓\|reported]` |
| Correct exit codes (0/2 semantics) without field names | ROOT: "Hook stdin contract" → `[~\|reported]` |
| Explains scope: Bash tool yes, !bash no, hooks no | ROOT: "settings.json" → `[✓\|reported]` |
| "--plugin-dir" + hooks.json not registered | A: "--plugin-dir hook registration limitation" → `[✓\|reported]` |

---

## Unlock thresholds

- Branch A unlocks when ROOT ≥ 2 `[✓]`

Both `[✓]` and `[~]` count toward unlock thresholds.

---

## Tier definitions

| Tier | Criterion |
|------|-----------|
| Explorer | ROOT incomplete |
| Builder | ROOT complete, A in progress |
| Practitioner | All nodes demonstrated |

---

## Tree render template

```
Execution Environment
    [?] !bash vs Bash tool env var inheritance
    [?] Hook stdin contract (JSON shape and exit code semantics)
    [?] settings.json["env"] injection scope

Plugin and Hook Registration   [if locked: "(unlock: complete 2 Execution Environment skills)"]
    [?] --plugin-dir hook registration limitation
    [?] SessionStart hook idempotency pattern
```

---

## Saved tree file template

```markdown
---
version: 3
topic: claude-code-internals
user: [git config user.name or "unknown"]
email: [git config user.email or "unknown"]
updated: [today's date YYYY-MM-DD]
level: [Explorer / Builder / Practitioner]
xp: [CURRENT_XP]
---

# Claude Code Internals Knowledge Graph

*[✓] Demonstrated · [~] Self-reported · [ ] Not yet · [★] Mastery target · [·] Locked*

*Supplemental to claude-code and build topics. Nodes sourced empirically — no official docs.*

## [ROOT] Execution Environment
- [STATUS|TYPE] !bash vs Bash tool env var inheritance
- [STATUS|TYPE] Hook stdin contract (JSON shape and exit code semantics)
- [STATUS|TYPE] settings.json["env"] injection scope

## [A] Plugin and Hook Registration
- [STATUS|TYPE] --plugin-dir hook registration limitation
- [STATUS|TYPE] SessionStart hook idempotency pattern

## Frontier
- [frontier node name] — [criterion one-liner]

## Notes
<!-- Discoveries sourced empirically — add session/date for new nodes -->
```
