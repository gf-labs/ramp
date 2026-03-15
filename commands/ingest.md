---
description: Generate knowledge-graph schemas from an external source — course curriculum, API docs, or technical specs
argument-hint: "[topic-name] [/path/to/source.pdf or https://...]"
allowed-tools: Read, Glob, Grep, Bash, Write, Edit, WebFetch
---

## Auto-collected context

**Arguments**: $ARGUMENTS

**Today's date**: !`date +%Y-%m-%d`

**Existing topic schemas**:
!`ls ~/.claude/knowledge-graphs/schemas/ 2>/dev/null || ls /Users/berniegreen/Repos/gfl/ramp/topics/*.md 2>/dev/null | xargs -I{} basename {} .md | sort || echo "none found"`

**Current plugin version**:
!`python3 -c "import json; d=json.load(open('/Users/berniegreen/Repos/gfl/ramp/.claude-plugin/plugin.json')); print(d['version'])" 2>/dev/null || echo "unknown"`

---

## Your role

You are the `/ramp:ingest` command. Your job is to generate a complete, high-quality knowledge-graph schema for a new topic by reading external source material and applying ramp's v3 schema format.

Work through the 7 phases below sequentially. **Do not write any files until Phase 3 approval.** After Phase 3, proceed autonomously through Phases 4–7.

---

## Phase 0 — Parse arguments and detect source type

Parse `$ARGUMENTS`: first word = `topic-name`, remainder = `source`.

**Argument checks:**
- If no `topic-name`: ask "What topic name should I use? (e.g., `aws-solutions-architect`)" and wait.
- If no `source`: ask "What source material should I read? Provide a file path or URL." and wait.
- If `topic-name` already appears in **Existing topic schemas** above: warn — "Topic `[name]` already exists. Extend it, or abort?" Wait for user reply. If extend: proceed with a gap-fill focus in Phase 2. If abort: stop.

**Source type detection:**
- Path ending `.pdf` → use Read tool (paginated; up to 20 pages per call — read in chunks)
- URL (`http://` or `https://`) → use WebFetch
- Path ending `.md`, `.txt`, or any local file → use Read tool

Proceed to Phase 1 once arguments are validated.

---

## Phase 1 — Read and internalize source material

Read the full source using the appropriate tool. For long PDFs, read pages 1–20, then continue in 20-page chunks until you have covered the full document.

Extract and display:
- Title of the source
- High-level structure: sections, domains, chapters — with page numbers if available
- Key concepts per section: what topics and skills each section covers
- Any explicit learning objectives, task statements, or assessment criteria

Display a brief inventory:
```
Source: [title]
Sections (N):
  1. [Section name] — [key concepts]
  2. ...

Does this look right? Any sections to skip or prioritize?
```

Wait for user confirmation before proceeding to Phase 2.

---

## Phase 2 — Coverage audit

Load all existing ramp topic schemas (Glob `topics/*.md`, Read each). Map each source section/domain to existing schema nodes. For each source section:
- Count matching nodes in existing schemas
- Compute rough coverage: 0 nodes = zero, 1–2 nodes = partial, 3+ nodes covering the criterion = solid

Display a coverage table:
```
| Source section | Existing nodes | Coverage | Gap |
|----------------|---------------|---------|-----|
| [Section 1]    | N from [schema] | XX% | [what's missing] |
```

Identify:
- New schemas to create (zero-coverage sections)
- Existing schemas to patch (partial coverage — add nodes)
- Whether a meta-topic aggregator is warranted (source has 3+ distinct domains)

Do not ask the user anything here — proceed to Phase 3.

---

## Phase 3 — Scope proposal (gate before writing)

Present the full proposed scope:
```
Ready to generate — here's what I'll create:

New files:
  topics/[name].md  (~N nodes, M branches)
  [if additional schemas:]
  topics/[name2].md  (~N nodes)

Edits to existing files:
  topics/[existing].md  (+N nodes to [Branch])

[if meta-topic:]
  topics/[topic-name]-meta.md  (aggregator)

Source registry:
  docs/[topic-name]-sources.md

Total: ~N new nodes across M schemas

Continue? Reply `yes` to generate, or describe any scope adjustments.
```

**Do not write any files until the user replies `yes` (or approves with adjustments).**

---

## Phase 4 — Generate new topic schemas

For each new schema, write `topics/[name].md` following the v3 schema format exactly. Reference `topics/build.md` as the canonical multi-branch example and `topics/mcp-development.md` as a second reference.

**Required sections in every schema file:**

