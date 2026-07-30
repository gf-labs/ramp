---
description: Generate knowledge-graph topic schemas from an external source — book, docs site, spec, or file
argument-hint: "[topic-name] [/path/to/source.pdf or https://...]"
allowed-tools: Read, Glob, Grep, Bash, Write, Edit, WebFetch
---

## Auto-collected context

**Arguments**: $ARGUMENTS

**Today's date**: !`date +%Y-%m-%d`

**Resolved schema dir** (what the kernel CLI reads — first match wins):
!`python3 -c "import os,sys; sys.path.insert(0, os.environ.get('CLAUDE_PLUGIN_ROOT','.')); import ramp_core; print(ramp_core._schema_dir())" 2>/dev/null || echo "UNRESOLVED"`

**Existing topics** (name · node_count):
!`python3 "${CLAUDE_PLUGIN_ROOT}/ramp_core.py" catalog 2>/dev/null | python3 -c "import json,sys; [print(t['name'], t['node_count'], sep=' · ') for t in json.load(sys.stdin)]" 2>/dev/null || echo "CATALOG_UNAVAILABLE"`

**Plugin root**: !`echo "${CLAUDE_PLUGIN_ROOT:-unset}"`

**Authoring contract**: `${CLAUDE_PLUGIN_ROOT}/docs/topic-authoring.md` — the normative
standard. Read it in Phase 0 before generating anything. This command implements it; on any
disagreement between this file and that one, **the contract wins**.

---

## Your role

You are the `/ramp:ingest` command. You generate a complete, **contract-conformant** topic
schema from external source material.

The definition of done is mechanical and non-negotiable: `ramp_core.py lint <topic>` reports
**zero problems and zero advisories**. A schema that does not pass is not delivered.

Work through the phases sequentially. **Write no files until the Phase 3 gate.** After that
gate, run to completion without further prompting.

---

## Phase 0 — Arguments, contract, and target

**Read `docs/topic-authoring.md` in full before anything else.** It is the specification you
are implementing; the templates below are a summary of it, not a replacement for it.

Parse `$ARGUMENTS`: first word = `topic-name`, remainder = `source`.

- No `topic-name`: ask "What topic name should I use? (e.g. `object-oriented-design`)" and wait.
- No `source`: ask "What source material should I read? A file path or URL." and wait.
- `topic-name` already in **Existing topics**: warn — "Topic `[name]` already exists. Extend it,
  or abort?" Wait. On extend, proceed with a gap-fill focus in Phase 2.
- `topic-name` must be a valid filename stem: lowercase, hyphens, no spaces. It becomes the
  `topic:` frontmatter value and the node-id prefix, and both are frozen after ship.

**Source type:**
- `.pdf` → Read tool, paginated (max 20 pages/call; read in chunks until covered)
- `http://` / `https://` → WebFetch
- any other local file → Read tool

### Choose the target (ask — never assume)

A schema can live in three places. Ask which, and state the consequence of each:

```
Where should this topic live?

  a) Plugin repo — topics/[name].md
     Ships as a default topic with ramp. Public. Requires the full wiring
     checklist (docs-map, CLAUDE.md, CHANGELOG) and review before merge.

  b) Project-local — .claude/knowledge-graphs/schemas/[name].md
     Committed to THIS repo, for its team. Not shipped with ramp.

  c) Personal — ~/.claude/ramp/schemas/[name].md
     Yours only, on this machine. Never committed anywhere.

Which? (a/b/c)
```

Record the answer as `TARGET_DIR`. Every later phase honors it.

⚠️ **Never write to the plugin repo unless the user chose (a).** A personal or project topic
that lands in `topics/` becomes a public shipped curriculum.

⚠️ **Never modify `.claude-plugin/plugin.json`.** Version bumps are release decisions, held
until a batch is release-ready. Adding a topic is not a release.

---

## Phase 1 — Read and internalize the source

Read the full source with the appropriate tool. For long PDFs, read pages 1–20, then continue
in 20-page chunks until covered.

Extract and display:
- Title, author, edition/date, and **license** (an openly-licensed source is preferred — record it)
- High-level structure: parts, chapters, sections, with page numbers or anchors
- Key concepts per section
- Any stated learning objectives or competency statements

Display the inventory:

```
Source: [title] ([license])
Sections (N):
  1. [Section] — [key concepts]
  ...

Does this look right? Any sections to skip or prioritize?
```

Wait for confirmation before Phase 2.

---

## Phase 2 — Coverage audit

Glob and Read every schema in the **resolved schema dir** (shown above) — not just the plugin's
`topics/`. Map each source section to existing nodes across all topics.

Display:

```
| Source section | Existing nodes | Coverage | Gap |
|----------------|---------------|----------|-----|
| [Section]      | N from [topic] | none/partial/solid | [what's missing] |
```

