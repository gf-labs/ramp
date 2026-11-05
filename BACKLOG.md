# ramp backlog

The open product work, curated. Tracked here until it moves to GitHub Issues; to pick one
up, see [CONTRIBUTING.md](CONTRIBUTING.md).

Each item states the problem and the proposed change; the new-topic items state source and
scope instead. Items marked **Decision needed** wait on a design call, not on effort.

## Bugs

### Gap-question answers are mapped to `[✓]`, which the engine forbids

**Problem.** Two sets of documents disagree about what a good gap-question answer earns.
Every leaf schema's *Answer → node mapping* table awards `[✓|reported]`, the authoring
contract (`docs/topic-authoring.md` §7) prescribes exactly that, each schema's qualitative
rubric has a `[✓]` outcome, and CLAUDE.md's inference priority says teaching-level answers
earn `[✓]`. Against them, `commands/up.md` states repeatedly that Phase 1 answers cap at
`[~]` and carries its own two-outcome rubric, and `commands/calibrate.md` says a claim never
becomes `[✓]` there. `up.md` also names the schema as the authoritative reference, so it
contradicts itself. The type is incoherent either way, since `reported` is the type that
pairs with `[~]`. Lint cannot catch it, because the contract prescribes it.

**Decision needed.** Which side is authoritative. The `up.md` reading keeps a gap question
distinct from teach-back verification; the other reading collapses them. The engine does
award `[✓]` for a qualitative answer at check-back, so the dispute is when, not whether.
Whichever wins, fix the contract and the schemas, or `up.md` and `calibrate.md`, together:
changing the tables alone means the next `/ramp:ingest`, which authors to the contract,
brings the contradiction back. A lint check for it belongs with lint hardening below.

### Team and local tree saves bypass the kernel writer

**Problem.** Every command-driven personal-layer save goes through `save_graph`:
validation, never-downgrade, id stamping, XP recompute. Phase 4 options `d` (team tree at
`.claude/knowledge-graphs/[topic].md`) and `e` (local tree under `local/`) are written
directly by the command instead. The writer already takes a target directory, but neither
the CLI `save` verb, which accepts only a topic, nor the MCP `save_graph`, which fixes the
graph directory, exposes it, so the commands have no kernel path to those layers.

**Fix.** Give `save` a `--layer team|local` flag (or an explicit path) on both the CLI and
the MCP tool, and point options `d` and `e` at it. The read side already merges all three
layers in Phase 2; only the write side is missing. Two details for whoever picks it up: the
team and local trees are session deltas with their own frontmatter, so the writer must know
which layer it is writing, and the backend push must decide whether those layers sync.

### Observer upgrades land without a review date until the next session start

**Problem.** `scripts/skill-observer.py` writes the personal `claude-code` graph through its
own `save_tree`, which recomputes the frontmatter and replaces the file but never fills the
`| next:` field, validates the tree, or stamps ids. A `[✓|historical]` line it writes has no
review date, which `validate_tree` reports as a problem and `/ramp:review` never sees as
due, until the SessionStart normalization fills it in.

**Fix.** Route the observer's write through `save_graph`, so every personal-layer writer
shares one path. The minimum is calling `fill_missing_review_dates` before the write.

### Kernel writers read the tree before taking the lock

**Problem.** `save_graph` and `advance_review` read the on-disk tree, then take the write
lock. An observer write that lands in between is lost: in `save_graph`,
`preserve_demonstrated` runs against the stale snapshot and the locked write puts the old
state back; in `advance_review` the interleaved write is overwritten outright.

**Fix.** Move the read inside the lock in both functions, with a test that interleaves a
write between the read and the lock.

### Backend mode never receives review outcomes

**Problem.** With `KNOWLEDGE_GRAPH_API_URL` set, the MCP `save_graph` pushes the written
tree to the backend, so `up`, `pin`, `wrap`, and teach-back upgrades all sync. The MCP
`advance_review` does not: a spaced-repetition pass or fail is written only to the local
cache. The next `read_graph` fetches the backend copy, which never saw it, and the schedule
silently reverts.