```markdown
---
topic: [name]
version: 1
source_url: [primary URL for this topic's official docs, or "*(see docs/[name]-sources.md)*"]
description: [one-sentence description of what this schema covers]
---

# [Topic Name] Knowledge Graph Schema

[1-2 sentence intro — what the schema covers, how many nodes, primary use case]

---

## Node definitions

[N] nodes across [M] branches.

### [ROOT] [Branch Name] (always unlocked — [N] nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|-----------|
| [Node name] | [Specific, testable behavior] | [Qualitative / Artifact / Exercise / Historical] | [signal → `[status]`] or None | [URL] |

### [A] [Branch Name] ([N] nodes, unlocks when ROOT ≥ [N] `[✓]`)

[... repeat for each branch ...]

---

## Detection signals

| Collected evidence | Node → status |
|--------------------|---------------|
| [signal] | [branch: "Node name"] → `[✓|artifact]` |

---

## Gap questions

| Branch | Gap | Ask this |
|--------|-----|----------|
| [ROOT] | [what's missing] | "[Feynman-framed question]" |

### Qualitative rubric

- **`[✓]` Demonstrated**: [what detail distinguishes demonstrated from claimed]
- **`[~]` Self-reported**: [what a vague answer looks like]
- **`[ ]` Not yet**: Negative or no exposure.

### Answer → node mapping

| Answer contains | Node → status |
|-----------------|---------------|
| [specific detail] | [branch: "Node"] → `[✓|reported]` |

---

## Unlock thresholds

- Branch A unlocks when ROOT ≥ [N] `[✓]`
- Branch B unlocks when Branch A ≥ [N] `[✓]`
[... etc ...]

Both `[✓]` and `[~]` count toward unlock thresholds.

---

## Tier definitions

| Tier | Criterion |
|------|-----------|
| Explorer | ROOT incomplete |
| Builder | Branch A in progress |
| Practitioner | Branch B+ active |
| Expert | All branches demonstrated |

---

## Tree render template

\`\`\`
[ROOT] [Branch Name]
    [?] [Node name]
    ...

[A] [Branch Name]   [if locked: "(unlock: complete N [Branch] skills)"]
    [?] [Node name]
    ...
\`\`\`

---

## Saved tree file template

\`\`\`markdown
---
version: 3
topic: [name]
user: [git config user.name or "unknown"]
email: [git config user.email or "unknown"]
updated: [today's date YYYY-MM-DD]
level: [Explorer / Builder / Practitioner / Expert]
xp: [CURRENT_XP]
---

# [Topic Name] Knowledge Graph

*[✓] Demonstrated · [~] Self-reported · [ ] Not yet · [★] Mastery target · [·] Locked*

## [ROOT] [Branch Name]
- [STATUS|TYPE] [Node name]
...

## Frontier
- [frontier node name] — [criterion one-liner]

## Notes
<!-- Add personal notes here -->
\`\`\`
```

**Node design rules:**
- ROOT: always unlocked; 4–6 nodes covering fundamentals that apply to all learners
- Branches A–E: progressively advanced; each branch unlocks the next
- Mastery criterion: one specific testable behavior per node — not "understands X" but "can describe the difference between X and Y" or "has done Z"
- Type: Qualitative (judgment call), Exercise (do it live), Artifact (file exists), Historical (past evidence)
- source_url: closest official doc URL for this specific node's concept; leave blank if empirically-verified

---

## Phase 5 — Patch existing schemas

For each existing schema with coverage gaps, use the Edit tool to:
1. Add new node rows to the appropriate branch table (preserve table formatting exactly)
2. Update the branch node count in its section header (e.g., `5 nodes` → `7 nodes`)
3. Update the file-level node count in `## Node definitions` (e.g., `20 nodes across 5 branches`)
4. Add new rows to the Detection signals table for any artifact-detectable new nodes
5. Add new Gap questions for the new nodes
6. Add the new nodes to the Tree render template and Saved tree file template sections

Do not rewrite the entire file — use targeted Edit calls for each section.

---

## Phase 6 — Meta-topic (if 3+ distinct domains)

If the source has 3 or more distinct domains, create `topics/[topic-name].md` as an aggregator meta-topic. Reference `topics/claude-code.md` as the canonical meta-topic template (it sources several sub-topics). The meta-topic must include:

- Domains table with weights (if the source specifies them) and sub-topic schema mappings
- Course/prerequisite section (if applicable)
- Course-to-node pre-population mapping (which nodes to mark `[~|reported]` per completed course)
- Session structure for `/ramp:up [topic-name]`: Phase 0 (source detection) through Phase 4 (node upgrade and save)
- Scenario exercise templates (one per major domain) in a scenario-based format
- Saved tree format showing cross-topic aggregation

---

## Phase 7 — Finalize

**Source registry** — write `docs/[topic-name]-sources.md`:
```markdown
# [Topic Name] — Source Registry

## Primary source
- **Title**: [source title]
- **Path / URL**: [path or URL]
- **Type**: [PDF / webpage / file]
- **Read**: [today's date]

## Section map

| Section | Nodes created | Coverage |
|---------|--------------|---------|
| [Section] | [schema.md: N nodes] | [%] |

## Official doc URLs per domain

| Domain | URL |
|--------|-----|
| [Domain] | [URL] |

## Audit notes
- [Any caveats, skipped sections, ambiguous mappings]
```

**CLAUDE.md updates** — edit the Structure section to add:
- New `topics/[name].md` file(s) with node count and description
- `commands/ingest.md` if not already listed (this command itself)
- New `docs/[topic-name]-sources.md` entry

**Plugin version bump** — increment the patch version in `.claude-plugin/plugin.json`:
```json
"version": "[current-version + 0.0.1]"
```

**Display summary:**
```
Done.

Created:
  topics/[name].md  (N nodes, M branches)
  [...]
  docs/[topic-name]-sources.md

Edited:
  topics/[existing].md  (+N nodes)
  CLAUDE.md  (structure section)
  .claude-plugin/plugin.json  ([old] → [new])

Total: N new nodes. Topic coverage: ~X%

Run `/ramp:up [topic-name]` to start a learning session with this schema.
```

---

## Constraints

- Never write topic files or patch existing schemas before Phase 3 user approval
- Follow the v3 schema format exactly — use `topics/build.md` as the reference if uncertain
- One schema per distinct domain — do not conflate unrelated topics into a single file
- Mastery criteria must be specific and falsifiable — reject criteria like "understands X" or "is familiar with Y"
- source_url must be a real URL to official docs — leave empty rather than invent one
- If the source is a PDF and too long to read in one call: read in 20-page chunks; synthesize before proceeding
- **PDF prerequisite:** PDF reading requires `poppler-utils` — if the Read tool returns a `pdftoppm is not installed` error, tell the user to run `brew install poppler` (macOS) or `apt-get install poppler-utils` (Linux) before retrying
- If any phase fails (source unreadable, schema format error): surface the problem and ask the user how to proceed
