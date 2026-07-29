# Design notes

Why ramp is built the way it is — three decisions that shaped the architecture. Companion
to [`topic-authoring.md`](topic-authoring.md) (the schema contract) and
[`tree-format.md`](tree-format.md) (the artifact format).

## The deterministic kernel

The engine is prompts, and prompts drift. Early versions let commands compute XP and
review dates inline — three commands, three slightly different answers. The fix was a
single stdlib kernel (`ramp_core.py`) owning everything that must not drift: XP tiers,
the spaced-repetition ladder, graph validation, locking, never-downgrade. Commands
propose status and evidence; only the kernel computes. The hook and the MCP server import
it; the read-only commands shell into its CLI. One number, one place.

The failure mode this replaced was structural. XP lived in two engines — a Python
function in the observer hook and mental arithmetic in four command prompts — writing the
same frontmatter field alternately, with no reconciliation. Review dates were model
date-math: one shipped graph drifted by eight days, and an impossible date would have
passed the due-filter silently. Three uncoordinated paths wrote tree files; only one held
the file lock.

Every write now converges on one validated writer. `save_graph` validates the tree,
recomputes `xp:` in code (overwriting whatever the caller proposed), enforces
never-downgrade against the on-disk graph, fills a missing review date on a
newly-demonstrated node, and writes atomically under the shared lock. Repairs are
surfaced in the writer's response, never applied silently — a malformed date is flagged,
not rewritten, because its correct value is unknowable. `advance_review` owns the other
write path: a pass/fail outcome goes in; level and next-date come out. Callers delegate
instead of reimplementing: the observer hook imports the kernel, the MCP server exposes
the same writer as a tool, and sessions without the server pipe the tree into
`ramp_core.py save` — where a rejection is an exit code, not a shrug.

## Evidence over declaration (the event-sourced tree)

A knowledge graph you can hand-edit is a knowledge graph you can lie to. The tree moved
to an event-shaped model: nodes carry *evidence trails* (who observed what, when, how),
statuses are derived from evidence, and `[✓]` is never downgraded — new evidence appends.

A mutable status flag records a conclusion and forgets the reasons. An evidence trail
records facts: each entry names the context, the date, and the method — `artifact`,
`exercise`, `historical`, or merely `reported`. Status is then *derived*: any
demonstration outranks any claim, so a `[✓|artifact]` earned by a file you wrote cannot
be argued back down by a later hesitant answer. Never-downgrade stops being a rule the
prompts must remember and becomes a property of the data — evidence only accumulates,
appended to the trail, and the writer refuses any write that would lower an on-disk
`[✓]`. The practical payoff: "did XP move?" is no longer a prompt-discipline question.
XP is computed from the derived statuses on every write; demonstrating something always
moves the number, because there is no step to forget.

The format got here incrementally, and old files ride along: version-1 trees carried bare
statuses, so every `[✓]` is read as `[✓|historical]` — the conservative interpretation
that something happened but the method went unrecorded. Version 2 added the `| next:`
review field; version 3 computes `xp:` in code on every write. A v1 file upgrades the
next time it is written, and nothing zeroes.

## Detection lives in schemas, not code

Detection used to be ~25 hardcoded bash probes inside the engine prompt — every new topic
meant editing the engine. Probes moved into the topic schemas themselves (a declarative
`## Probes` grammar), with the kernel as the single runner. Adding a topic — detection
included — is once again just adding one file. The schema linter checks the grammar, so a
topic can't ship probes the runner can't execute.

The grammar is a table: each row wires a probe *name* to one of a small set of read-only
primitives — `file-exists`, `file-lines`, `glob-count`, `json-has-key`, `grep-count`,
`git-log-grep`, and friends — each returning a scalar. None execute arbitrary shell (a
`cmd` escape hatch exists, trust-gated to bundled schemas), and a probe that can't run —
missing file, not a git repo — degrades to its zero value rather than erroring. The
realization that made expansion cheap: a new topic needs new *declarations*, not new
primitive *types*. "Session count" is a glob over history files; a shell topic's
equivalent is the same primitive pointed at different paths.

Probes produce evidence; the schema's `## Detection signals` table gives it meaning,
mapping quantities to nodes and statuses — a CLAUDE.md above a threshold flips its node
to `[✓|artifact]`, a nonzero headless count marks that surface `[~|historical]`. The
engine applies whatever mapping the loaded schema declares; it never knows what the
topic is. And because a schema is now executable configuration, it is linted like code:
`ramp_core.py lint` checks the probe grammar along with the rest of the authoring
contract, splitting hard problems from advisories, and the same check runs in CI — so a
schema that declares a probe the runner can't execute fails before it ships.
