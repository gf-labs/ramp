---
description: Project status — architecture snapshot, knowledge tree health, and next steps
allowed-tools: Bash, mcp__knowledge-tree__list_topics, mcp__knowledge-tree__read_tree
---

## Auto-collected context

**Today's date**: !`date +%Y-%m-%d`

**Git branch + remote sync**:
!`git status -b --short 2>/dev/null | head -3 || echo "not a git repo"`

**Staged changes (ready to commit)**:
!`git diff --stat --cached HEAD 2>/dev/null || echo "none staged"`

**Unstaged changes**:
!`git diff --stat 2>/dev/null || echo "none"`

**Untracked files**:
!`git ls-files --others --exclude-standard 2>/dev/null | head -10 || echo "none"`

**Recent commits**:
!`git log --oneline -8 2>/dev/null || echo "no commits"`

**Commands** (`commands/`):
!`ls -1 commands/ 2>/dev/null || echo "none"`

**Topics** (`topics/`):
!`ls -1 topics/ 2>/dev/null || echo "none"`

**Scripts** (`scripts/`):
!`ls -1 scripts/ 2>/dev/null || echo "none"`

**MCP server** (`mcp/`):
!`ls -1 mcp/ 2>/dev/null || echo "none"`

**Docs** (`docs/`):
!`ls -1 docs/ 2>/dev/null || echo "none"`

**Hooks configured** (`.claude/settings.json`):
!`python3 -c "import json; d=json.load(open('.claude/settings.json')); h=d.get('hooks',{}); [print(k+':', len(v), 'handler(s)') for k,v in h.items()]" 2>/dev/null || echo "none or not found"`

**MCP server registered** (`~/.claude.json` local scope):
!`python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude.json'))); proj=os.getcwd(); pdata=d.get('projects',{}).get(proj,{}); servers=pdata.get('mcpServers',{}); print(list(servers.keys()) if servers else 'none')" 2>/dev/null || echo "none or not found"`

**Knowledge tree summary** (all topics):
!`python3 -c "
import re, os
from datetime import date
today = date.today().isoformat()
tree_dir = os.path.expanduser('~/.claude/knowledge-trees')
if not os.path.isdir(tree_dir):
    print('no trees found')
else:
    for fname in sorted(os.listdir(tree_dir)):
        if not fname.endswith('.md'): continue
        fpath = os.path.join(tree_dir, fname)
        try:
            c = open(fpath).read()
            topic = fname[:-3]
            level = (re.search(r'^level: (.+)$', c, re.M) or type('', (), {'group': lambda s,n: '?'})()).group(1)
            xp = (re.search(r'^xp: (.+)$', c, re.M) or type('', (), {'group': lambda s,n: '0'})()).group(1)
            updated = (re.search(r'^updated: (.+)$', c, re.M) or type('', (), {'group': lambda s,n: '?'})()).group(1)
            demonstrated = len(re.findall(r'\[✓', c))
            all_dates = re.findall(r'next: (\d{4}-\d{2}-\d{2})', c)
            due = sum(1 for d in all_dates if d <= today)
            nxt = min(all_dates) if all_dates else 'none'
            print(f'{topic} | {level} | {xp} XP | {demonstrated} demonstrated | due today: {due} | next review: {nxt}')
        except Exception as e:
            print(fname, '| error:', e)
" 2>/dev/null || echo "error reading knowledge trees"`

**Plugin version** (`.claude-plugin/plugin.json`):
!`python3 -c "import json; d=json.load(open('.claude-plugin/plugin.json')); print('v' + d.get('version','?'), '—', d.get('name','?'))" 2>/dev/null || echo "not found"`

---

## Your role

Read all auto-collected context above and produce a **project status report**. This is a read-only snapshot — no writes, no questions, no assessment.

Keep output scannable: headers + short bullets. No wall of prose.

---

## Status report structure

### Git state
- Branch and sync (commits ahead/behind remote)
- Staged changes: what's ready to commit (list file names from diff stats)
- Unstaged changes: what's modified but not staged
- Last 5 commits (one-liners)

### Architecture
Summarize what exists by directory:
- `commands/` — N commands: [names without .md extension]
- `topics/` — N schemas: [list]
- `scripts/` — [list]
- `mcp/` — [list]
- `docs/` — [list]
- Hooks: [which event types are configured]
- MCP server: [registered or not, server name if registered]

### Knowledge tree health
For each topic tree found (from the summary above):
- **[topic]** — [Level] · [XP] XP · [N] demonstrated · [N due today] due today · next review [date]

If any nodes are due today: "**[N] node(s) due for review** — run `/review` to work through them."

### Next steps
Infer the most actionable next steps from the data:
- If staged files exist: "Ready to commit: [N] files ([list])"
- If [~] nodes exist in the tree: "[N] self-reported nodes to demonstrate — run `/sup` to convert them"
- If due nodes exist: "Review due — run `/review`"
- If untracked files exist: "Untracked files to consider adding or ignoring"
- If no recent commits in N days: "No commits recently"
- Show the top 1–2 frontier nodes from the active tree as the learning focus

Keep next steps to 4–6 bullets maximum. Most important first.

---

## Constraints

- No writes
- No questions
- No assessment of knowledge
- Output fits in one screenful — be concise