Coverage: 0 nodes = none · 1–2 = partial · 3+ covering the criterion = solid.

Identify new schemas to create, existing schemas to extend, and whether a **composite** is
warranted (3+ distinct domains). Ask nothing here — proceed to Phase 3.

---

## Phase 3 — Scope proposal (gate — no writes before this passes)

Present the full scope, including the branch topology and the OUT-list:

```
Ready to generate.

Target: [TARGET_DIR]  (from Phase 0)

New:
  [TARGET_DIR]/[name].md   — N nodes across M branches
      ROOT [title] (n) · A [title] (n) · B [title] (n) · ...
  [if composite:]
  [TARGET_DIR]/[meta].md   — composite over [subs]

Edits:
  [TARGET_DIR]/[existing].md   +N nodes to Branch [X]

Out of scope (deliberately): [the OUT-list — what this topic excludes and where it would go]

Source of record: [title] — [url]

Continue? `yes` to generate, or describe scope adjustments.
```

**Write nothing until the user replies `yes`.** The OUT-list is required — §10 of the contract:
a map without one can't be judged for coverage.

---

## Phase 4 — Generate the schema

Write `[TARGET_DIR]/[name].md` in the canonical section order. Use `topics/git.md` as the
reference implementation — it is contract-clean and shows every section in its final form.

### Frontmatter — all six fields required

```yaml
---
topic: [name]                 # equals the filename stem
node_count: [N]               # MUST equal the number of node rows below
version: 1
source_url: [canonical source URL]
goal: ramp them up on [...]   # the role goal /ramp:up reads
description: [one sentence — rendered by /ramp:list]
---
```

`node_count` and `goal` are the two fields the old version of this command omitted. A missing
`node_count` is a lint **problem** (exit 1); a missing `goal` is an advisory. Both block delivery.

### Intro prose

Two to four sentences: what the topic covers, the source it follows, **the explicit OUT-list**,
and the node/branch count.

### `## Node definitions`

Open with `[N] nodes across [M] branches.` Then one `### [X] Title (…)` subheader per branch,
`X` from `ROOT A B C D E` in order:

- `### [ROOT] [Title] (always unlocked — [n] nodes)`
- `### [A] [Title] ([n] nodes, unlocks when ROOT ≥ [k] `[✓]`)`

Every branch table uses **exactly these six columns**:

```
| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|-----------|-----|
```

- **Node** — the skill title. Must pass the four tests in §1 of the contract: verb test,
  evidence test, atomicity test, teeth test.
- **Mastery criterion** — one or two sentences *including the teeth*: the element surface
  familiarity gets wrong. "Can explain X **and** why Y-nuance", never "understands X".
- **Type** — `/`-separated from exactly: `Artifact`, `Exercise`, `Qualitative`, `Historical`.
- **Auto-detect signal** — `None`, or `evidence → [status|type]` matching a Detection signals row.
- **source_url** — the canonical reference **for this node**. Fetch every URL before shipping
  (Phase 7 checks this); never write one from memory.
- **id** — `[topic]-[kebab-title]`. Generate with the kernel, never by hand:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/ramp_core.py" ids [name] 2>/dev/null | python3 -c "import json,sys; [print(r['title'],'->',r['suggested']) for r in json.load(sys.stdin)['rows']]"
```

Escape any literal pipe in a cell as `\|`.

### `## Probes`

```
| name | primitive | args |
```

The primitive set is **closed** — exactly these ten, and extending it is a kernel change:

`file-exists` · `file-lines` · `glob-count` · `dir-count` · `json-has-key` · `json-value` ·
`grep-count` · `git-log-grep` · `git-worktree-count` · `git-max-commit-files`

Gotchas that have each bitten before:
- Args parse with `shlex.split` — **quote any regex containing spaces or backslashes**.
- `grep-count` needs a regex **plus one or more explicit path bases**; it cannot take a glob,
  and with no path it is a dead probe the lint rejects.
- `glob-count` skips dot-directories; pair with `--exclude` where a vendor dir would inflate it.
- `—` in the args cell means "no args". A literal `|` in a regex is written `\|`.
- A missing path yields 0, not an error. Probes are **precision-biased**: prefer a signal that
  under-fires to one that false-positives.

Close with a **Notes** paragraph explaining every non-obvious threshold.

If the topic has no detectable environmental signal, omit the section — but say so explicitly in
the Phase 8 report, because it is an advisory the user is accepting knowingly.

### `## Detection signals`

```
| Collected evidence | Node → status |
```

Evidence names the probe and threshold (`git_history > 0`). The status cell is
`BRANCH: "Node title" → [status|type]` with the pipe escaped.

