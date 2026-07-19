"""Schema lint — the mechanical half of docs/topic-authoring.md.

`lint_schema(topic, content, schema_dir)` reports two tiers:

- **problems** — the schema lies or breaks (count/parity mismatches, dangling
  node references, unknown/dead probes, missing engine-consumed sections,
  bracket codes leaking into the render template). New topics: zero.
- **advisories** — below the current authoring standard but degrades
  gracefully (missing ``## Probes``, missing ``goal:``, per-node coverage
  gaps, pre-node-ids legacy). New topics: zero; legacy schemas carry these
  as the quantified retrofit backlog.

The corpus tests at the bottom pin the real ``topics/`` files: the two
native-format exemplars (git, bash) must lint 0/0; every leaf schema and the
claude-code composite must be problem-free (advisories allowed on legacy).
"""
from pathlib import Path

TOPICS = Path(__file__).resolve().parent.parent / "topics"

VALID = r'''---
topic: demo
node_count: 3
version: 1
source_url: https://example.com/docs
description: Demo topic for lint tests.
goal: ramp them up on demo
---

# Demo Schema

Covers alpha and gamma. OUT: everything else (future `demo-internals`).

## Node definitions

3 nodes across 2 branches.

### [ROOT] Foundations (always unlocked — 2 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|-----------|-----|
| Alpha basics | Can explain alpha and the beta edge case | Qualitative | None | https://example.com/docs/alpha | demo-alpha-basics |
| Writing scripts | Has written a script and can explain the shebang choice | Artifact / Exercise | scripts present → `[~\|artifact]` | https://example.com/docs/scripts | demo-writing-scripts |

### [A] Advanced (1 node, unlocks when ROOT ≥ 1 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|-----------|-----|
| Gamma tuning | Can tune gamma and state the latency tradeoff | Qualitative | None | https://example.com/docs/gamma | demo-gamma-tuning |

---

## Probes

| name | primitive | args |
|------|-----------|------|
| readme | file-exists | README.md |
| scripts | grep-count | "#!" scripts bin |

---

## Detection signals

| Collected evidence | Node → status |
|--------------------|---------------|
| scripts > 0 | ROOT: "Writing scripts" → `[~\|artifact]` |

---

## Gap questions

| Branch | Gap | Ask this |
|--------|-----|----------|
| [ROOT] | Alpha | "Explain alpha — and where does beta bite?" |
| [ROOT] | Scripts | "Walk me through your last script — why that shebang?" |
| [A] | Gamma | "Tune gamma for a spiky load — what do you trade away?" |

### Qualitative rubric

- **`[✓]` Demonstrated**: specific, verifiable detail.
- **`[~]` Self-reported**: affirmative but vague.
- **`[ ]` Not yet**: negative or unsure.

### Answer → node mapping

| Answer contains | Node → status |
|-----------------|---------------|
| alpha mechanism + beta edge | ROOT: "Alpha basics" → `[✓\|reported]` |
| shebang reasoning | ROOT: "Writing scripts" → `[✓\|reported]` |
| gamma tradeoff named | A: "Gamma tuning" → `[✓\|reported]` |

---

## Unlock thresholds

- Branch A unlocks when ROOT ≥ 1 `[✓]`

Both `[✓]` and `[~]` count toward unlock thresholds.

---

## Tier definitions

| Tier | Criterion |
|------|-----------|
| Explorer | ROOT incomplete |
| Builder | ROOT complete |
| Practitioner | Branch A active |
| Expert | All branches complete |

---

## Tree render template

```
Foundations
    [?] Alpha basics
    [?] Writing scripts

Advanced   [if locked: "(unlock: complete 1 Foundations skill)"]
    [?] Gamma tuning
```

---

## Saved tree file template

```markdown
---
version: 3
topic: demo
---

# Demo Knowledge Tree

## [ROOT] Foundations
- [STATUS|TYPE] Alpha basics
- [STATUS|TYPE] Writing scripts

## [A] Advanced
- [STATUS|TYPE] Gamma tuning

## Frontier
- [frontier node name]

## Notes
```
'''


def _cut_section(text: str, start_marker: str, end_marker: str) -> str:
    """Remove text between two section headings (start inclusive, end exclusive)."""
    return text[: text.index(start_marker)] + text[text.index(end_marker):]


# --- the clean case ---------------------------------------------------------

def test_valid_schema_is_zero_zero(core):
    r = core.lint_schema("demo", VALID)
    assert r["problems"] == []
    assert r["advisories"] == []
    assert r["nodes"] == 3


