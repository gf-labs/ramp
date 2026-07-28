---
topic: best-practices
node_count: 15
version: 1
source_url: https://docs.anthropic.com/en/docs/claude-code/
description: Best practices for structuring Claude Code projects — designing CLAUDE.md files, configuring tools and permissions, writing effective hooks, and session hygiene patterns.
goal: ramp them up on configuring Claude Code well — the CLAUDE.md scope hierarchy, build/architecture/onboarding docs, scoped permissions and hooks, and session hygiene that keeps a project maximally effective
---

# Best Practices Knowledge Graph Schema

This topic covers **how to set up Claude Code well** — not how to use its features, but how to configure and structure your project so Claude is maximally effective. It's meta-knowledge: the difference between someone who installs Claude Code and someone who makes it a reliable team member.

A developer who completes this tree writes CLAUDE.md files that onboard new engineers, configures permissions that prevent accidents, and maintains sessions without context rot.

---

## Node definitions

15 nodes across 3 branches.

### [ROOT] Understand the scope hierarchy (always unlocked — 3 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|----|-----|
| Global vs. project vs. local scope | Knows the three CLAUDE.md scopes; understands that `~/.claude/CLAUDE.md` applies everywhere, `./CLAUDE.md` at the repo root (or `./.claude/CLAUDE.md`) is committed and shared, and `./CLAUDE.local.md` at the repo root is gitignored and personal | Qualitative | `~/.claude/CLAUDE.md` exists (global scope in use → `[~]`) | https://docs.anthropic.com/en/docs/claude-code/memory | best-practices-global-vs-project-vs-local-scope |
| What belongs where (scoping judgment) | Has placed at least one item in each scope with a deliberate reason; can explain a concrete example of global vs. project vs. local placement | Qualitative | `./CLAUDE.local.md` exists → `[~\|artifact]` | https://docs.anthropic.com/en/docs/claude-code/memory | best-practices-what-belongs-where-scoping-judgment |
| Auto-memory system (/memory command) | Has run `/memory` to see current memory state; understands that auto-memory captures session context automatically; has reviewed and curated the auto-memory file | Exercise | auto-memory files > 0 → `[~\|historical]` | https://docs.anthropic.com/en/docs/claude-code/memory | best-practices-auto-memory-system-memory-command |

### [A] Writing effective CLAUDE.md files (unlocks when ROOT ≥ 2 `[✓]` — 5 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|----|-----|
| Build and run commands | CLAUDE.md includes verified build, test, lint, and run commands; another developer could clone the repo and run correctly without guessing | Artifact | CLAUDE.md contains code blocks with commands → `[~\|artifact]` | https://docs.anthropic.com/en/docs/claude-code/memory | best-practices-build-and-run-commands |
| Architecture and structure documentation | CLAUDE.md describes the codebase at the right level: module responsibilities, key data flows, where to look first — not a restatement of file names | Artifact / Qualitative | CLAUDE.md line count > 30 → `[~\|artifact]` | https://docs.anthropic.com/en/docs/claude-code/memory | best-practices-architecture-and-structure-documentation |
| Team conventions and contacts | CLAUDE.md names who owns which systems, where to ask questions, and what the review/deploy process is — something Claude can cite when advising on a PR | Artifact | `## Onboarding` or `## Team` section in CLAUDE.md → `[~\|artifact]` | https://docs.anthropic.com/en/docs/claude-code/memory | best-practices-team-conventions-and-contacts |
| Security-sensitive path exclusions | Has explicitly excluded at least one path from Claude's access (e.g., `.env`, `secrets/`) in CLAUDE.md or settings; understands why this matters | Artifact | CLAUDE.md or settings contains explicit deny/exclude patterns → `[✓\|artifact]` | https://docs.anthropic.com/en/docs/claude-code/settings | best-practices-security-sensitive-path-exclusions |
| Onboarding section for team tools | CLAUDE.md has a team-facing `## Onboarding` section with first-week guidance; `/ramp:up` can read it and surface it to new hires | Artifact | `## Onboarding` section in CLAUDE.md → `[✓\|artifact]` | https://docs.anthropic.com/en/docs/claude-code/memory | best-practices-onboarding-section-for-team-tools |