**Fix.** Give `advance_review` the same post-write push `save_graph` has, through one shared
sync helper. Only installs with a backend configured are affected.

### Schema symlinks are provisioned but never pruned

**Problem.** `provision_schema_symlinks` links every plugin topic into
`~/.claude/ramp/schemas/` on SessionStart and repairs broken links for topics that still
exist, but a link for a removed or renamed topic stays behind. The catalog skips it
silently, while `known_topics` still lists the name, so the retired topic stays resolvable
with no schema behind it.

**Fix.** Prune symlinks whose target no longer exists. Never touch a regular file or a live
link, whoever made it. Extend `tests/test_symlink_provisioning.py`, which has no prune case.

## Features

### Mastery is not binary: model graded proficiency

**Problem.** A node flips once to `[✓]`, from `[~]` or straight from `[ ]`, and never
downgrades, so one successful demonstration permanently equals mastery. Proficiency doesn't
work that way. A skill needs repeated demonstration across contexts before "mastered" is
honest, and the intermediate states (learned, applied once, applied repeatedly, can teach
it) have no representation. The spaced-repetition level is the only proxy for depth, and it
encodes schedule, not confidence.

**Decision needed.** The directions to weigh:

- a demonstration count per node, with "mastered" as a threshold rather than a status;
- explicit graded statuses;
- surfacing the SR level as the proficiency signal;
- context-tagged evidence (warm/cold, assisted/unassisted), so a regression is recordable
  without a downgrade.

The blast radius is the pedagogy core: `compute_xp` tiers, `preserve_demonstrated`, every
render, the authoring contract, and the graph format (a version 4). Design before build.

### Active mode: a proactive hook layer with an intensity dial

**Problem.** ramp is passive today. The observer upgrades nodes silently, and every other
capture waits for the user to run a command (`pin`, `wrap`, `check`).

**Proposal.** Two ideas unified: a Stop hook that runs the end-of-session harvest
automatically, and a dial that nudges learning mid-session through SessionStart,
UserPromptSubmit, and Stop. Dial positions: off · low (session start only) · medium
(periodic) · high (every session end as well). Hard rule for the new layer: opt-in, default
off, never writes the graph without consent. Design pass first.

### Drive the passive observer from schema-declared signals

**Problem.** `scripts/skill-observer.py` upgrades only the `claude-code` graph, from a
hardcoded `DETECTION_RULES` table, and its own notes say other topics would get separate
observer scripts. A new topic gets `/ramp:up` detection through its `## Probes` section but
no passive observation at all, which contradicts "adding a topic is adding one file."

**Proposal.** Let a schema declare observer signals (tool, input field, pattern → node)
beside its probes, and have the observer load every provisioned schema. It runs as a fresh
process on every tool call, so parsing every schema each time is the cost to measure first,
with an on-disk cache if it matters. Any tool a signal may name must be in the PostToolUse
matcher (see the matcher item under Maintenance), which makes the matcher a closed,
lint-checked set. The fallback is to document passive observation as a `claude-code`-only
feature; the first option is the honest one.

### A self-updating content library

**Problem.** Curricula ship inside engine releases, so a corrected mastery criterion or a
new topic waits for a plugin version.

**Proposal.** Decouple them. The plugin ships a thin default bundle (`claude-code`, perhaps
a short ramp-usage topic); every other topic is fetched on demand from a separate content
repo into `~/.claude/ramp/schemas/`, with a local cache so nothing needs the network at
lesson time. A nightly freshness job lives in the content repo: fetch each node's
`source_url`, diff against the live docs, and open a proposed schema update for review.
Never an unreviewed write. Three steps, in order: the on-demand loader, the content repo
with its validation CI, then the freshness job.

Constraints already settled:

- local-first survives;
- node ids are the schema↔graph join key, so a reworded node never orphans a learner's
  `[✓]`;
- a pinned, curated index, because fetched markdown becomes model instructions;
- validation CI on the content repo;
- personal graphs stay out; this hosts curricula only.

This supersedes the in-plugin `/ramp:sync` sketched in `docs/docs-map.md`; that file stays
the URL→node source of truth the differ reads. Authoring new topics into `topics/` today is
fine; migration is moving files plus one loader path.