# --- problems: the schema lies or breaks ------------------------------------

def test_missing_engine_section_is_problem(core):
    r = core.lint_schema("demo", _cut_section(VALID, "## Detection signals", "## Gap questions"))
    assert any("detection signals" in p.lower() for p in r["problems"])


def test_frontmatter_topic_mismatch(core):
    r = core.lint_schema("other", VALID)
    assert any("topic" in p for p in r["problems"])


def test_node_count_mismatch(core):
    r = core.lint_schema("demo", VALID.replace("node_count: 3", "node_count: 4"))
    assert any("node_count" in p for p in r["problems"])


def test_empty_criterion_is_problem(core):
    r = core.lint_schema("demo", VALID.replace(
        "Can tune gamma and state the latency tradeoff", ""))
    assert any("Gamma tuning" in p and "criterion" in p for p in r["problems"])


def test_unknown_type_token_is_problem(core):
    r = core.lint_schema("demo", VALID.replace(
        "| Can tune gamma and state the latency tradeoff | Qualitative |",
        "| Can tune gamma and state the latency tradeoff | Wizardry |"))
    assert any("Wizardry" in p for p in r["problems"])


def test_missing_id_cell_is_problem(core):
    r = core.lint_schema("demo", VALID.replace("| demo-gamma-tuning |", "| |"))
    assert any("missing id" in p for p in r["problems"])


def test_unknown_primitive_is_problem(core):
    r = core.lint_schema("demo", VALID.replace(
        "| readme | file-exists | README.md |", "| readme | shell-run | README.md |"))
    assert any("shell-run" in p for p in r["problems"])


def test_dead_grep_probe_is_problem(core):
    # grep-count with a regex but no path base always returns 0 — a dead probe
    r = core.lint_schema("demo", VALID.replace('"#!" scripts bin', '"#!"'))
    assert any("scripts" in p and "grep-count" in p for p in r["problems"])


def test_duplicate_probe_name_is_problem(core):
    r = core.lint_schema("demo", VALID.replace(
        "| scripts | grep-count |", "| readme | grep-count |"))
    assert any("duplicate" in p.lower() for p in r["problems"])


def test_dangling_answer_ref_is_problem(core):
    r = core.lint_schema("demo", VALID.replace('A: "Gamma tuning"', 'A: "Delta tuning"'))
    assert any("Delta tuning" in p for p in r["problems"])
    # ...and the node it abandoned now lacks a mapping row (advisory)
    assert any("Gamma tuning" in a for a in r["advisories"])


def test_detection_ref_wrong_branch_is_problem(core):
    r = core.lint_schema("demo", VALID.replace(
        'scripts > 0 | ROOT: "Writing scripts"', 'scripts > 0 | A: "Writing scripts"'))
    assert any("Writing scripts" in p for p in r["problems"])


# --- problems the inline review missed (2026-07-19 agent review) ------------

def test_node_count_inline_comment_is_problem(core):
    # a present-but-unparseable node_count (trailing comment) must not silently
    # disable the parity check — the `except ValueError: pass` used to swallow it
    r = core.lint_schema("demo", VALID.replace("node_count: 3", "node_count: 3  # three"))
    assert any("node_count" in p for p in r["problems"])


def test_node_count_blank_is_problem(core):
    # a present-but-blank node_count is likewise a problem, not a skip
    r = core.lint_schema("demo", VALID.replace("node_count: 3", "node_count:"))
    assert any("node_count" in p for p in r["problems"])


def test_malformed_ref_case_typo_is_problem(core):
    # a branch label with the wrong case (`Root` vs `ROOT`) escapes the strict
    # ref grammar entirely — it must be flagged, not left silently unvalidated
    r = core.lint_schema("demo", VALID.replace(
        'A: "Gamma tuning"', 'Root: "Gamma tuning"'))
    assert any("malformed" in p.lower() for p in r["problems"])


def test_malformed_ref_stray_space_is_problem(core):
    # a stray space before the colon (`ROOT :`) also escapes the strict grammar
    r = core.lint_schema("demo", VALID.replace(
        'ROOT: "Alpha basics"', 'ROOT : "Alpha basics"'))
    assert any("malformed" in p.lower() for p in r["problems"])


def test_missing_unlock_line_is_problem(core):
    r = core.lint_schema("demo", VALID.replace(
        "- Branch A unlocks when ROOT ≥ 1 `[✓]`\n", ""))
    assert any("unlock" in p.lower() and "A" in p for p in r["problems"])


