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
