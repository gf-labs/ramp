## Ramp-specific context

**Plugin version**:
```bash
python3 -c "import json; d=json.load(open('.claude-plugin/plugin.json')); print('v' + d.get('version','?'), '—', d.get('name','?'))" 2>/dev/null || echo "not found"
```

**commands/ (names)**:
```bash
ls -1 commands/ 2>/dev/null || echo "none"
```

**topics/ (names)**:
```bash
ls -1 topics/ 2>/dev/null || echo "none"
```

**scripts/ (names)**:
```bash
ls -1 scripts/ 2>/dev/null || echo "none"
```

**mcp_server/ (Python files)**:
```bash
ls -1 mcp_server/*.py 2>/dev/null || echo "none"
```

**docs/ (names)**:
```bash
ls -1 docs/ 2>/dev/null || echo "none"
```

**Knowledge graph summary** (all topics):
```bash
python3 -c "
import re, os
from datetime import date
today = date.today().isoformat()
tree_dir = os.path.expanduser('~/.claude/knowledge-graphs')
if not os.path.isdir(tree_dir):
    print('no graphs found')
else:
    found = [f for f in sorted(os.listdir(tree_dir)) if f.endswith('.md')]
    if not found:
        print('no graph files')
    for fname in found:
        fpath = os.path.join(tree_dir, fname)
        try:
            c = open(fpath).read()
            topic = fname[:-3]
            level_m = re.search(r'^level: (.+)$', c, re.M)
            xp_m = re.search(r'^xp: (.+)$', c, re.M)
            level = level_m.group(1) if level_m else '?'
            xp = xp_m.group(1) if xp_m else '0'
            demonstrated = len(re.findall(r'\[✓', c))
            self_reported = len(re.findall(r'\[~\]', c))
            all_dates = re.findall(r'next: (\d{4}-\d{2}-\d{2})', c)
            due = sum(1 for d in all_dates if d <= today)
            nxt = min(all_dates) if all_dates else 'none'
            frontier = re.findall(r'^- \[ \] (.+)$', c, re.M)
            top_frontier = frontier[:2]
            print(f'TOPIC={topic}')
            print(f'  level={level} xp={xp} demonstrated={demonstrated} self_reported={self_reported}')
            print(f'  due_today={due} next_review={nxt}')
            print(f'  frontier={top_frontier}')
        except Exception as e:
            print(fname, '| error:', e)
" 2>/dev/null || echo "error reading knowledge graphs"
```

---

## Additional sections to render

After the generic Architecture section, render the following two sections:

### Ramp architecture
Using the ramp-specific dir listings above:
- Plugin: [v and name from plugin version output]
- commands/ — [N]: [names without .md extension]
- topics/ — [N]: [names without extension]
- scripts/ — [N]: [names]
- mcp_server/: [Python file names]
- docs/: [names]
- Hooks: [from main context hooks output]
- MCP: [from main context MCP output]

### Knowledge graph health
For each TOPIC block from the KG summary above:
- **[topic]** — [Level] · [XP] XP · [N] demonstrated · [N] due today · next review [date]
  Frontier: [top 1–2 node names, or "none"] · [N] self-reported

If any due_today > 0 across all topics: append "**[total N] node(s) due for review** — run `/ramp:review`"

---

## Next steps additions

Append these bullets to the main Next steps section (after git-inferred bullets):
- If due_today > 0 for any topic: "Review due — `/ramp:review` ([N] nodes)"
- If self_reported > 0 for any topic: "[N] self-reported to demonstrate — `/ramp:up`"
- If frontier is non-empty: "Learning focus: [node1][, node2]"