def test_render_template_bracket_leak_is_problem(core):
    r = core.lint_schema("demo", VALID.replace(
        "Foundations\n    [?] Alpha basics", "[ROOT] Foundations\n    [?] Alpha basics"))
    assert any("render" in p.lower() for p in r["problems"])


def test_saved_template_missing_branch_header_is_problem(core):
    # mutate only the saved-tree template's header (the node-defs `### [A]`
    # header is a superstring — anchor on the template's following line)
    r = core.lint_schema("demo", VALID.replace(
        "## [A] Advanced\n- [STATUS|TYPE] Gamma tuning",
        "## Advanced-unlabeled\n- [STATUS|TYPE] Gamma tuning"))
    assert any("[A]" in p for p in r["problems"])


# --- advisories: below standard, degrades gracefully ------------------------

def test_missing_probes_section_is_advisory(core):
    r = core.lint_schema("demo", _cut_section(VALID, "## Probes", "## Detection signals"))
    assert any("probes" in a.lower() for a in r["advisories"])
    assert not any("probes" in p.lower() for p in r["problems"])


def test_missing_goal_is_advisory(core):
    r = core.lint_schema("demo", VALID.replace("goal: ramp them up on demo\n", ""))
    assert any("goal" in a for a in r["advisories"])


def test_gap_question_coverage_is_advisory(core):
    r = core.lint_schema("demo", VALID.replace(
        '| [ROOT] | Scripts | "Walk me through your last script — why that shebang?" |\n', ""))
    assert any("gap" in a.lower() and "ROOT" in a for a in r["advisories"])
    assert r["problems"] == []


def test_answer_ref_prefix_is_accepted(core):
    # an unambiguous prefix of the full title is legal reference grammar
    r = core.lint_schema("demo", VALID.replace('ROOT: "Alpha basics"', 'ROOT: "Alpha"'))
    assert r["problems"] == []
    assert r["advisories"] == []


# --- composites --------------------------------------------------------------

COMPOSITE = """---
topic: combo
node_count: 3
version: 1
source_url: https://example.com/docs
description: Composite demo.
goal: ramp them up on combo
sources: [demo]
---

# Combo — Meta Topic
"""


def test_composite_aggregates_sources(core, tmp_path):
    (tmp_path / "demo.md").write_text(VALID, encoding="utf-8")
    (tmp_path / "combo.md").write_text(COMPOSITE, encoding="utf-8")
    r = core.lint_schema("combo", COMPOSITE, tmp_path)
    assert r["problems"] == []
    assert r["nodes"] == 3


def test_composite_prefixes_source_problems(core, tmp_path):
    (tmp_path / "demo.md").write_text(
        VALID.replace("node_count: 3", "node_count: 9"), encoding="utf-8")
    (tmp_path / "combo.md").write_text(COMPOSITE, encoding="utf-8")
    r = core.lint_schema("combo", COMPOSITE, tmp_path)
    assert any(p.startswith("demo: ") for p in r["problems"])


def test_composite_node_count_must_equal_source_sum(core, tmp_path):
    (tmp_path / "demo.md").write_text(VALID, encoding="utf-8")
    bad = COMPOSITE.replace("node_count: 3", "node_count: 5")
    r = core.lint_schema("combo", bad, tmp_path)
    assert any("node_count" in p for p in r["problems"])


# --- the real corpus ---------------------------------------------------------

def _read(name: str) -> str:
    return (TOPICS / f"{name}.md").read_text(encoding="utf-8")


def test_exemplars_lint_clean(core):
    """git, bash, and python are the native-format exemplars: zero problems
    AND zero advisories — the bar every new topic must meet."""
    for t in ("git", "bash", "python"):
        r = core.lint_schema(t, _read(t), TOPICS)
        assert r["problems"] == [], (t, r["problems"])
        assert r["advisories"] == [], (t, r["advisories"])


def test_all_leaf_schemas_problem_free(core):
    """Legacy schemas may carry advisories (the retrofit backlog) but no
    schema in the shipped corpus may carry a problem."""
    leafs = sorted(p.stem for p in TOPICS.glob("*.md") if p.stem != "claude-code")
    assert leafs, "no leaf schemas found"
    for t in leafs:
        r = core.lint_schema(t, _read(t), TOPICS)
        assert r["problems"] == [], (t, r["problems"])


def test_claude_code_composite_problem_free(core):
    r = core.lint_schema("claude-code", _read("claude-code"), TOPICS)
    assert r["problems"] == [], r["problems"]
    assert r["nodes"] == 81