### [B] Configuration patterns (unlocks when Branch A ≥ 3 `[✓]` — 4 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|----|-----|
| Scoped allowed-tools rules | Has written at least one `Bash(npm run *)` style glob rule in permissions; knows the difference between allowing a tool broadly vs. narrowly; has both an allow and a deny rule | Artifact / Qualitative | global permission rules > 0 → `[~\|artifact]` | https://docs.anthropic.com/en/docs/claude-code/settings | best-practices-scoped-allowed-tools-rules |
| Hook design (exit codes and output) | Has written a PreToolUse or PostToolUse hook; knows exit 0 allows (stdout to debug log), exit 2 blocks with the message on **stderr** fed back to Claude; knows context injection uses exit-2 stderr or JSON `additionalContext`, not exit-0 stdout | Artifact | hooks in project or global settings → `[✓\|artifact]` | https://docs.anthropic.com/en/docs/claude-code/hooks | best-practices-hook-design-exit-codes-and-output |
| MCP server selection and scope | Has chosen a specific MCP server for a specific use case (not "I installed all of them"); can explain why a particular server makes Claude better for this project | Artifact + Qualitative | MCP servers configured → `[~\|artifact]` | https://docs.anthropic.com/en/docs/claude-code/mcp | best-practices-mcp-server-selection-and-scope |
| Project vs. global settings discipline | Has a deliberate split: global settings have universal rules, project settings are repo-specific; nothing is in global that should be local | Qualitative | both project and global settings files exist → `[~\|artifact]` | https://docs.anthropic.com/en/docs/claude-code/settings | best-practices-project-vs-global-settings-discipline |

### [C] Session hygiene (unlocks when Branch B ≥ 2 `[✓]` — 3 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|----|-----|
| Compact timing and triggers | Has used `/compact` before hitting context limits, not after; knows that compacting early preserves quality; has a personal heuristic for when to compact | Exercise / Qualitative | total Claude sessions > 5 → `[~\|historical]` | https://docs.anthropic.com/en/docs/claude-code/cli-reference | best-practices-compact-timing-and-triggers |
| Session naming and project hygiene | Names sessions with `/rename` at the start of meaningful work, not after the fact; can retrieve a session from a week ago by name; deletes dead sessions regularly | Historical / Exercise | total Claude sessions > 10 → `[~\|historical]` | https://docs.anthropic.com/en/docs/claude-code/cli-reference | best-practices-session-naming-and-project-hygiene |
| Rewind vs. restart judgment | Has a clear personal rule for when to use `Esc+Esc` (undo last action) vs. `/clear` (start over) vs. starting a new session; can describe a case where the wrong choice caused problems | Qualitative | None (ask via gap question) | https://docs.anthropic.com/en/docs/claude-code/interactive-mode | best-practices-rewind-vs-restart-judgment |

---

## Probes

| name | primitive | args |
|------|-----------|------|
| claude_md_global     | file-exists  | ~/.claude/CLAUDE.md |
| claude_local         | file-exists  | CLAUDE.local.md |
| claude_md_lines      | file-lines   | CLAUDE.md |
| claude_md_codeblocks | grep-count   | "^```" CLAUDE.md |
| claude_md_onboarding | grep-count   | "^## Onboarding\|^## Team" CLAUDE.md |
| memory_files         | glob-count   | ~/.claude/projects/**/MEMORY.md |
| deny_rules           | json-has-key | ~/.claude/settings.json permissions.deny |
| global_permissions   | json-has-key | ~/.claude/settings.json permissions.allow |
| hooks_global         | json-has-key | ~/.claude/settings.json hooks |
| hooks_project        | json-has-key | .claude/settings.json hooks |
| mcp_user             | json-has-key | ~/.claude.json mcpServers |
| mcp_project          | json-has-key | .mcp.json mcpServers |
| settings_project     | file-exists  | .claude/settings.json |
| settings_global      | file-exists  | ~/.claude/settings.json |
| sessions             | glob-count   | ~/.claude/projects/**/*.jsonl --exclude ~/.claude/projects/**/agent-*.jsonl |

**Notes.** The `[✓|artifact]` seeds (a global `permissions.deny` key, a hook in
personal settings) come from **personal** config the developer authored — a direct
witness of the act. Project-scoped artifacts (a CLAUDE.md, a project hook) may be
inherited from a cloned repo, so they seed `[~|artifact]` and rely on teach-back.
`claude_md_codeblocks` counts fenced blocks as a proxy for build/run commands.

---

## Detection signals

