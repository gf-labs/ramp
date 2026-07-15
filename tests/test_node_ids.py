"""node-ids slice — frozen kernel-owned identity per curriculum node."""
import json
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import ramp_core  # noqa: E402

CORE = str(Path(__file__).resolve().parent.parent / "ramp_core.py")


# --- Task 1: readers ignore a trailing | id: ---

def test_node_id_extracts_and_absent():
    assert ramp_core.node_id("- [ ] Foo | id: getting-started-foo") == "getting-started-foo"
    assert ramp_core.node_id("- [✓|exercise] Foo — ev | next: 2026-01-01 [L1] | id: gs-foo") == "gs-foo"
    assert ramp_core.node_id("- [ ] Foo") is None


def test_node_name_stops_before_trailing_id():
    # the corruption this slice fixes: a bare node folds the id into the name today
    assert ramp_core.node_name("- [ ] Foo | id: gs-foo") == "Foo"
    assert ramp_core.node_name("- [~|reported] Core surface | id: gs-core") == "Core surface"
    # nodes that already stop at — / | next: are unchanged
    assert ramp_core.node_name("- [✓|exercise] Foo — ev | next: 2026-01-01 [L1] | id: gs-foo") == "Foo"
    assert ramp_core.node_name("- [ ] Foo — note | id: gs-foo") == "Foo"


def test_node_evidence_strips_trailing_id():
    # a [~]/[ ] node with a trail but no | next: leaks the id into evidence today
    assert ramp_core._node_evidence("- [~|reported] Foo — reported: vague | id: gs-foo") == "reported: vague"
    assert ramp_core._node_evidence("- [ ] Foo — note here | id: gs-foo") == "note here"
    # a [✓] node (cut at | next:) is unchanged, and a bare node is still None
    assert ramp_core._node_evidence("- [✓|exercise] Foo — ev | next: 2026-01-01 [L1] | id: gs-foo") == "ev"
    assert ramp_core._node_evidence("- [ ] Foo | id: gs-foo") is None


# --- Task 2: set_review_field keeps a trailing id final ---

def test_set_review_field_keeps_id_final_with_prior_next():
    line = "- [✓|exercise] Foo — ev | next: 2026-01-01 [L1] | id: gs-foo"
    out = ramp_core.set_review_field(line, "2026-06-25", 2)
    assert out == "- [✓|exercise] Foo — ev | next: 2026-06-25 [L2] | id: gs-foo"


def test_set_review_field_keeps_id_final_without_prior_next():
    # the fill_missing_review_dates path: no | next: yet, id already stamped
    line = "- [✓|exercise] Foo — ev | id: gs-foo"
    out = ramp_core.set_review_field(line, "2026-08-01", 1)
    assert out == "- [✓|exercise] Foo — ev | next: 2026-08-01 [L1] | id: gs-foo"


def test_set_review_field_permanent_keeps_id():
    line = "- [✓|exercise] Foo — ev | next: 2026-01-01 [L1] | id: gs-foo"
    out = ramp_core.set_review_field(line, None, 6)
    assert out == "- [✓|exercise] Foo — ev | next: permanent [L6] | id: gs-foo"


def test_set_review_field_without_id_unchanged_behavior():
    # regression: a line with no id behaves exactly as before
    line = "- [✓|exercise] Foo — ev | next: 2026-01-01 [L1]"
    assert ramp_core.set_review_field(line, "2026-06-25", 2).endswith("| next: 2026-06-25 [L2]")


# --- Hardening: `| id:` is the final field, so a literal "| id:" appearing
#     inside evidence text must not be read as the node's id (regex anchored to
#     end-of-line). Plausible here since the curriculum teaches the id syntax. ---

def test_node_id_ignores_id_literal_in_evidence():
    line = "- [✓|exercise] Node ids — ramp: used the | id: field syntax | next: 2026-07-01 [L1] | id: build-node-ids"
    assert ramp_core.node_id(line) == "build-node-ids"


def test_set_review_field_survives_id_literal_in_evidence():
    # the confirmed corruption: the greedy first-match peeled evidence + real id,
    # writing a garbage id to disk on the next schedule advance
    line = "- [✓|exercise] Node ids — ramp: used the | id: field syntax | next: 2026-07-01 [L1] | id: build-node-ids"
    out = ramp_core.set_review_field(line, "2026-09-01", 2)
    assert out == "- [✓|exercise] Node ids — ramp: used the | id: field syntax | next: 2026-09-01 [L2] | id: build-node-ids"


# --- Task 3: parse_node_ids + load_topic_node_ids ---

