---
topic: configuration
node_count: 13
version: 1
source_url: https://code.claude.com/docs/en/settings
description: Claude Code configuration — settings hierarchy, permissions, sandboxing, model selection, terminal, keybindings, and interface customization.
---

# Configuration Knowledge Graph Schema

This file defines the curriculum for the `configuration` topic. Covers the Configuration docs section: settings, permissions, sandboxing, terminal-config, model-config, fast-mode, statusline, keybindings.

---

## Node definitions

13 nodes across 3 branches.

### [ROOT] Settings fundamentals (always unlocked — 4 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|-----------|
| Settings scope hierarchy: global, project, local | Can describe all three settings scopes (`~/.claude/settings.json`, `.claude/settings.json`, `.claude/settings.local.json`), which takes precedence, and what each is for | Qualitative | settings file exists → `[~\|artifact]` | https://code.claude.com/docs/en/settings |
| Settings file format and key options | Has edited a settings.json; knows the key fields: `permissions` (and its nested `defaultMode`), `hooks`, `mcpServers`, `model`, `env`; can add a field without breaking the file | Artifact / Exercise | settings file with non-empty content → `[✓\|artifact]` | https://code.claude.com/docs/en/settings |
| Model selection and budget configuration | Has explicitly set `model` in settings.json; can explain the tradeoff between model capability and cost/speed; knows available model IDs and that there is no settings.json token/budget cap (cost limits come from the `--max-budget-usd` headless flag or API-side limits, not `maxTokens`) | Artifact / Qualitative | `model` in settings → `[✓\|artifact]` | https://code.claude.com/docs/en/model-config |
| Server-managed settings (policy enforcement) | Understands that admins can push settings that users cannot override; knows the difference between user-settable and org-enforced config | Qualitative | None | https://code.claude.com/docs/en/settings |

### [A] Permissions and security (5 nodes, unlocks when ROOT ≥ 2 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|-----------|
| Permissions: allow/deny rules and glob patterns | Has written at least one allow rule (e.g., `Bash(npm run *)`) or deny rule; can explain glob syntax and precedence; knows `/permissions` to inspect current state | Artifact / Exercise | global permission rules > 0 → `[✓\|artifact]` | https://code.claude.com/docs/en/permissions |
| Permission precedence and scoping | Can trace how permissions resolve when global, project, and local settings conflict; understands deny overrides allow at the same level | Qualitative | global + project permissions both present → `[~\|historical]` | https://code.claude.com/docs/en/permissions |
| Sandboxing configuration | Knows what sandboxing does (restricts file system and network access for tool calls); has configured or deliberately left it at default; understands the performance tradeoff | Qualitative | None | https://code.claude.com/docs/en/sandboxing |
| Fast mode | Has toggled fast mode with `/fast`; can explain what it changes (faster output on Opus, not a smaller model) and when to use it; knows the only related settings key is `fastModePerSessionOptIn` — there is no `fastMode` toggle key | Exercise / Qualitative | `fastModePerSessionOptIn` in settings → `[~\|artifact]` | https://code.claude.com/docs/en/fast-mode |
| Plan mode as default | Has set `permissions.defaultMode: plan` in settings (the documented location — `defaultMode` lives under the `permissions` object); understands what plan mode prevents (no file writes, no bash execution) and when it's the right default | Artifact | `defaultMode: plan` set, under `permissions` or top-level → `[✓\|artifact]` | https://code.claude.com/docs/en/settings |

### [B] Interface customization (4 nodes, unlocks when Branch A ≥ 2 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|-----------|
| Terminal configuration | Has customized terminal behavior (color, width, or rendering settings); or knows the relevant config keys and why they matter for different terminal emulators | Qualitative | None | https://code.claude.com/docs/en/terminal-config |
| Status line customization | Has configured the Claude Code status line (shows token count, model, session info); knows which information it surfaces and how to toggle it | Exercise / Qualitative | None | https://code.claude.com/docs/en/statusline |
| Keybindings customization | Has modified `~/.claude/keybindings.json`; knows the default bindings (Shift+Tab for plan, Esc for cancel, Esc+Esc for rewind) and has changed at least one | Artifact | `~/.claude/keybindings.json` exists with content → `[✓\|artifact]` | https://code.claude.com/docs/en/keybindings |
| Interactive mode features | Has used: plan mode (Shift+Tab), rewind/checkpointing (Esc+Esc), session naming (`/rename`), and the session history picker; can describe what each does | Exercise / Historical | sessions > 5 → `[~\|historical]` | https://code.claude.com/docs/en/terminal-config |

---

## Detection signals

| Collected evidence | Node → status |
|--------------------|---------------|
| settings file exists with non-empty content | ROOT: "Settings file format and key options" → `[✓\|artifact]` |
| settings file exists (any) | ROOT: "Settings scope hierarchy" → `[~\|artifact]` |
| `model` in settings | ROOT: "Model selection and budget configuration" → `[✓\|artifact]` |
| global permission rules > 0 | A: "Permissions: allow/deny rules" → `[✓\|artifact]` |
| global + project permissions both present | A: "Permission precedence and scoping" → `[~\|historical]` |
| `fastModePerSessionOptIn` in settings | A: "Fast mode" → `[~\|artifact]` |
| `defaultMode: plan` set (under `permissions` or top-level) | A: "Plan mode as default" → `[✓\|artifact]` |
| `~/.claude/keybindings.json` exists with content | B: "Keybindings customization" → `[✓\|artifact]` |
| sessions > 5 | B: "Interactive mode features" → `[~\|historical]` |