| Collected evidence | Node → status |
|--------------------|---------------|
| claude_md_global is true | ROOT: "Global vs. project vs. local scope" → `[~\|artifact]` |
| claude_local is true | ROOT: "What belongs where" → `[~\|artifact]` |
| memory_files > 0 | ROOT: "Auto-memory system" → `[~\|historical]` |
| claude_md_codeblocks > 0 | A: "Build and run commands" → `[~\|artifact]` |
| claude_md_lines > 30 | A: "Architecture and structure documentation" → `[~\|artifact]` |
| claude_md_onboarding > 0 | A: "Team conventions and contacts" + "Onboarding section" → `[~\|artifact]` |
| deny_rules is true | A: "Security-sensitive path exclusions" → `[✓\|artifact]` |
| global_permissions is true | B: "Scoped allowed-tools rules" → `[~\|artifact]` |
| hooks_global is true (personal hook) | B: "Hook design" → `[✓\|artifact]` |
| hooks_project is true (may be inherited) | B: "Hook design" → `[~\|artifact]` |
| mcp_user or mcp_project is true | B: "MCP server selection" → `[~\|artifact]` |
| settings_project and settings_global both true | B: "Project vs. global settings discipline" → `[~\|artifact]` |
| sessions > 5 | C: "Compact timing" → `[~\|historical]` |
| sessions > 10 | C: "Session naming" → `[~\|historical]` |

---

## Gap questions

| Branch | Gap | Ask this |
|--------|-----|------------|
| [ROOT] | No scope evidence | "Do you have a global `~/.claude/CLAUDE.md`? If so, what have you put in it that's different from your project CLAUDE.md?" |
| [ROOT] | Scoping judgment | "Give me one concrete thing you deliberately put in *global* scope and one you kept *project-local* — and why each belongs where it is, not the other way around." |
| [ROOT] | Auto-memory | "Have you run `/memory`? What does auto-memory capture on its own, and have you ever gone in and pruned or corrected what it saved?" |
| [A] | No build commands in CLAUDE.md | "Does your CLAUDE.md include the commands to build, test, and run the project? If not, what would a new engineer need to know that isn't there?" |
| [A] | Architecture docs | "Does your CLAUDE.md explain the codebase's shape — module responsibilities, key data flows, where to look first — or does it just restate file names? Quote me one line from it." |
| [A] | Team conventions | "Does your CLAUDE.md say who owns which system and where to ask questions, so Claude can cite it when advising on a PR? What's actually in there?" |
| [A] | No security exclusions | "Have you told Claude to stay away from any paths — like `.env` files or secrets directories? If so, where did you put that instruction?" |
| [A] | Onboarding section | "Does your CLAUDE.md carry a team-facing `## Onboarding` section with first-week guidance? What would a new hire read there on day one?" |
| [B] | No permission rules | "Have you written a permissions glob rule — like `Bash(npm run *)` — so Claude can run specific commands without asking every time? If so, what did you allow?" |
| [B] | No hook evidence | "Have you set up a hook that fires before or after Claude uses a tool? If so, what exit code does it return and what does it check?" |
| [B] | MCP selection | "Which MCP server did you pick for this project, and why that one specifically — what does it let Claude do here that it couldn't otherwise? (Not 'I installed a bunch.')" |
| [B] | Settings discipline | "How do you decide whether a setting belongs in your global settings vs. the project's? Give me one rule you keep global and one you keep repo-specific." |
| [C] | No compact evidence | "Do you have a personal rule for when to run `/compact`? For example, do you do it at the start of a new task, or when you feel the responses getting worse?" |
| [C] | Session naming | "Do you `/rename` sessions when meaningful work starts? Could you find a session from last week by name right now — and do you clear out the dead ones?" |
| [C] | No rewind evidence | "Have you used `Esc+Esc` to undo something Claude did? If so, can you describe what happened and why rewind was the right choice over starting over?" |

### Qualitative rubric for answers

Same rubric as claude-code topic:
- **`[✓]` Demonstrated**: Specific, verifiable detail only someone who has done it would know
- **`[~]` Self-reported**: Affirmative but vague
- **`[ ]` Not yet**: Negative, "not sure," or "heard of it but haven't tried"

### Answer → node mapping