_NODEDEFS = """---
topic: demo
---

## Node definitions

### [ROOT] Branch one

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|--------------------|-----------|-----|
| Alpha node | crit | Qualitative | some \\| piped signal | http://x | demo-alpha-node |
| Beta node | crit | Qualitative | None | http://x | demo-beta-node |

## Saved tree file template

```markdown
## [ROOT] Branch one
- [STATUS|TYPE] Alpha node
- [STATUS|TYPE] Beta node
```
"""


def test_parse_node_ids_reads_id_column_by_header_position():
    ids = ramp_core.parse_node_ids(_NODEDEFS)
    assert ids == {"Alpha node": "demo-alpha-node", "Beta node": "demo-beta-node"}


def test_parse_node_ids_missing_column_is_empty():
    no_id = _NODEDEFS.replace(" source_url | id |", " source_url |").replace(
        " http://x | demo-alpha-node |", " http://x |").replace(
        " http://x | demo-beta-node |", " http://x |")
    assert ramp_core.parse_node_ids(no_id) == {}


def test_parse_node_ids_scoped_to_node_definitions():
    # the saved-tree template's bullet lines are not node-definition rows
    ids = ramp_core.parse_node_ids(_NODEDEFS)
    assert "- [STATUS" not in "".join(ids.keys())
    assert len(ids) == 2


def _write_schema(d, name, frontmatter, rows):
    body = "---\n" + frontmatter + "---\n\n## Node definitions\n\n"
    body += "| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |\n"
    body += "|--|--|--|--|--|--|\n"
    for title, nid in rows:
        body += f"| {title} | c | Q | None | u | {nid} |\n"
    (d / (name + ".md")).write_text(body)


def test_load_topic_node_ids_unions_sources_first_wins(tmp_path):
    d = tmp_path / "schemas"
    d.mkdir()
    (d / "combo.md").write_text(
        "---\ntopic: combo\nsources: [subA, subB]\n---\n\n## Node definitions\n"
    )  # composite: no rows of its own
    _write_schema(d, "subA", "topic: subA\n", [("Shared", "subA-shared"), ("OnlyA", "subA-only-a")])
    _write_schema(d, "subB", "topic: subB\n", [("Shared", "subB-shared"), ("OnlyB", "subB-only-b")])
    ids = ramp_core.load_topic_node_ids("combo", d)
    assert ids["OnlyA"] == "subA-only-a"
    assert ids["OnlyB"] == "subB-only-b"
    assert ids["Shared"] == "subA-shared"  # first declaration (subA) wins


# --- Task 4: stamp_ids ---

def test_stamp_ids_fills_absent_as_final_field():
    tree = (
        "## [Build · ROOT] x\n"
        "- [ ] Alpha\n"
        "- [✓|exercise] Beta — ev | next: 2026-01-01 [L1]\n"
    )
    out = ramp_core.stamp_ids(tree, {"Alpha": "b-alpha", "Beta": "b-beta"})
    assert "- [ ] Alpha | id: b-alpha" in out
    assert "- [✓|exercise] Beta — ev | next: 2026-01-01 [L1] | id: b-beta" in out


def test_stamp_ids_leaves_existing_and_no_match_and_is_idempotent():
    tree = (
        "## [Build · ROOT] x\n"
        "- [ ] Alpha | id: frozen-alpha\n"   # already id'd: frozen
        "- [ ] Unknown\n"                     # not in the map: untouched
    )
    mapping = {"Alpha": "b-alpha", "Beta": "b-beta"}
    once = ramp_core.stamp_ids(tree, mapping)
    assert "- [ ] Alpha | id: frozen-alpha" in once   # not re-derived
    assert "- [ ] Unknown\n" in once                  # no id appended
    assert ramp_core.stamp_ids(once, mapping) == once  # idempotent


def test_stamp_ids_result_round_trips_through_node_name():
    out = ramp_core.stamp_ids("## [Build · ROOT] x\n- [ ] Alpha node\n", {"Alpha node": "b-alpha-node"})
    line = [ln for ln in out.splitlines() if ln.startswith("- [")][0]
    assert ramp_core.node_name(line) == "Alpha node"   # Task 1 keeps the name clean
    assert ramp_core.node_id(line) == "b-alpha-node"


# --- Task 5: preserve_demonstrated by id (name fallback) ---

def test_preserve_reword_survives_via_id():
    # earned on disk with an id; the schema reworded the title (same id) on incoming
    existing = "## [Build · A] x\n- [✓|exercise] Old title — r, 2026-06-01: proof | next: 2026-07-01 [L3] | id: b-node\n"
    incoming = "## [Build · A] x\n- [ ] New title | id: b-node\n"
    out, preserved = ramp_core.preserve_demonstrated(existing, incoming)
    assert "[✓|exercise] Old title" in out          # earned line restored despite title change
    assert "2026-07-01 [L3]" in out
    assert preserved == ["Old title"]


