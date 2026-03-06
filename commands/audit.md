---
description: Repo audit — find and fix stale references, inconsistencies, and misaligned artifacts
allowed-tools: Read, Glob, Grep, Bash, Edit
---

## Auto-collected context

**Today's date**: !`date +%Y-%m-%d`

**CLAUDE.md (full)**:
!`cat CLAUDE.md 2>/dev/null || echo "not found"`

**README.md (first 120 lines)**:
!`head -120 README.md 2>/dev/null || echo "not found"`

**Actual file tree (max depth 3, excluding .git/.venv/node_modules)**:
!`find . -not -path './.git/*' -not -path './.venv/*' -not -path './node_modules/*' -not -path './__pycache__/*' -maxdepth 3 -type f | sort 2>/dev/null || echo "find failed"`

**commands/ directory**:
!`ls -1 commands/ 2>/dev/null || echo "none"`

**topics/ directory (with line counts)**:
!`ls -1 topics/ 2>/dev/null | while read f; do echo "$f ($(wc -l < topics/$f) lines)"; done || echo "none"`

**scripts/ directory**:
!`ls -1 scripts/ 2>/dev/null || echo "none"`

**mcp/ directory**:
!`ls -1 mcp/ 2>/dev/null || echo "none"`

**docs/ directory**:
!`ls -1 docs/ 2>/dev/null || echo "none"`

**hooks/hooks.json**:
!`cat hooks/hooks.json 2>/dev/null || echo "not found"`

**.claude/settings.json**:
!`cat .claude/settings.json 2>/dev/null || echo "not found"`

**.claude-plugin/plugin.json**:
!`cat .claude-plugin/plugin.json 2>/dev/null || echo "not found"`

**.gitignore**:
!`cat .gitignore 2>/dev/null || echo "not found"`

**.mcp.json.example**:
!`cat .mcp.json.example 2>/dev/null || echo "not found"`

**Knowledge tree schema files**:
!`ls -1 ~/.claude/knowledge-trees/schemas/ 2>/dev/null || echo "none or not found"`

**Git status**:
!`git status --short 2>/dev/null || echo "not a git repo"`

**Recent git tags**:
!`git tag --sort=-creatordate 2>/dev/null | head -5 || echo "none"`

**Command file frontmatter**:
!`for f in commands/*.md; do echo "=== $f ==="; head -6 "$f"; echo; done 2>/dev/null || echo "none"`

**JSON syntax check**:
!`python3 -c "
import json
files = ['.claude/settings.json', 'hooks/hooks.json', '.claude-plugin/plugin.json', '.mcp.json.example']
for f in files:
    try:
        json.load(open(f))
        print('OK: ' + f)
    except Exception as e:
        print('ERROR: ' + f + ': ' + str(e))
" 2>/dev/null || echo "python3 not available"`

**Python syntax check**:
!`python3 -m py_compile scripts/skill-observer.py 2>&1 && echo "OK: scripts/skill-observer.py" || echo "ERROR: scripts/skill-observer.py"; python3 -m py_compile scripts/file-size-warn.py 2>&1 && echo "OK: scripts/file-size-warn.py" || echo "ERROR: scripts/file-size-warn.py"; python3 -m py_compile mcp/server.py 2>&1 && echo "OK: mcp/server.py" || echo "ERROR: mcp/server.py"`