| Answer contains | Node → status |
|-----------------|---------------|
| Specific explanation of what goes in global vs. project scope | ROOT: "Global vs. project vs. local scope" → `[✓\|reported]` |
| Vague awareness of multiple scopes | ROOT: "Global vs. project vs. local scope" → `[~\|reported]` |
| Specific example of choosing one scope over another | ROOT: "What belongs where" → `[✓\|reported]` |
| Has run `/memory` and describes curating or pruning the auto-memory file | ROOT: "Auto-memory system" → `[✓\|reported]` |
| Confirms CLAUDE.md has build commands | A: "Build and run commands" → `[✓\|reported]` |
| Quotes an architecture/data-flow line from their CLAUDE.md (not a filename restatement) | A: "Architecture and structure documentation" → `[✓\|reported]` |
| Names ownership, contacts, or review/deploy process content in their CLAUDE.md | A: "Team conventions and contacts" → `[✓\|reported]` |
| Describes security exclusion with specific path or rule | A: "Security-sensitive path exclusions" → `[✓\|reported]` |
| Describes a team-facing `## Onboarding` section with concrete first-week guidance | A: "Onboarding section for team tools" → `[✓\|reported]` |
| Specific glob rule or deny rule described | B: "Scoped allowed-tools rules" → `[✓\|reported]` |
| Exit code or hook output behavior described | B: "Hook design" → `[✓\|reported]` |
| Names a specific MCP server and a project-specific reason for choosing it | B: "MCP server selection and scope" → `[✓\|reported]` |
| States a deliberate global-vs-project split with an example rule on each side | B: "Project vs. global settings discipline" → `[✓\|reported]` |
| Personal /compact heuristic described | C: "Compact timing" → `[✓\|reported]` |
| Describes renaming sessions at the start and retrieving or deleting them by name | C: "Session naming and project hygiene" → `[✓\|reported]` |
| Specific rewind scenario described | C: "Rewind vs. restart judgment" → `[✓\|reported]` |

---

## Unlock thresholds

- Branch A unlocks when ROOT ≥ 2 `[✓]`
- Branch B unlocks when Branch A ≥ 3 `[✓]`
- Branch C unlocks when Branch B ≥ 2 `[✓]`

Both `[✓]` and `[~]` count toward unlock thresholds.

---

## Tier definitions

| Tier | Criterion |
|------|-----------|
| Explorer | ROOT incomplete — hasn't internalized the scope model |
| Builder | Branch A mostly done — writing useful CLAUDE.md files but not yet locking down configuration |
| Practitioner | Branch B done — deliberate about permissions, hooks, and MCP selection |
| Expert | Branch C done — session hygiene is second nature; configuration is minimal and intentional |

---

## Tree render template

```
Understand the scope hierarchy
    [?] Global vs. project vs. local scope
    [?] What belongs where (scoping judgment)
    [?] Auto-memory system (/memory command)

Writing effective CLAUDE.md files
    [?] Build and run commands
    [?] Architecture and structure documentation
    [?] Team conventions and contacts
    [?] Security-sensitive path exclusions
    [?] Onboarding section for team tools

Configuration patterns   [if locked: "(unlock: complete 3 CLAUDE.md skills)"]
    [?] Scoped allowed-tools rules
    [?] Hook design (exit codes and output)
    [?] MCP server selection and scope
    [?] Project vs. global settings discipline

Session hygiene   [if locked: "(unlock: complete 2 Configuration skills)"]
    [?] Compact timing and triggers
    [?] Session naming and project hygiene
    [?] Rewind vs. restart judgment
```

---

## Saved tree file template

When writing to `~/.claude/ramp/graphs/best-practices.md`, use this format:

```markdown
---
version: 3
topic: best-practices
user: [git config user.name or "unknown"]
email: [git config user.email or "unknown"]
updated: [today's date YYYY-MM-DD]
level: [Explorer / Builder / Practitioner / Expert]
xp: [CURRENT_XP]
---

# Best Practices Knowledge Graph

*[✓] Demonstrated · [~] Self-reported · [ ] Not yet · [★] Mastery target · [·] Locked*

## [ROOT] Understand the scope hierarchy
- [STATUS|TYPE] Global vs. project vs. local scope
- [STATUS|TYPE] What belongs where (scoping judgment)
- [STATUS|TYPE] Auto-memory system (/memory command)

## [A] Writing effective CLAUDE.md files
- [STATUS|TYPE] Build and run commands
- [STATUS|TYPE] Architecture and structure documentation
- [STATUS|TYPE] Team conventions and contacts
- [STATUS|TYPE] Security-sensitive path exclusions
- [STATUS|TYPE] Onboarding section for team tools

## [B] Configuration patterns
- [STATUS|TYPE] Scoped allowed-tools rules
- [STATUS|TYPE] Hook design (exit codes and output)
- [STATUS|TYPE] MCP server selection and scope
- [STATUS|TYPE] Project vs. global settings discipline

## [C] Session hygiene
- [STATUS|TYPE] Compact timing and triggers
- [STATUS|TYPE] Session naming and project hygiene
- [STATUS|TYPE] Rewind vs. restart judgment

## Frontier
- [frontier node name] — [criterion one-liner]

## Notes
<!-- Add personal notes here -->
```

**Demonstration evidence trail:** For `[✓]` nodes only, append `— [repo-name], [YYYY-MM-DD]: [brief note] | next: [YYYY-MM-DD] [L1]`.
Spaced repetition levels: L1=1d, L2=3d, L3=7d, L4=21d, L5=60d, L6=permanent.
