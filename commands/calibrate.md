---
description: Place yourself on a topic's skill tree — a pre-filled worksheet whose claims seed your graph
argument-hint: [topic — default: getting-started]
allowed-tools: Read, Write, Bash, mcp__knowledge-graph__read_graph, mcp__knowledge-graph__save_graph
---

## Context

**Today's date**: !`date +%Y-%m-%d`

**Active topic** (the topic the arguments name — multi-word names resolve, e.g. "object oriented design"; else getting-started):
!`python3 "$CLAUDE_PLUGIN_ROOT/ramp_core.py" resolve --default getting-started -- "$ARGUMENTS" 2>/dev/null || echo "getting-started"`

**Project** (workspace home + evidence trail):
!`P=$(cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)" && pwd -P); echo "$P (repo: $(basename "$P"))"`

**Topic schema** (node map + detection-signal table):
!`T=$(python3 "$CLAUDE_PLUGIN_ROOT/ramp_core.py" resolve --default getting-started -- "$ARGUMENTS" 2>/dev/null || echo "getting-started"); cat "$HOME/.claude/ramp/schemas/$T.md" 2>/dev/null || echo "NO_SCHEMA:$T"`

**Your saved graph** (merge base — nothing here is ever downgraded):
!`T=$(python3 "$CLAUDE_PLUGIN_ROOT/ramp_core.py" resolve --default getting-started -- "$ARGUMENTS" 2>/dev/null || echo "getting-started"); cat "$HOME/.claude/ramp/graphs/$T.md" 2>/dev/null || echo "NO_TREE_FILE:$T"`

