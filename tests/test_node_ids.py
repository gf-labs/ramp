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
