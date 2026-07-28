# Topic authoring standard

The normative contract for `topics/*.md` schemas. A topic ships as **one file**;
the engine never changes. This document is what any producer — a human author, a
future generator agent, a community contributor — must satisfy, and
`python3 ramp_core.py lint <topic>` checks the mechanical half of it.
Companion doc: `docs/tree-format.md` (the *graph file* a schema generates);
per-node doc links live in `docs/docs-map.md`.

Terminology: a schema is a **capability map plus its instrumentation**. The map
is the node set; the instrumentation is how the engine measures a person
against it (probes, detection signals, gap questions, rubric). Curricula are
not authored artifacts — the engine derives the learning path at runtime from
map × user state × `goal:`.

---

## 1. What a skill is

> **A skill is the smallest durable capability a practitioner can
> independently demonstrate, verifiable against an explicit criterion.**

Every word is load-bearing:

- **smallest** — atomic units, so evidence maps cleanly and the frontier is precise.
- **durable** — a standing capability of the *person*, persisting across
  projects (why graphs are personal-global) and decaying without use (why SR exists).
- **independently demonstrate** — an observable act exists: produce an
  artifact, perform an exercise, teach it back, or show historical evidence.
- **explicit criterion** — a third party (or Claude applying the rubric) can
  grade it pass/fail. The criterion's *teeth* are the nuance that separates
  "used it" from "understands it".

**Four tests every candidate node must pass** (the first is wording, the rest
are judgment — the lint cannot check these; the author must):

1. **Verb test** — statable as "can *\<demonstration verb\>* …" (write, predict,
   diagnose, choose, explain-why). "Knows about X" fails.
2. **Evidence test** — you can name the concrete evidence that would flip it to
   `[✓]`. Can't name it → it's a topic label, not a skill.
3. **Atomicity test** — demonstrable without fully demonstrating a sibling.
   Always co-demonstrated → merge. Two separately-held demonstrations bundled → split.
4. **Teeth test** — the criterion contains at least one element that surface
   familiarity gets wrong. Without teeth, `[~]→[✓]` verification collapses
   into self-report.

Boundaries (none of these are nodes):

| Not a skill | What it is | Where it lives |
|-------------|-----------|----------------|
| A fact ("dicts are insertion-ordered ≥3.7") | knowledge atom | inside a criterion, as teeth |
| A topic label ("Dictionaries") | a container | becomes a skill once a verb + criterion attach |
| A demonstration | one evidence event | the graph's evidence trail |
| A tier/level | computed aggregate | never authored |

---

## 2. Anatomy of a topic schema

One `topics/<name>.md` per topic. Section order below is the canonical order.

| Section | Required | Consumed by |
|---------|----------|-------------|
| YAML frontmatter | always | catalog, detect, up |
| intro prose (scope + source + OUT-list) | always | human readers |
| `## Node definitions` | leaf topics | ids, lint, up (assessment + missions) |
| `## Probes` | new topics (legacy gap tracked) | `detect <topic>` |
| `## Detection signals` | leaf topics | up Phase 2, calibrate scan rows |
| `## Gap questions` + `### Qualitative rubric` + `### Answer → node mapping` | leaf topics | up Phase 2/3, calibrate, check |
| `## Unlock thresholds` | leaf topics | up tree locking |
| `## Tier definitions` | leaf topics | tier label |
| `## Tree render template` | leaf topics | up display (plain titles) |
| `## Saved tree file template` | leaf topics | graph generation (kernel-parsed) |

**Composite topics** (frontmatter `sources:` lists sub-topics) carry only
frontmatter, prose, and a composite saved-tree template; the map and
instrumentation live in the sub-schemas. Probes and node ids are unioned
across `sources:` at runtime (first declaration of a name wins).

---

## 3. Frontmatter

| Field | Required | Contract |
|-------|----------|----------|
| `topic:` | yes | equals the filename stem |
| `node_count:` | yes | integer; **must equal** the number of node rows in `## Node definitions` |
| `version:` | yes | integer; bump on breaking change (see §10) |
| `source_url:` | yes | the canonical source the topic is grounded in |
| `description:` | yes | one sentence; rendered by `/ramp:list` |
| `goal:` | new topics | the role goal `/ramp:up` reads; write it as "ramp them up on …" |
| `sources:` | composites only | `[sub-a, sub-b, …]` — marks the topic composite |

---

## 4. Node definitions — the map

Nodes are grouped by branch under `### [X] Title (…)` subheaders, `X` one of
`ROOT A B C D E` in order. ROOT is always unlocked; each later branch carries
an unlock threshold (§8). Branch assignment encodes the domain's difficulty
topology — coarse prerequisites — not a syllabus.

Every branch table uses exactly these columns:

```
| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
```

Per-column contract:

- **Node** — the skill title. Short, specific, stable-ish (rewording is safe:
  ids are the join key, but gratuitous renames churn diffs).
