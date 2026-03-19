## Ramp-specific context

**CLAUDE.md (full)**:
```bash
cat CLAUDE.md 2>/dev/null || echo "not found"
```

**README.md (first 120 lines)**:
```bash
head -120 README.md 2>/dev/null || echo "not found"
```

**Actual file tree (max depth 3, excluding .git/.venv/node_modules)**:
```bash
find . -not -path './.git/*' -not -path './.venv/*' -not -path './node_modules/*' -not -path './__pycache__/*' -maxdepth 3 -type f | sort 2>/dev/null || echo "find failed"
```

**commands/ directory**:
```bash
ls -1 commands/ 2>/dev/null || echo "none"
```

**topics/ directory (with line counts)**:
```bash
ls -1 topics/ 2>/dev/null | while read f; do echo "$f ($(wc -l < topics/$f) lines)"; done || echo "none"
```

**scripts/ directory**:
```bash
ls -1 scripts/ 2>/dev/null || echo "none"
```

**mcp/ directory**:
```bash
ls -1 mcp/ 2>/dev/null || echo "none"
```

**docs/ directory**:
```bash
ls -1 docs/ 2>/dev/null || echo "none"
```

**hooks/hooks.json**:
```bash
cat hooks/hooks.json 2>/dev/null || echo "not found"
```

**.claude/settings.json**:
```bash
cat .claude/settings.json 2>/dev/null || echo "not found"
```

**.claude-plugin/plugin.json**:
```bash
cat .claude-plugin/plugin.json 2>/dev/null || echo "not found"
```

**.gitignore**:
```bash
cat .gitignore 2>/dev/null || echo "not found"
```

**.mcp.json.example**:
```bash
cat .mcp.json.example 2>/dev/null || echo "not found"
```

