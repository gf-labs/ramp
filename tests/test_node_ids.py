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