**Scan signals** (raw evidence the schema's detection table consumes):
!`echo "CLAUDE.md lines: $([ -f CLAUDE.md ] && wc -l < CLAUDE.md | tr -d ' ' || echo 0)"; echo "git commits: $(git rev-list --count HEAD 2>/dev/null || echo 0)"; echo "claude sessions: $(find "$HOME/.claude/projects" -maxdepth 2 -name '*.jsonl' 2>/dev/null | wc -l | tr -d ' ')"; echo "project commands: $(ls .claude/commands/*.md 2>/dev/null | wc -l | tr -d ' ')"; echo "project hooks: $(python3 -c "import json;print(sorted(json.load(open('.claude/settings.json')).get('hooks',{}).keys()))" 2>/dev/null || echo none)"; echo "user mcp servers: $(python3 -c "import json,os;print(len(json.load(open(os.path.expanduser('~/.claude.json'))).get('mcpServers',{})))" 2>/dev/null || echo 0)"; echo "identity: $(git config user.name 2>/dev/null || echo unknown) <$(git config user.email 2>/dev/null || echo unknown)>"`

**Topic catalog** (for the Explore next block):
!`[ -n "$CLAUDE_PLUGIN_ROOT" ] && python3 "$CLAUDE_PLUGIN_ROOT/ramp_core.py" catalog 2>/dev/null || echo "CATALOG_UNAVAILABLE"`

**Kernel CLI** (the no-MCP write path):
!`[ -n "$CLAUDE_PLUGIN_ROOT" ] && [ -f "$CLAUDE_PLUGIN_ROOT/ramp_core.py" ] && echo "KERNEL_OK" || echo "KERNEL_UNAVAILABLE"`

**Existing placement worksheet** (`./.ramp/calibrate.md`):
!`cat .ramp/calibrate.md 2>/dev/null || echo "NO_CALIBRATE"`

---

## Your role

The front door. Write a placement worksheet the user marks up in their own time, then — when they say **done** — record their claims through the validated writer and start them at the right place. Two rules shape everything: detection outranks self-report (a claim never becomes `[✓]` here), and state lives in files, not scrollback.

The worksheet format is defined by the `## The ./.ramp/ workspace` contract in `up.md` (`### .ramp/calibrate.md`); the template in Step 3 mirrors it — if you change one, change both.

## Step 1 — Guards

- `NO_SCHEMA`: say "No schema found for **[topic]** — run `/ramp:list` to see what's available." Stop.
- If the existing worksheet already carries user marks (`[~]` or `[✓]` rows outside the detected block) that the saved graph doesn't reflect, those are unrecorded claims: say so and grade them now (Step 5) instead of overwriting. Regenerate only if the user asks.

## Step 2 — Pre-fill from evidence

Two sources, in priority order:

1. **Your saved graph** — every node already `[✓]` or `[~]` there enters the detected block with its status and a trimmed evidence one-liner.
2. **The schema's detection table** applied to the scan signals — pre-fill exactly the status the table grants (`[✓|artifact]` only where it says so; historical hints stay `[~]`). No signal, no pre-fill — never infer beyond the table.

Everything else renders `[ ]`.

## Step 3 — Write the workspace files

Create `./.ramp/` if missing (location rule in the contract: the repo's top level, else the working directory — resolved real path).

**`.ramp/calibrate.md`** (mirrors the contract template):

```markdown
# Place yourself — [topic] skill tree
Mark what you can already do. I'll verify the high-value ones; the rest seed your tree.
*[✓] I've done this (with evidence) · [~] I know this · [ ] not yet*

## Already detected on this machine  (the scan — see scan.md for scope)
- [✓] [node title] — [evidence one-liner]

## [Branch name]
- [ ] [node title]
- [ ] [node title]

## Explore next  (other skill trees — start with `/ramp:up <name>`)
- [topic] — [one-line description] ([N] nodes)

---
*Done? Say **done** — I'll record your claims and start you at the right place.*
```

- **Branch names:** render each schema section as its plain name only — the text after the closing `]`, minus any parenthetical unlock note. Never print the bracketed letter codes: they're internal XP weights, and placement should read as *where you are*, not labels.
- **Every schema node appears exactly once** — in the detected block (pre-filled) or under its branch (`[ ]`), never both.
- **Explore next:** up to 4 not-started topics from the catalog — name, one-line description, node count. On `CATALOG_UNAVAILABLE`, omit the block.

**`.ramp/scan.md`** (contract format): the scope actually scanned (project path, `~/.claude/` config, git history + Claude sessions), the explicit **Not looked at** boundary, and every pre-filled row with the evidence that triggered it. If nothing was detected, still write the scope + boundary with an empty findings list.

## Step 4 — Hand it over

One compact pointer in chat — no menus:

> **Place yourself — [topic]** → `.ramp/calibrate.md`
> [N] of [M] nodes pre-filled from the scan (scope: `.ramp/scan.md`). Mark the rest, then say **done** — claims seed your tree, and nothing you mark can lower what's already demonstrated.

## Step 5 — When they say **done**

1. **Read `.ramp/calibrate.md` fresh** — the marks live in the file. A claim stated in chat counts too; use their words as the note.
2. **Build the full updated tree:**
   - Graph exists: change only node lines; keep everything else verbatim.
   - `NO_TREE_FILE`: create one — YAML frontmatter (`version: 3`, `topic:`, `user:`/`email:` from the identity signal, `updated:` today, `level: Explorer`, `xp: 0` — the writer recomputes), the legend line, then one `##` header per schema section. Keep the schema's bracket text verbatim in graph headers — the writer's XP pass reads them; only the worksheet hides them.
   - Detected rows keep their pre-filled status with the scan evidence: `- [✓|artifact] [node title] — [repo], [today]: [evidence] via /ramp:calibrate` (or `[~|historical]` as granted).
   - User marks — both `[~]` and `[✓]` — become `- [~|reported] [node title] — [repo], [today]: claimed in /ramp:calibrate[ — their note]`. A `[✓]` mark with a written note is still `[~|reported]`: flag it high-value — it gets verified live in the first lesson or `/ramp:review`, where it can earn the upgrade.
   - Do not hand-write `| next:` or `xp:` — the writer owns both.
3. **Persist through the writer** (same ladder as `/ramp:check`):
   - MCP configured: call `mcp__knowledge-graph__save_graph(topic=[active-topic], content=[full updated tree])`.
   - No MCP, `KERNEL_OK`: run the CLI verb with the tree on stdin:

     ```bash
     python3 "$CLAUDE_PLUGIN_ROOT/ramp_core.py" save [active-topic] <<'RAMP_TREE'
     [the full updated tree]
     RAMP_TREE
     ```

     Exit 2 means the writer **REJECTED** the content — report its message verbatim and stop.
   - Neither: ramp's validated writer isn't reachable on this install — say so and stop; never simulate the save with Edits.
4. **Report the delta** from the writer's confirmation (`saved · [topic] · [level] · [XP] XP → [path]`): [N] claims recorded, [M] detected, XP now [X]. Numbers come from the writer, never your own arithmetic.
5. **Route into the first lesson:** "Next: `/ramp:up [topic]` — it reads your calibrated tree and delivers your first task to `.ramp/worksheet.md`."

## Constraints

- A claim never mints `[✓]` — detection or live demonstration only; never downgrade anything
- Full-tree persistence through `save_graph` or the CLI `save` verb only — no Edit-tool writes to the graph, ever
- The worksheet shows plain branch names; the graph file keeps the schema's bracket headers verbatim
- Pre-fill only what the saved graph or the schema's detection table supports — no inferred credit
- One topic per run; the worksheet is regenerable, but unrecorded marks are graded before any overwrite
- No menus — the worksheet is the interaction surface; chat gets the pointer and the delta
