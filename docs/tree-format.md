# Knowledge Graph File Format

Canonical reference for the v3 knowledge graph file format.

**Location:** `~/.claude/knowledge-graphs/[topic].md`
**Written by:** `/ramp:up` (Phase 4, option a) and `skill-observer.py`
**Read by:** `/ramp:up` (Phase 2 inference), `/ramp:tree`, `/ramp:review`, `/ramp:cheatsheet`

---

## Annotated example

```markdown
---
version: 3                          # Schema version — always 3 for new files
topic: claude-code                  # Topic name (matches filename stem)
user: [Your Name]                   # From git config user.name
email: [your@email.com]             # From git config user.email
updated: YYYY-MM-DD                 # Date of last write
level: Builder                      # Derived tier: Explorer / Builder / Practitioner / Expert
xp: 240                             # Computed XP total (see XP system below)
---

# Claude Code Knowledge Graph

*[✓] Demonstrated · [~] Self-reported · [ ] Not yet · [★] Mastery target · [·] Locked*

## [ROOT] Configure Claude
- [✓|artifact] CLAUDE.md with project guidance — my-repo, 2026-03-04: 80+ lines with build commands and architecture | next: 2026-03-05 [L1]
- [✓|exercise] Model or budget settings configured — my-repo, 2026-03-04: set claude-sonnet-4-6 as default; understands Haiku/Sonnet/Opus tradeoffs | next: 2026-03-05 [L1]
- [~|reported] /memory audit and CLAUDE.md hierarchy
- [ ] CLI fundamentals (/help, /doctor, /usage)

## [A] Memory and Context Management
- [✓|historical] Permissions system (/permissions, globs) — my-repo, 2026-03-01: 12 allow rules in ~/.claude/settings.json | next: 2026-03-08 [L2]
- [ ] Context window and /compact usage
- [ ] Session naming and resumption

## [B] Codebase Navigation
- [ ] Read + Glob + Grep exploration
- [ ] Explain an unfamiliar module

## [C] Code Change Workflows
- [~|historical] Multi-file coordinated changes — my-repo, 2026-02-20: 20-file commit detected
- [ ] Single-file edits with context

## [D] Agents and Orchestration
- [ ] Parallel subagents
- [·] Worktrees for parallel development

## [E] Automation and Extension
- [·] PostToolUse hooks
- [·] Custom MCP server

## Frontier
- Context window and /compact usage — use /compact deliberately; explain compact vs clear, token cost
- Session naming and resumption — use /rename, understand session resume flow

## Notes
<!-- Add personal notes here -->
```

---

## Field reference

### Frontmatter fields

| Field | Type | Description |
|-------|------|-------------|
| `version` | int | Always `3` for new files. v1/v2 files are auto-migrated on next write. |
| `topic` | string | Topic name — matches filename stem (e.g., `claude-code` for `claude-code.md`) |
| `user` | string | From `git config user.name` at time of write |
| `email` | string | From `git config user.email` at time of write |
| `updated` | date | ISO date of last write (YYYY-MM-DD) |
| `level` | string | Derived tier label: Explorer / Builder / Practitioner / Expert |
| `xp` | int | Computed XP total — always recomputed on write, never preserved stale |

### Node status markers

| Marker | Meaning | Saved as |
|--------|---------|----------|
| `[✓]` | Demonstrated — artifact found, exercise completed, or history verified | `[✓\|TYPE]` |
| `[~]` | Self-reported — claimed but not corroborated | `[~\|reported]` |
| `[ ]` | Not yet | `[ ]` |
| `[★]` | Frontier / mastery target | Display only — not saved |
| `[·]` | Locked (dependency not met) | Display only — not saved |

### Demonstration types (TYPE field)

| Type | How earned |
|------|-----------|
| `artifact` | File or config detected in environment scan |
| `exercise` | Completed live in session |
| `historical` | Verified from git log, session history, or directory structure |
| `reported` | Self-reported answer to gap question (Feynman-framed) |

### Evidence trail + spaced repetition field

`[✓]` nodes only. Format:
```
— [repo-name], YYYY-MM-DD: [brief note] | next: YYYY-MM-DD [LN]
```

Example:
```
- [✓|artifact] CLAUDE.md with project guidance — my-repo, 2026-03-04: 80+ lines | next: 2026-03-05 [L1]
```

**Interval ladder:** L1=1d · L2=3d · L3=7d · L4=21d · L5=60d · L6=permanent (no further review)

`[~]` and `[ ]` nodes have no evidence trail and no `next:` field.

---

## XP system

XP is computed per branch tier. `[✓]` = full XP. `[~]` = half XP (floor). `[ ]` = 0.

| Branch | XP per node |
|--------|-------------|
| ROOT | 10 |
| [A] | 15 |
| [B] | 20 |
| [C] | 25 |
| [D] | 35 |
| [E] | 50 |

---

## Merge rules (when an existing file is updated)

- Never downgrade `[✓]` to `[~]` or `[ ]`
- Preserve existing evidence trails and `next:` schedules — do not reset
- New `[✓]` nodes from this session get `| next: [today+1d] [L1]`
- Existing `[✓]` nodes without a `next:` field: add `| next: [today+1d] [L1]` on first v3 write
- Update `updated:` date and recompute `xp:` on every write

---

## Version migration

| Source version | Migration |
|----------------|-----------|
| v1 | Treat all `[✓]` as `[✓\|historical]`; add `next:` fields; recompute XP |
| v2 | Add `next:` fields to `[✓]` nodes that lack them; recompute XP |
| v3 | No migration needed |