---

## Gap questions

| Branch | Gap | Ask this |
|--------|-----|----------|
| [ROOT] | No settings hierarchy evidence | "Walk me through the three settings files Claude Code uses and what each one is for. Where would you put a setting that only applies to one repo vs. one that applies everywhere?" |
| [ROOT] | No model config evidence | "Have you ever set `model` in your settings to pin a default model? What were you trying to achieve and what tradeoff (capability vs. cost/speed) did you navigate?" |
| [ROOT] | No server-managed evidence | "Do you know what server-managed settings are and why an organization would use them? What can they enforce that users can't override?" |
| [A] | No permissions evidence | "Have you written a custom allow or deny rule for Claude? Walk me through what rule you wrote, where you put it, and what problem it solved." |
| [A] | No sandboxing evidence | "Do you know what sandboxing does in Claude Code? Have you configured it, and if so, what did you change and why?" |
| [A] | No fast mode evidence | "Have you used fast mode? When would you reach for it vs. leaving it off?" |
| [B] | No keybindings evidence | "Have you modified your Claude Code keybindings? What did you change and why?" |
| [B] | No interactive mode evidence | "Walk me through the interactive mode features you use regularly: plan mode, rewind, session naming. Which do you reach for most?" |

### Qualitative rubric

- **`[✓]` Demonstrated**: Contains a specific field name, file path, tradeoff, or observed behavior. "I set `model` to a Haiku ID for my read-only commands to cut cost" counts. "Yes I've configured it" doesn't.
- **`[~]` Self-reported**: Affirmative but vague. Knows the feature exists but no specific detail.
- **`[ ]` Not yet**: No exposure or negative answer.

### Answer → node mapping

| Answer contains | Node → status |
|-----------------|---------------|
| Names global, project, and local scopes with correct file paths | ROOT: "Settings scope hierarchy" → `[✓\|reported]` |
| Specific model ID set via `model` with rationale | ROOT: "Model selection and budget configuration" → `[✓\|reported]` |
| Description of server-managed settings enforcement | ROOT: "Server-managed settings" → `[✓\|reported]` |
| Specific glob rule (e.g., `Bash(npm run *)`) | A: "Permissions: allow/deny rules" → `[✓\|reported]` |
| Description of `permissions.defaultMode: plan` | A: "Plan mode as default" → `[✓\|reported]` |
| Description of fast mode use case | A: "Fast mode" → `[✓\|reported]` |
| Description of keybinding change | B: "Keybindings customization" → `[✓\|reported]` |
| Description of plan mode, rewind, or session naming with specifics | B: "Interactive mode features" → `[✓\|reported]` |

---

## Unlock thresholds

- Branch A unlocks when ROOT ≥ 2 `[✓]`
- Branch B unlocks when Branch A ≥ 2 `[✓]`

Both `[✓]` and `[~]` count toward unlock thresholds.

---

## Tier definitions

| Tier | Criterion |
|------|-----------|
| Explorer | ROOT incomplete |
| Builder | ROOT complete, Branch A in progress |
| Practitioner | Branch A complete, Branch B active |
| Expert | All branches complete |

---

## Tree render template

```
[ROOT] Settings Fundamentals
    [?] Settings scope hierarchy: global, project, local
    [?] Settings file format and key options
    [?] Model selection and budget configuration
    [?] Server-managed settings (policy enforcement)

[A] Permissions and Security   [if locked: "(unlock: complete 2 Settings Fundamentals)"]
    [?] Permissions: allow/deny rules and glob patterns
    [?] Permission precedence and scoping
    [?] Sandboxing configuration
    [?] Fast mode
    [?] Plan mode as default

[B] Interface Customization   [if locked: "(unlock: complete 2 Permissions & Security skills)"]
    [?] Terminal configuration
    [?] Status line customization
    [?] Keybindings customization
    [?] Interactive mode features
```

---

## Saved tree file template

```markdown
---
version: 3
topic: configuration
user: [git config user.name or "unknown"]
email: [git config user.email or "unknown"]
updated: [today's date YYYY-MM-DD]
level: [Explorer / Builder / Practitioner / Expert]
xp: [CURRENT_XP]
---

# Configuration Knowledge Graph

*[✓] Demonstrated · [~] Self-reported · [ ] Not yet · [★] Mastery target · [·] Locked*

## [ROOT] Settings Fundamentals
- [STATUS|TYPE] Settings scope hierarchy: global, project, local
- [STATUS|TYPE] Settings file format and key options
- [STATUS|TYPE] Model selection and budget configuration
- [STATUS|TYPE] Server-managed settings (policy enforcement)

## [A] Permissions and Security
- [STATUS|TYPE] Permissions: allow/deny rules and glob patterns
- [STATUS|TYPE] Permission precedence and scoping
- [STATUS|TYPE] Sandboxing configuration
- [STATUS|TYPE] Fast mode
- [STATUS|TYPE] Plan mode as default

## [B] Interface Customization
- [STATUS|TYPE] Terminal configuration
- [STATUS|TYPE] Status line customization
- [STATUS|TYPE] Keybindings customization
- [STATUS|TYPE] Interactive mode features

## Frontier
- [frontier node name] — [criterion one-liner]

## Notes
<!-- Add personal notes here -->
```