def test_preserve_name_fallback_for_idless_nodes():
    # regression: nodes with no id still match by name (custom/frontier/historical)
    existing = "## [Build · A] x\n- [✓|exercise] Kept — r, 2026-06-01: proof | next: 2026-07-01 [L3]\n"
    incoming = "## [Build · A] x\n- [ ] Kept\n"
    out, preserved = ramp_core.preserve_demonstrated(existing, incoming)
    assert "[✓|exercise] Kept" in out
    assert preserved == ["Kept"]


def test_preserve_id_beats_a_stale_name_collision():
    # incoming's new title happens to collide with a *different* earned node's name;
    # id-match must win so the right node is preserved
    existing = (
        "## [Build · A] x\n"
        "- [✓|exercise] Target — r, d: p | next: 2026-07-01 [L2] | id: b-target\n"
        "- [✓|exercise] Decoy — r, d: p | next: 2026-07-01 [L2] | id: b-decoy\n"
    )
    incoming = "## [Build · A] x\n- [ ] Decoy | id: b-target\n"  # title says Decoy, id says target
    out, preserved = ramp_core.preserve_demonstrated(existing, incoming)
    assert preserved == ["Target"]                  # id wins over the name collision


# --- Task 6: save_graph wiring + graph_nodes id + validate dup-id ---

def _schema_with_ids(schema_dir, topic, rows):
    body = f"---\ntopic: {topic}\n---\n\n## Node definitions\n\n"
    body += "| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |\n"
    body += "|--|--|--|--|--|--|\n"
    for title, nid in rows:
        body += f"| {title} | c | Q | None | u | {nid} |\n"
    (schema_dir / (topic + ".md")).write_text(body)


def test_save_graph_end_to_end_reword_preserves_status(monkeypatch, tmp_path):
    monkeypatch.setenv("HOME", str(tmp_path))
    schemas = tmp_path / "schemas"
    schemas.mkdir()
    graphs = tmp_path / ".claude" / "ramp" / "graphs"
    graphs.mkdir(parents=True)
    # on disk: earned, id-native (as archive-and-fresh guarantees)
    (graphs / "demo.md").write_text(
        "---\nversion: 3\ntopic: demo\nlevel: Explorer\nxp: 10\nupdated: 2026-07-01\n---\n"
        "## [Build · ROOT] x\n- [✓|exercise] Old title — r, 2026-07-01: proof | next: 2026-07-03 [L1] | id: demo-node\n"
    )
    # schema reworded the title (same id); incoming regenerates the new title, no id
    _schema_with_ids(schemas, "demo", [("New title", "demo-node")])
    ramp_core.save_graph(
        "demo",
        "---\nversion: 3\ntopic: demo\nlevel: Explorer\nxp: 0\nupdated: 2026-07-02\n---\n"
        "## [Build · ROOT] x\n- [ ] New title\n",
        schema_dir=schemas,
    )
    saved = (graphs / "demo.md").read_text()
    assert "[✓|exercise] Old title" in saved     # earned status preserved across the reword
    assert "id: demo-node" in saved


def test_save_graph_no_schema_degrades_to_today(monkeypatch, tmp_path):
    monkeypatch.setenv("HOME", str(tmp_path))
    empty = tmp_path / "empty-schemas"
    empty.mkdir()
    out = ramp_core.save_graph(
        "demo",
        "---\nversion: 3\ntopic: demo\nlevel: Explorer\nxp: 0\nupdated: 2026-07-02\n---\n"
        "## [Build · ROOT] x\n- [✓|exercise] a — r, 2026-07-02: n\n",
        schema_dir=empty,
    )
    saved = (tmp_path / ".claude" / "ramp" / "graphs" / "demo.md").read_text()
    assert "| id:" not in saved                  # nothing stamped
    assert "xp: 10" in saved and out.startswith("saved · demo")


def test_graph_nodes_emits_id():
    content = (
        "## [Build · ROOT] Agents\n"
        "- [✓|exercise] First — r, d: n | next: 2026-06-23 [L2] | id: b-first\n"
        "- [ ] Second | id: b-second\n"
    )
    nodes = ramp_core.graph_nodes(content)
    assert nodes[0]["id"] == "b-first" and nodes[0]["name"] == "First"
    assert nodes[1]["id"] == "b-second" and nodes[1]["name"] == "Second"


def test_validate_tree_flags_duplicate_id():
    tree = (
        "---\nxp: 0\n---\n## [Build · A] x\n"
        "- [ ] One | id: dup\n- [ ] Two | id: dup\n"
    )
    assert any("duplicate id" in p.lower() for p in ramp_core.validate_tree(tree))