**Knowledge graph frontmatter** (user's actual trees):
```bash
python3 -c "
import os, glob
path = os.path.expanduser('~/.claude/knowledge-graphs/')
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
" 2>/dev/null || echo "none"
```

**Git status**:
```bash
git status --short 2>/dev/null || echo "not a git repo"
```

**Recent git tags**:
```bash
git tag --sort=-creatordate 2>/dev/null | head -5 || echo "none"
```

**Command file frontmatter**:
```bash
for f in commands/*.md; do echo "=== $f ==="; head -6 "$f"; echo; done 2>/dev/null || echo "none"
```

**Stale plugin command syntax** (unnamespaced /cmd refs in committed files):
```bash
grep -rn --include="*.md" -E "/(ramp|tree|review|cheatsheet|status|audit)[ \`\[]" commands/ CLAUDE.md README.md 2>/dev/null | grep -v "ramp:" || echo "none"
```

**Plugin cache sync**:
```bash
python3 -c "
import json
from pathlib import Path
settings = json.loads((Path.home() / '.claude' / 'settings.json').read_text())
enabled = settings.get('enabledPlugins', {})
cache_base = Path.home() / '.claude' / 'plugins' / 'cache'
marketplaces = settings.get('extraKnownMarketplaces', {})
for plugin_at_market, active in enabled.items():
    if not active: continue
    parts = plugin_at_market.split('@', 1)
    if len(parts) != 2: continue
    plugin, market = parts
    m = marketplaces.get(market, {})
    source_path = m.get('source', {}).get('path', '') if isinstance(m, dict) else ''
    cache_plugin = cache_base / market / plugin
    cached_versions = sorted(cache_plugin.iterdir()) if cache_plugin.exists() else []
    if not cached_versions:
        print(f'{plugin_at_market}: NO_CACHE')
        continue
    latest = cached_versions[-1]
    cached = set(f.stem for f in (latest / 'commands').glob('*.md')) if (latest / 'commands').exists() else set()
    source = set(f.stem for f in (Path(source_path) / 'commands').glob('*.md')) if source_path and (Path(source_path) / 'commands').exists() else set()
    stale = cached - source
    missing = source - cached
    if stale or missing:
        print(f'DRIFT: stale={sorted(stale)}, missing={sorted(missing)}')
    else:
        print(f'IN_SYNC: {len(cached)} commands (latest cache: {latest.name})')
" 2>/dev/null || echo "check failed"
```

**Schema symlinks**:
```bash
python3 -c "
from pathlib import Path
schemas_dir = Path.home() / '.claude' / 'knowledge-graphs' / 'schemas'
if not schemas_dir.exists():
    print('MISSING')
else:
    for f in sorted(schemas_dir.iterdir()):
        try:
            target = f.resolve(strict=True)
            print(f'OK: {f.name} -> {target}')
        except OSError:
            print(f'BROKEN: {f.name}')
" 2>/dev/null || echo "check failed"
```

**Project .mcp.json**:
```bash
cat .mcp.json 2>/dev/null || echo "NOT FOUND"
```

---

## Ramp-specific checks

Run these checks. Prefix findings S1–S15. Same severity model ([CRITICAL] / [WARN] / [INFO] / [PASSED]).

### S1 — Structure listing vs actual files (CLAUDE.md)

Find the `## Structure` code block in CLAUDE.md. Extract every file path listed. Compare against the actual file tree.

Flag:
- Files listed in Structure but NOT found in the actual file tree
- Files found in the actual file tree that are NOT listed in Structure (only flag files that seem like they should be documented — skip `.venv/`, `.git/`, `__pycache__/`, `.tmp` files, etc.)

### S2 — Topic node counts

CLAUDE.md and README.md may claim specific node counts per topic. Compare these claims against the actual `topics/*.md` files. Proxy for node count: count lines containing ` | ` in each schema file. Flag any discrepancy of ±3 or more.

Also verify the topics listed under `## Topics` in CLAUDE.md match the actual files in `topics/`.

### S3 — Hook script references

For every `command:` value in `.claude/settings.json` and `hooks/hooks.json`:
- Extract the script path (strip shell variable prefixes like `${CLAUDE_PLUGIN_ROOT}/`)
- Check if that script path exists in the actual file tree
- Flag: referenced scripts that don't exist

### S4 — `.gitignore` completeness

Check for these common items that should typically be ignored:
- `.venv/` — Python virtual environment
- `.mcp.json` — local MCP config with absolute paths
- `__pycache__/` — Python bytecode
- `*.pyc` — compiled Python
- `.claude/knowledge-graphs/local/` — personal local trees
- `.claude/settings.local.json` — local-only settings

Flag any that are missing from `.gitignore` but appear relevant to this repo.

### S5 — Plugin manifest consistency

Check `.claude-plugin/plugin.json` version field. Look for any version mentions in README.md. Flag if:
- Version in `plugin.json` differs from version mentioned in README
- No version mention found in README at all

### S6 — Cross-file topic consistency

Compare the topics listed in:
- CLAUDE.md `## Topics` section
- README.md (any topics table or list)
- Actual files in `topics/` directory

Flag: topics mentioned in docs but no corresponding file in `topics/`, or topic files that exist but aren't mentioned in either doc.

### S7 — Stale personal data in committed files

Scan CLAUDE.md, README.md, and files in `commands/`, `topics/`, `scripts/`, `mcp/`, `docs/`, `hooks/` for:
- Email addresses that look personal (not placeholder examples)
- GitHub usernames hardcoded in unexpected places

Flag any found.

### S8 — .mcp.json.example accuracy

Compare `.mcp.json.example` against what the README or CLAUDE.md says about MCP setup. Flag if the example uses `python3` without noting the venv requirement, or if the structure doesn't match what's documented.

### S9 — Command file frontmatter [LINT]

Interpret the "Command file frontmatter" output. For each `commands/*.md`:
- `[WARN]` if `description:` is missing — required for plugin command registration
- `[INFO]` if `allowed-tools:` is missing — command runs with default tool access (may be intentional)

### S10 — Knowledge graph v3 compliance [LINT]

Interpret the "Knowledge graph frontmatter" output. For each tree file found:
- `[WARN]` if `version:` is missing or not `3`
- `[WARN]` if any required field is absent: `topic`, `user`, `updated`, `level`, `xp`
- `[INFO]` if `email:` is absent (optional but recommended for multi-device sync)

### S11 — Plugin command syntax [LINT]

Interpret the "Stale plugin command syntax" output. For each match:
- `[WARN]` if a committed file contains a user-facing command reference like `/tree`, `/ramp`, `/review`, `/cheatsheet`, `/status`, or `/audit` without the `ramp:` namespace prefix
- Fix: replace with the namespaced form (`/ramp:tree`, `/ramp:review`, etc.)

Exclude: lines beginning with `!` (bash injections), and lines in sections explicitly documenting historical or old syntax.

### S12 — Python semantic naming [LINT]

Scan all `.py` files in `scripts/` and `mcp/` for stale naming from the `knowledge-tree` era:
- `knowledge-tree` or `knowledge_tree`
- `TREE_DIR` or `SKILL_TREE_PATH`
- `/trees/` in URL strings
- `read_tree` or `save_tree` as function/variable names

`[WARN]` for each stale identifier found.

To collect:
```bash
grep -n "knowledge.tree\|TREE_DIR\|SKILL_TREE_PATH\|/trees/\|read_tree\|save_tree" scripts/*.py mcp/*.py 2>/dev/null || echo "none"
```

### S13 — Plugin cache sync

Read the plugin cache sync output above.
- `[CRITICAL]` if `NO_CACHE` — plugin not installed or cache missing; run `/plugin install ramp@gfl-marketplace`
- `[WARN]` if `DRIFT` — cached commands differ from live repo; run `/plugin install ramp@gfl-marketplace` to refresh
- `[PASSED]` if `IN_SYNC`

### S14 — Schema symlinks

Read the schema symlinks output above.
- `[CRITICAL]` if `MISSING` — `~/.claude/knowledge-graphs/schemas/` doesn't exist; SessionStart hook should create it on next session
- `[CRITICAL]` if any symlink shows `BROKEN` — stale symlink from old plugin cache; restart session to trigger SessionStart hook
- `[PASSED]` if all symlinks show `OK`

### S15 — MCP config present

Read the project .mcp.json output above.
- `[INFO]` if `NOT FOUND` — `.mcp.json` absent; knowledge-graph MCP features unavailable (local-only mode); copy `.mcp.json.example` → `.mcp.json` to enable
- `[PASSED]` if present — MCP server configured