**The direct-witness rule (§6):** seed `[✓]` **only when the evidence witnesses the criterion's
act**. A linked worktree does not witness "has used `git worktree`" — agent tooling creates them.
Evidence merely *consistent with* the skill seeds `[~]`. Doubt → `[~]`.

**Reference grammar — two ways this silently breaks:**
- The branch label must be exactly `ROOT` or `A`–`E` followed by `:`. `Root:` or `ROOT :` is
  harvested by the loose matcher and flagged as malformed.
- A multi-fragment cell registers **only the first quoted title** unless each carries its own
  label. Write `A: "X" + A: "Y"`, never `A: "X" + "Y"`.

### `## Gap questions` + two subsections

The question table is `| Branch | Gap | Ask this |` with **one row per node, in node order**.
Branch row counts must equal that branch's node count *exactly* — anything else is an advisory
that blocks delivery. Write questions teach-back style, aimed at the criterion's teeth: pose the
scenario where the nuance bites, and ask for the *why*.

`### Qualitative rubric` — canonically:
- **`[✓]` Demonstrated**: at least one specific verifiable detail — the actual command/flag, an
  observed behavior, a tradeoff navigated, or a causal *why*.
- **`[~]` Self-reported**: affirmative but vague — no mechanism, no scenario.
- **`[ ]` Not yet**: negative, "not sure", or "heard of it".

`### Answer → node mapping` — `| Answer contains | Node → status |`, **one row per node**, same
reference grammar. One explicit `Branch: "title"` per node; matching is by substring, so a
fragment that matches two nodes in a branch is ambiguous — use enough of the title to be unique.

### `## Unlock thresholds`

One bullet per non-ROOT branch, ascending. Pick roughly N−2 of the branch's node count so a
learner unlocks the next branch before exhausting the current one. Close with the literal line:

``Both `[✓]` and `[~]` count toward unlock thresholds.``

### `## Tier definitions`

The standard four-tier table (Explorer · Builder · Practitioner · Expert), adapted to the
branch letters.

### `## Tree render template`

A fenced block, plain branch titles, `[?]` node lines, `[if locked: …]` hints.

⚠️ **No bracket tier codes** (`[ROOT]`, `[A]`) anywhere in this block — codes leaking into
user-facing output is a lint **problem**.

### `## Saved tree file template`

A fenced ```markdown block: frontmatter placeholders, the status legend, then `## [X] Branch
Title` headers — **bracket codes required here**, the kernel's header regex parses them — with
`- [STATUS|TYPE] Node title` lines, then `## Frontier` and `## Notes`.

⚠️ Node titles must match `## Node definitions` **exactly, one line per node**. The lint
enforces parity in both directions, and this is the single most common failure.

---

## Phase 5 — Extend existing schemas

For each schema with a coverage gap, use targeted Edit calls — never a rewrite:

1. Add node rows to the right branch table (all six columns, id included)
2. Update the branch's node count in its `###` header
3. Update `node_count:` in frontmatter **and** the `[N] nodes across [M] branches` line
4. Add Detection signals rows for anything probe-detectable
5. Add one Gap question row **and** one Answer-mapping row **per new node**
6. Add the new nodes to **both** templates
7. Re-check the unlock threshold if the branch grew substantially

Adding nodes is a **safe** change under §10 — do not bump the schema `version:`. Bump only on a
removal, an id change, or a branch restructure, and write the migration note when you do.

---

## Phase 6 — Composite topic (3+ distinct domains)

A composite carries **only** frontmatter, prose, and a composite saved-tree template. The map
and instrumentation live in the sub-schemas — it has no node tables, probes, or questions of its
own. Reference `topics/claude-code.md`.

```yaml
---
topic: [meta-name]
node_count: [MUST equal the sum of the sources' node_counts]
version: 1
source_url: [...]
goal: ramp them up on [...]
description: [...]
sources: [sub-a, sub-b, sub-c]
---
```

Probes and node ids are unioned across sources at runtime, **first declaration of a name wins** —
so a probe name colliding across two sub-schemas silently drops one. Keep probe names unique
across the family.

---

## Phase 7 — Make it resolvable, then validate (the gate)

### 7a — Make the schema visible to the CLI

`_schema_dir()` returns the **first** existing candidate, in this order:

1. `.claude/knowledge-graphs/schemas/` (project-local, relative to cwd)
2. `~/.claude/ramp/schemas/`
3. `$CLAUDE_PLUGIN_ROOT/topics/`

So a schema freshly written to the plugin's `topics/` is **invisible** to `lint`, `ids`, and
`detect` whenever `~/.claude/ramp/schemas/` exists — which it does on every plugin install. The
SessionStart hook symlinks new topics, but not until the *next* session.