# --- Task 7: ids verb (slug suggestions + lint) ---

def test_suggest_node_id_is_full_kebab():
    assert ramp_core.suggest_node_id("getting-started", "Memory types and scope hierarchy") == \
        "getting-started-memory-types-and-scope-hierarchy"
    assert ramp_core.suggest_node_id("getting-started", "How Claude Code uses computers (tool loop)") == \
        "getting-started-how-claude-code-uses-computers-tool-loop"
    assert ramp_core.suggest_node_id("gs", "Reading and verifying Claude's output") == \
        "gs-reading-and-verifying-claude-s-output"


_LINT_SCHEMA = """---
topic: demo
---

## Node definitions

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|--|--|--|--|--|--|
| Alpha | c | Q | None | u | demo-alpha |
| Beta | c | Q | None | u | demo-beta |

## Saved tree file template

```markdown
## [ROOT] x
- [STATUS|TYPE] Alpha
- [STATUS|TYPE] Beta
```
"""


def test_lint_clean_schema_has_no_problems():
    result = ramp_core.lint_schema_ids("demo", _LINT_SCHEMA)
    assert result["problems"] == []
    assert {r["title"]: r["id"] for r in result["rows"]} == {"Alpha": "demo-alpha", "Beta": "demo-beta"}


def test_lint_flags_missing_id_and_suggests_slug():
    schema = _LINT_SCHEMA.replace(" u | demo-beta |", " u |  |")  # Beta id blanked
    result = ramp_core.lint_schema_ids("demo", schema)
    beta = next(r for r in result["rows"] if r["title"] == "Beta")
    assert beta["id"] is None
    assert beta["suggested"] == "demo-beta"
    assert any("missing id" in p.lower() and "Beta" in p for p in result["problems"])


def test_lint_flags_duplicate_id():
    schema = _LINT_SCHEMA.replace("demo-beta", "demo-alpha")  # dup
    assert any("duplicate id" in p.lower() for p in ramp_core.lint_schema_ids("demo", schema)["problems"])


def test_lint_flags_template_nodedef_parity_skew():
    schema = _LINT_SCHEMA.replace("- [STATUS|TYPE] Beta", "- [STATUS|TYPE] Beta renamed")
    problems = ramp_core.lint_schema_ids("demo", schema)["problems"]
    assert any("parity" in p.lower() for p in problems)


def test_cli_ids_emits_json(tmp_path):
    plugin_root = tmp_path / "plugin"
    (plugin_root / "topics").mkdir(parents=True)
    (plugin_root / "topics" / "demo.md").write_text(_LINT_SCHEMA)
    home = tmp_path / "home"
    (home / ".claude" / "ramp" / "graphs").mkdir(parents=True)
    env = dict(os.environ)
    env["HOME"] = str(home)
    env["CLAUDE_PLUGIN_ROOT"] = str(plugin_root)
    out = subprocess.check_output(["python3", CORE, "ids", "demo"], env=env, text=True, cwd=str(tmp_path))
    data = json.loads(out)
    assert data["problems"] == []
    assert {r["title"]: r["id"] for r in data["rows"]} == {"Alpha": "demo-alpha", "Beta": "demo-beta"}


# --- Task 8: real schemas are id-native ---

TOPICS = Path(__file__).resolve().parent.parent / "topics"
SUBS = ["getting-started", "build", "configuration", "deployment", "administration"]


def test_real_leaf_schemas_lint_clean():
    for t in SUBS:
        content = (TOPICS / f"{t}.md").read_text(encoding="utf-8")
        assert ramp_core.lint_schema_ids(t, content)["problems"] == [], t


def test_composite_claude_code_unions_81_ids():
    ids = ramp_core.load_topic_node_ids("claude-code", TOPICS)
    assert len(ids) == 81
    # every title in the composite saved-tree template resolves to an id
    comp = ramp_core._template_titles((TOPICS / "claude-code.md").read_text(encoding="utf-8"))
    assert len(comp) == 81
    missing = [t for t in comp if t not in ids]
    assert missing == []


def test_leaf_ids_are_frozen_at_creation_kebab():
    # FREEZE LEDGER: at creation every id == its kebab suggestion. When a title is
    # later reworded, DO NOT change the id (it is frozen) — instead pin the old id
    # here. A divergence between this expectation and suggest_node_id() is the
    # feature working, not a bug: update this test to the frozen id, never the id.
    for t in SUBS:
        content = (TOPICS / f"{t}.md").read_text(encoding="utf-8")
        for title, nid in ramp_core.parse_node_ids(content).items():
            assert nid == ramp_core.suggest_node_id(t, title), f"{t}: {title!r}"