- **Mastery criterion** — one or two sentences of what demonstrating it looks
  like, **including the teeth** (§1 test 4). Write "Can explain/has done X …
  *and* Y-nuance", not "understands X".
- **Type** — demonstration route(s), `/`-separated, from exactly:
  `Artifact`, `Exercise`, `Qualitative`, `Historical`.
- **Auto-detect signal** — `None`, or `evidence → [status|type]` prose matching
  a `## Detection signals` row (§6).
- **source_url** — the canonical reference for this node. **Verify every URL
  against the live source before shipping** (fetch it; don't trust memory).
  Empirically-sourced topics (e.g. `claude-code-internals`) may cite
  session/date instead.
- **id** — the frozen node id: `suggest_node_id(topic, title)` =
  `<topic>-<kebab(title)>`. Paste the suggestion, then **never change it** — a
  reworded title keeps its id (that is the point). On graph lines the kernel
  stamps `| id: <slug>` as the **final field**; nothing may follow it.

Table cells containing a literal pipe must escape it as `\|`.

---

## 5. Probes — read-only environment detection

Probes are declared, not scripted: a `## Probes` table wires probe **names** to
one of ten shell-free, read-only kernel primitives. The set is **closed** —
extending it is a kernel change (code + tests + review), never a schema-side
addition. A probe can never write, never shells out, and degrades to its zero
value on any error.

```
| name | primitive | args |
```

| Primitive | Args | Returns | Notes |
|-----------|------|---------|-------|
| `file-exists` | `<path>` | bool | `~` expanded |
| `file-lines` | `<path>` | int | 0 if missing |
| `glob-count` | `<pattern> [--exclude <pattern>]` | int | recursive — `**` works |
| `dir-count` | `<path>` | int | immediate subdirs |
| `json-has-key` | `<path> <dotted.key>` | bool | |
| `json-value` | `<path> <dotted.key>` | value | `none` if absent |
| `grep-count` | `<regex> <path> [path …]` | int | see gotchas below |
| `git-log-grep` | `<regex> [--diff-filter=X] [--path=Y]` | int | commits whose message matches (`--all -E`) |
| `git-worktree-count` | `—` | int | always ≥ 1 (main worktree listed) — threshold at `> 1` |
| `git-max-commit-files` | `[N]` | int | max files touched in one of the last N (default 10) commits |

Args gotchas (each has bitten):

- Args are parsed with `shlex.split`. **Quote any regex containing spaces or
  backslashes** — unquoted, shlex eats `\` (`\(\)` becomes `()`).
- `grep-count` takes a regex plus **one or more explicit path bases** (files,
  or directories walked recursively). It **cannot take a glob**, and with no
  path it is a dead probe (always 0) — the lint rejects it.
- A missing path yields 0, not an error — probes are precision-biased: prefer
  a signal that under-fires to one that false-positives.
- An em-dash `—` in the args cell means "no args". A literal `|` in a regex is
  written `\|` (markdown escape; the parser restores it).

After the table, add a **Notes** paragraph documenting any non-obvious
threshold (e.g. why a signal fires at `> 1` rather than `> 0`).

---

## 6. Detection signals — evidence → seed status

Maps collected probe evidence to node seeds:

```
| Collected evidence | Node → status |
```

- **Collected evidence** — prose naming the probe and threshold (`git_history > 0`).
- **Node → status** — `BRANCH: "Node title" → [status|type]`, e.g.
  `A: "Basic branch-and-merge workflow" → [~|historical]` (pipe escaped as
  `\|` in the cell). The quoted title may be the full node title or an
  unambiguous fragment of it; prefer the full title. A title that itself
  contains double quotes (`Positional parameters and "$@" vs "$*"`) cannot be
  quoted whole — reference it by an unambiguous quote-free fragment
  (`B: "Positional parameters"`). The branch letter and title must resolve to
  a real node — the lint rejects dangling references.

**Seed-status rule (the direct-witness rule):** a probe may seed
`[✓|historical]` / `[✓|artifact]` **only when the evidence directly witnesses
the criterion's act** (git history existing witnesses "has created/cloned a
repository"). Ask *whose* act the evidence witnesses: a linked worktree does
**not** witness "has used `git worktree`" — agent tooling (Claude Code's
worktree isolation) creates linked worktrees without the user ever running
the command. Evidence that is merely *consistent with* the skill — a
`.gitignore` exists, shell scripts are present — seeds `[~|artifact]`, to be
verified by teach-back. Doubt → seed `[~]`. The criterion's teeth are then
what `/ramp:review` tests.

---

## 7. Gap questions, rubric, answer mapping

Three parts, in one `## Gap questions` section:

**The question table** — `| Branch | Gap | Ask this |`, **one row per node**,
in node order. `Gap` is a short label (may abbreviate the node title). Write
questions teach-back style, targeted at the criterion's teeth: pose the
scenario where the nuance bites ("You've edited three files but want to commit
only one …"), and ask for the *why*, not the definition.

**`### Qualitative rubric`** — the grading contract, canonically:

- **`[✓]` Demonstrated**: at least one specific, verifiable detail — the actual
  command/flag, an observed behavior, a tradeoff navigated, or a causal *why*.
- **`[~]` Self-reported**: affirmative but vague — no mechanism, no scenario.
- **`[ ]` Not yet**: negative, "not sure", or "heard of it".

**`### Answer → node mapping`** — `| Answer contains | Node → status |`, **one
row per node**, mapping a teaching-level answer to
`BRANCH: "Node title" → [✓|reported]`. Same reference grammar as §6: full
title preferred, unambiguous prefix accepted, dangling references rejected.

---

## 8. Unlock thresholds and tier definitions

`## Unlock thresholds` — one bullet per non-ROOT branch, ascending:

```
- Branch A unlocks when ROOT ≥ 3 `[✓]`
- Branch B unlocks when Branch A ≥ 3 `[✓]`
```

Close the section with: `Both `[✓]` and `[~]` count toward unlock thresholds.`
Pick thresholds so a learner unlocks the next branch before exhausting the
current one (typically N−2 of the branch's node count).

`## Tier definitions` — the standard four-tier table, adapted to branch letters:

| Tier | Criterion |
|------|-----------|
| Explorer | ROOT incomplete |
| Builder | ROOT complete, early branches in progress |
| Practitioner | mid branches active |
| Expert | all branches complete |

---

## 9. Templates

**`## Tree render template`** — the fenced block `/ramp:up` renders from:
plain branch titles with `[?]` node lines and `[if locked: …]` hints. It must
contain **no bracket tier codes** (`[ROOT]`, `[A]` …) — codes are hidden from
user-facing output (the terminology sweep).

**`## Saved tree file template`** — the fenced markdown block graphs are
generated from: frontmatter placeholders, the status legend, then
`## [X] Branch Title` headers (bracket codes **required** — the kernel's
header regex parses them) with `- [STATUS|TYPE] Node title` lines, then
`## Frontier` and `## Notes`. Node titles here must match `## Node definitions`
**exactly, one line per node** — the lint enforces parity in both directions.

---

## 10. Scope and evolution

**Scope is declared, not implied.** The intro prose states what the topic
covers, the source it follows, and the explicit **OUT-list** — what is
deliberately excluded and where it would go (a future sibling topic, a later
branch). A map without an OUT-list can't be judged for coverage.

**Evolution is additive.** The map may grow; demonstrated state must survive:

- **Safe (same `version:`)**: add nodes or branches (update `node_count:`,
  both templates, questions, mappings); reword a title or criterion (id
  frozen — `preserve_demonstrated` matches on it); tighten questions/probes.
- **Breaking (bump `version:`, migration note required)**: remove a node,
  change an existing node's `id`, restructure branches such that saved-graph
  section headers no longer correspond.
- Never reuse a retired id for a different capability.

---

## 11. Validation gate — definition of done

Run from the repo root with the plugin root pinned (otherwise the CLI may
resolve a different schema dir):

```bash
export CLAUDE_PLUGIN_ROOT="$(pwd)"
python3 ramp_core.py lint <topic>      # zero problems AND zero advisories
python3 ramp_core.py ids <topic>       # problems: []
python3 ramp_core.py detect <topic>    # probes execute (values sane in a known env)
python3 ramp_core.py catalog           # topic registered with correct node_count
python3 -m pytest tests/ -q            # suite green
```

Plus the two non-mechanical checks:

- **Every `source_url` fetched against the live source** — no from-memory URLs.
- **Probe regexes proven against a fixture** — a scratch directory containing a
  known-positive file for each grep probe.

Wiring checklist for a new topic (same commit):

- `docs/docs-map.md` — URL→node section + a row in the topics table
- `CLAUDE.md` — Structure listing line + Topics section line
- `CHANGELOG.md` — bullet under `## [Unreleased]` → `### Added`

---

## 12. Lint tiers and legacy schemas

`lint <topic>` reports two lists:

- **problems** — the schema lies or breaks: count/parity mismatches, dangling
  node references, unknown or dead probes, missing engine-consumed sections,
  bracket codes leaking into the render template. Exit 1. New topics: zero.
- **advisories** — below current standard but degrades gracefully: missing
  `## Probes`, missing `goal:`, per-node question/mapping coverage gaps.
  Exit 0. New topics: zero. Legacy schemas (the pre-standard claude-code
  sub-schemas and older standalones) carry advisories as the quantified
  retrofit backlog — burn it down opportunistically, never silently.

A composite topic is linted as: own frontmatter, then every `sources:`
sub-schema in full, problems prefixed with the sub-schema name.