For target (a), link it now so validation reads the file you just wrote:

```bash
ln -sfn "${CLAUDE_PLUGIN_ROOT}/topics/[name].md" "$HOME/.claude/ramp/schemas/[name].md"
```

The observer leaves manually-placed files and valid symlinks alone, so this is stable.

For targets (b) and (c) the file is already on the resolution path — but note that a
project-local schema dir **shadows the global one entirely**, hiding every personal topic while
cwd is that repo. Say so in the report if you created one.

Confirm resolution before proceeding:

```bash
python3 -c "import os,sys; sys.path.insert(0, os.environ.get('CLAUDE_PLUGIN_ROOT','.')); import ramp_core; print(ramp_core._schema_dir() / '[name].md')"
```

### 7b — Run the gate

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/ramp_core.py" lint [name]      # zero problems AND zero advisories
python3 "${CLAUDE_PLUGIN_ROOT}/ramp_core.py" ids [name]       # "problems": []
python3 "${CLAUDE_PLUGIN_ROOT}/ramp_core.py" detect [name]    # probes execute, values sane
python3 "${CLAUDE_PLUGIN_ROOT}/ramp_core.py" catalog          # topic registered, node_count correct
```

**Loop until `lint` is clean.** Read each finding, fix the schema, re-run. Do not rationalize a
finding away and do not report partial success — an unclean lint means the work is not done.

Common failures and their causes:

| Finding | Cause |
|---------|-------|
| `node_count N != M node rows` | Frontmatter not updated after adding/removing a row |
| `parity: 'X' in Node definitions but not the saved-tree template` | Title drift between the two — they must match character for character |
| `detection signal: A: "X" matches no node` | Typo, or the title was reworded in one place only |
| `malformed node reference` | Branch label not exactly `ROOT`/`A`–`E` + `:` |
| `probe 'p': grep-count needs ≥2 arg(s) — dead probe` | Regex with no path base |
| `tree render template: bracket tier codes leak` | `[ROOT]`/`[A]` left in the render block |
| `gap questions: branch A has 3 row(s) for 5 node(s)` | Not one question per node |

### 7c — The two checks the lint cannot make

- **Fetch every `source_url`** against the live source with WebFetch. A 404 in a shipped schema
  is a broken promise to the learner. Fix or remove — never leave an unverified URL.
- **Prove every grep probe against a fixture**: create a scratch directory containing a
  known-positive file, run `detect`, confirm the probe fires. A probe that can never fire is
  dead weight the lint cannot see.

Then run the suite:

```bash
python3 -m pytest tests/ -q
```

---

## Phase 8 — Wire and report

**Wiring checklist — target (a) only**, all in the same change:

- `docs/docs-map.md` — URL→node section + a row in the topics table
- `CLAUDE.md` — Structure listing line + Topics section line
- `CHANGELOG.md` — a bullet under `## [Unreleased]` → `### Added`

**Do not touch `.claude-plugin/plugin.json`.**

For targets (b) and (c), skip the checklist entirely — those schemas are not part of the
plugin's shipped surface.

Report:

```
Done.

Created:
  [path]   N nodes across M branches
  [if composite:] [path]   composite over [subs]

Edited:
  [path]   +N nodes to Branch [X]
  [wiring files, target (a) only]

Validation:
  lint     0 problems, 0 advisories
  ids      0 problems
  detect   [N] probes executed — [what fired in this environment]
  catalog  registered, node_count [N]
  pytest   [result]
  URLs     [N]/[N] fetched and verified

Source of record: [title] — [url] ([license])
Out of scope: [the OUT-list]

Start a session:  /ramp:up [name]
```

If anything was accepted below standard — no `## Probes`, an unverifiable URL — say so plainly
here. Never report a clean gate you did not get.

---

## Constraints

- **Zero problems and zero advisories, or it is not delivered.** No partial-credit reporting.
- Read `docs/topic-authoring.md` before generating; on conflict, the contract wins.
- No writes before the Phase 3 gate.
- **Never write to the plugin repo unless the user chose target (a).**
- **Never modify `plugin.json`.** Version bumps are release decisions.
- Mastery criteria must be specific and falsifiable, with teeth. Reject "understands X".
- `source_url` must be fetched, never recalled. Leave it out rather than invent it.
- Node ids come from `ramp_core.py ids`, never hand-written, and are frozen once shipped.
- Adding nodes is safe and does not bump the schema `version:`; removals and id changes do, and
  require a migration note.
- PDF reading needs `poppler-utils` — on a `pdftoppm is not installed` error, tell the user to
  run `brew install poppler` (macOS) or `apt-get install poppler-utils` (Linux).
- If a phase fails — source unreadable, lint unfixable, URLs dead — surface it and ask. Never
  paper over it.