**Knowledge tree frontmatter** (user's actual trees):
!`python3 -c "
import os, glob
path = os.path.expanduser('~/.claude/knowledge-trees/')
for f in sorted(glob.glob(path + '*.md')):
    lines = open(f).readlines()
    front = []
    in_front = False
    for l in lines:
        if l.strip() == '---':
            if not in_front: in_front = True
            else: break
        elif in_front:
            front.append(l.rstrip())
    print('=== ' + os.path.basename(f) + ' ===')
    print('\n'.join(front))
    print()
" 2>/dev/null || echo "none"`

---

## Your role

You are a repo consistency auditor. Read all auto-collected context above and run the checks below. Be precise — compare what docs *claim* against what files *actually exist*. Do not hallucinate file contents; use only what was injected above.

---

## Audit checks

### Check 1 — Structure listing vs actual files (CLAUDE.md)

Find the `## Structure` code block in CLAUDE.md. Extract every file path listed. Compare against the actual file tree.

Flag:
- Files listed in Structure but NOT found in the actual file tree
- Files found in the actual file tree that are NOT listed in Structure (only flag files that seem like they should be documented — skip `.venv/`, `.git/`, `__pycache__/`, `.tmp` files, etc.)

### Check 2 — Topic node counts

CLAUDE.md and README.md may claim specific node counts per topic (e.g., "71 nodes", "15 nodes"). Compare these claims against the actual `topics/*.md` files. Proxy for node count: count lines containing ` | ` in each schema file (table rows). Flag any discrepancy of ±3 or more.

Also verify the topics listed under `## Topics` in CLAUDE.md match the actual files in `topics/`.

### Check 3 — Hook script references

For every `command:` value in `.claude/settings.json` and `hooks/hooks.json`:
- Extract the script path (strip shell variable prefixes like `${CLAUDE_PLUGIN_ROOT}/`)
- Check if that script path exists in the actual file tree
- Flag: referenced scripts that don't exist

### Check 4 — `.gitignore` completeness

Check for these common items that should typically be ignored:
- `.venv/` — Python virtual environment
- `.mcp.json` — local MCP config with absolute paths
- `__pycache__/` — Python bytecode
- `*.pyc` — compiled Python
- `.claude/knowledge-trees/local/` — personal local trees
- `.claude/settings.local.json` — local-only settings

Flag any that are missing from `.gitignore` but appear relevant to this repo.

### Check 5 — Plugin manifest consistency

Check `.claude-plugin/plugin.json` version field. Look for any version mentions in README.md. Flag if:
- Version in `plugin.json` differs from version mentioned in README
- No version mention found in README at all

### Check 6 — Cross-file topic consistency

Compare the topics listed in:
- CLAUDE.md `## Topics` section
- README.md (any topics table or list)
- Actual files in `topics/` directory

Flag: topics mentioned in docs but no corresponding file in `topics/`, or topic files that exist but aren't mentioned in either doc.

### Check 7 — Stale personal data in committed files

Scan CLAUDE.md, README.md, and files in `commands/`, `topics/`, `scripts/`, `mcp/`, `docs/`, `hooks/` for:
- Email addresses that look personal (not placeholder examples)
- GitHub usernames hardcoded in unexpected places (not in git config context or example URLs)

Flag any found.

### Check 8 — .mcp.json.example accuracy

Compare `.mcp.json.example` against what the README or CLAUDE.md says about MCP setup. Flag if the example uses `python3` without noting the venv requirement, or if the structure doesn't match what's documented.

### Check 9 — JSON file validity [LINT]

Interpret the "JSON syntax check" output. Flag any file that shows `ERROR:`.

- `[CRITICAL]` if any JSON file has a parse error — malformed JSON silently breaks hook execution and plugin loading

### Check 10 — Python syntax [LINT]

Interpret the "Python syntax check" output. Flag any file that shows `ERROR:`.

- `[CRITICAL]` if any `.py` file has a syntax error — the hook will fail silently on every tool use

### Check 11 — Command file frontmatter [LINT]

Interpret the "Command file frontmatter" output. For each `commands/*.md`:
- `[WARN]` if `description:` is missing — required for plugin command registration
- `[INFO]` if `allowed-tools:` is missing — command runs with default tool access (may be intentional)

### Check 12 — Knowledge tree v3 compliance [LINT]

Interpret the "Knowledge tree frontmatter" output. For each tree file found:
- `[WARN]` if `version:` is missing or not `3`
- `[WARN]` if any required field is absent: `topic`, `user`, `updated`, `level`, `xp`
- `[INFO]` if `email:` is absent (optional but recommended for multi-device sync)

---

## Output format

```
## Audit Results — [date]

### [N] issue(s) found

**[SEVERITY] Check N — Check name**
- Finding: [what's wrong, specific]
- Fix: [exact action needed]

[PASSED] Check N — Check name — ok
```

Severity levels:
- `[CRITICAL]` — broken references, missing files, hook scripts that don't exist
- `[WARN]` — doc drift, stale counts, version mismatches
- `[INFO]` — cosmetic, low-risk inconsistencies

List all issues first (most severe first within each check), then list passed checks at the bottom.

---

## After the report

Once you've listed all findings, ask:

> "Fix issues automatically? Reply `fix all`, `fix [N]` for specific ones (e.g. `fix 1 3`), or `skip` to review only."

If the user requests fixes: use Read + Edit to make targeted, minimal changes. Report each change as a one-liner: `[fixed] path/to/file — what changed`. Do not rewrite files wholesale — make surgical edits only.