### A curriculum-generator agent

**Problem.** `/ramp:ingest` is the v0: one source in, one schema out, gated on
`lint → ids → detect → catalog → pytest`. Authoring a topic by hand is still days of work,
and that is the limit on how many domains ramp can cover.

**Proposal.** An agent that authors to the contract in `docs/topic-authoring.md` and to the
shape the breadth topics share (see the shape-rules item under Maintenance), with criteria
that distinguish knowing from doing, and later lessons and worksheets. Gold references are
the shipped breadth topics (`git`, `bash`, `python`, `object-oriented-design`); the gate is
the one `ingest` already enforces, at zero problems and zero advisories. Sequenced after the
content library, since generated topics need a home that is not an engine release.

## Topics

New curricula and refreshes of existing ones. Every topic lands through the same gate:
`lint → ids → detect → catalog → pytest` at zero problems and zero advisories, every
`source_url` fetched live, every probe regex proven against a fixture.

### Author the `domain-modeling` topic

**Source.** The Domain-Driven Design Reference (Eric Evans), CC-BY.

**Scope.** The DDD material deliberately excluded from `object-oriented-design`: aggregates,
bounded contexts, ubiquitous language, entities vs value objects, repositories, domain
events. Shape follows the breadth topics: six branches of about five nodes, one source set.
Read `topics/object-oriented-design.md` for the source-set precedent and
`docs/topic-authoring.md` for the contract.

**Decision needed.** Whether this and `object-oriented-design` sit under a `software-design`
composite.

### Author the `data-structures-algorithms` topic

**Source.** Open Data Structures (Pat Morin), CC-BY.

**Scope.** Ships standalone: it is an algorithmic axis, not a design one, so it belongs
under no design composite. The shipped corpus is already teach-back dominant, so no new
demonstration format is needed; criteria of the form "can explain when a two-pointer
applies and what invariant it maintains" fit the existing engine. Same shape as
`domain-modeling`.

### Refresh `claude-code` against the current docs

**Problem.** Capabilities the docs now cover that the sub-topic schemas don't: the
SessionStart, PreCompact, SessionEnd, UserPromptSubmit, SubagentStop, and WorktreeCreate
hook events (the schemas name only PreToolUse, PostToolUse, Stop, and Notification); skills
vs slash commands; deferred tool loading; background tasks; scheduled routines; subagent
messaging. The observer's own notes also deny that WorktreeCreate exists.

**Fix.** Refresh the five sub-topic schemas through `/ramp:ingest`, which supports extending
an existing schema, and correct the observer note in the same pass.

## Maintenance

### Bring `up.md` under the 600-line limit its own hook warns about

**Problem.** `scripts/file-size-warn.py`, wired in the repo's `.claude/settings.json`, warns
at 600 lines on markdown writes, and `commands/up.md` is over it.

**Fix.** `up.md` is the engine prompt, so anything moved out must still reach the model when
it is needed, by an include or an injection. That satisfies the line count and keeps the
files focused, which is the hook's stated intent, but does not shrink the prompt; if no
section can honestly move, raising the limit for this one file is the other answer.
Candidate splits, safest first:

- the `./.ramp/` workspace section is a pure format contract that other commands already
  reference rather than duplicate; `CLAUDE.md` names `up.md` as its canonical home and
  changes with it;
- the Phase 4 artifact templates are emitted verbatim and need not sit in engine prose;
- the Mode A and Mode D blocks are self-contained.

While there, re-letter Phase 0, whose steps currently run 0a, 0b, 0e, 0c. Constraint:
`up.md` is topic-agnostic by design. No split may push curriculum concerns into it or
scatter the phase flow; a reader should still follow Phase 0 → 4 in one pass.

### Narrow the PostToolUse hook matcher

**Problem.** The plugin's PostToolUse matcher is `.*`, which starts a Python interpreter on
every tool call, although the observer's detection rules name only Bash, Write, Edit,
Glob, Grep, and Agent.

**Fix.** Match the tools the rules name, everywhere the matcher is written:
`hooks/hooks.json`, the repo's `.claude/settings.json`, and the observer's docstring. If
schema-declared signals land (see Features), the matcher becomes the closed set a signal
may name, checked by lint. It is also the idiomatic hook a plugin about Claude Code should
model.

### Delete the duplicate frontmatter parser

**Problem.** `mcp/server.py` keeps its own `_parse_frontmatter` beside the kernel's. The two
differ slightly: the kernel keeps an empty value, the server drops the key.

**Fix.** Delete it and call `ramp_core.parse_frontmatter`; check the one render where an
empty `level:` would now read differently. Single-sourcing is the reason the kernel exists.

### Record the shape rules in the authoring contract

**Problem.** The breadth topics (`git`, `bash`, `python`, `object-oriented-design`) share a
shape: about five nodes per branch, branch count as the dial, one source set per topic.
`docs/topic-authoring.md` does not state it, so a contributor authoring a topic, and the
generator agent under Features, have nothing written to author to. The older schemas
predate the rule and vary widely.

**Fix.** Add a shape section to the contract, stated as the rule for new topics. A lint
advisory for a branch outside the band is optional and belongs with lint hardening.

### Lint hardening: three new problem-class checks

**Problem.** `lint` catches dangling node refs but not ambiguous ones, while the authoring
contract demands unambiguous. Three gaps:

- a ref that matches two in-branch nodes passes silently (a loosened `ROOT: "Settings"` ref
  in `configuration` would match more than one node);
- the second fragment of a multi-ref (`A: "X" + "Y"`) is invisible to the node-ref regex,
  so it goes unchecked;
- a composite's cross-sub-topic probe-name collision is silent; first wins in the union.

**Fix.** One problem-class check per gap, each with a fixture that fails before and passes
after. A check for the `[✓|reported]` mapping contradiction above belongs here once that
decision lands.

### Assert the node counts quoted in README and CLAUDE.md

**Problem.** README and `CLAUDE.md` quote the total and per-sub-topic node counts for
`claude-code`. `scripts/check-docs.py` asserts only the topics badge against the README
table's row count, so those figures are maintained by hand and nothing fails when a schema
changes.

**Fix.** Assert them against the schemas, as the test suite already does for each schema's
own `node_count:` frontmatter.

### Drop the unused `email:` graph field

**Problem.** `up` and `calibrate` write `user:` and `email:` from git config into every
personal graph, and every schema's saved-tree template carries the field. Nothing in the
kernel, server, or hooks reads `email:`.

**Fix.** Remove it from every schema's saved-tree template under `topics/`, from the
identity scan and fallback template in `commands/up.md`, from `commands/calibrate.md`, and
from `docs/tree-format.md`. Collect nothing the product doesn't use.

### Keep `./.ramp/` out of the host repo's history

**Problem.** `./.ramp/scan.md` records the absolute project path and `calibrate.md` records
your self-placement. `up.md` describes the workspace as gitignored, but nothing adds
`.ramp/` to the host repo's `.gitignore`; the README asks users to do it themselves. A
`git add -A` in the host repo commits both.

**Fix.** Print the one-liner on first workspace write, the way option `e` already does for
the local tree, and stop calling the directory gitignored. Appending the entry automatically
would be friendlier, but the README promises that ramp never edits your ignore file; if that
is the choice, change the promise in the same change.

### Run first-run acceptance on a clean machine

**Problem.** First-run happens once per machine, so it is the path most likely to break
unnoticed, and it has not been exercised on a machine with no prior ramp state.

**Fix.** Install via `--plugin-dir` on such a machine, without the MCP server, and assert: a
new user with no or unknown topic routes to `/ramp:calibrate` rather than a full graph
dump; after a demonstration and a check-back the node flips to `[✓]` *and* `xp:`
increases; `tree` and `list` reflect the new state; a side question can be asked mid-lesson
and the lesson resumed from the bookmark the worksheet leaves (the lesson-registry flow is
deferred and not under test); nothing lands outside `~/.claude/ramp/` and `./.ramp/` unless
a team or local save was chosen. Interactive by nature; not automatable.
