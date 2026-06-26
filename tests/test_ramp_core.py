"""Tier-1 unit tests for the ramp_core deterministic kernel."""
import json
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import ramp_core  # noqa: E402


def test_compute_xp_composite_header_form():
    # claude-code.md style: "## [SubTopic · TIER]"
    tree = (
        "## [Getting Started · ROOT] Core\n"
        "- [✓|exercise] a\n"
        "- [~|reported] b\n"
        "## [Build · A] Skills\n"
        "- [✓|artifact] d\n"
    )
    # ROOT: 10 (✓) + 5 (~ floored); A: 15 (✓) = 30
    assert ramp_core.compute_xp(tree) == 30


def test_compute_xp_bare_tier_header_form():
    # standalone topic style: "## [TIER]" (the format-tolerance fix)
    tree = "## [ROOT] section\n- [✓|artifact] a\n## [D] later\n- [~|reported] b\n"
    # ROOT 10 (✓) + D 35//2=17 (~) = 27
    assert ramp_core.compute_xp(tree) == 27


def test_compute_xp_subtopic_label_without_tier_is_zero():
    # "## [Getting Started]" has no tier -> contributes 0 (preserved C1 behavior)
    assert ramp_core.compute_xp("## [Getting Started] Core\n- [✓|exercise] a\n") == 0


def test_compute_xp_not_yet_nodes_zero():
    assert ramp_core.compute_xp("## [Build · C] x\n- [ ] y\n") == 0


def test_next_review_date_each_ladder_step():
    t = date(2026, 6, 22)
    assert ramp_core.next_review_date(1, t) == "2026-06-23"
    assert ramp_core.next_review_date(2, t) == "2026-06-25"
    assert ramp_core.next_review_date(3, t) == "2026-06-29"
    assert ramp_core.next_review_date(4, t) == "2026-07-13"
    assert ramp_core.next_review_date(5, t) == "2026-08-21"
    assert ramp_core.next_review_date(6, t) is None  # permanent


def test_advance_and_reset_level():
    assert ramp_core.advance_level(1) == 2
    assert ramp_core.advance_level(5) == 6
    assert ramp_core.advance_level(6) == 6  # caps at 6
    assert ramp_core.reset_level() == 1


def test_parse_review_field():
    assert ramp_core.parse_review_field("- [✓|exercise] x | next: 2026-06-25 [L2]") == (date(2026, 6, 25), 2)
    assert ramp_core.parse_review_field("- [✓] x — no schedule") is None
    assert ramp_core.parse_review_field("- [✓] x | next: 2026-13-99 [L1]") is None  # bad date


def test_is_valid_iso_date():
    assert ramp_core.is_valid_iso_date("2026-06-22") is True
    assert ramp_core.is_valid_iso_date("2026-07-32") is False
    assert ramp_core.is_valid_iso_date("2026-13-01") is False
    assert ramp_core.is_valid_iso_date("2026-6-2") is False  # must be zero-padded
    assert ramp_core.is_valid_iso_date("nope") is False


def test_validate_tree_clean():
    tree = (
        "---\nversion: 3\nxp: 10\nupdated: 2026-06-22\n---\n"
        "## [Build · ROOT] x\n"
        "- [✓|artifact] Node one — repo, 2026-06-22: note | next: 2026-06-23 [L1]\n"
    )
    assert ramp_core.validate_tree(tree) == []


def test_validate_tree_flags_bad_date_missing_next_and_xp_mismatch():
    tree = (
        "---\nversion: 3\nxp: 999\nupdated: 2026-06-22\n---\n"
        "## [Build · ROOT] x\n"
        "- [✓|artifact] Bad date — r, 2026-06-22: n | next: 2026-07-32 [L1]\n"
        "- [✓|exercise] No schedule — r, 2026-06-22: n\n"
    )
    problems = ramp_core.validate_tree(tree)
    joined = " ".join(problems)
    assert "2026-07-32" in joined            # invalid date flagged
    assert "No schedule" in joined           # missing next: flagged
    assert "999" in joined                   # xp mismatch flagged


def test_validate_tree_flags_branch_header_without_tier():
    tree = "---\nxp: 0\n---\n## [Mystery Section]\n- [ ] x\n"
    assert any("TIER" in p for p in ramp_core.validate_tree(tree))


def test_validate_tree_flags_duplicate_node():
    tree = (
        "---\nxp: 0\n---\n## [Build · A] x\n"
        "- [ ] Same name\n- [ ] Same name\n"
    )
    assert any("duplicate" in p.lower() for p in ramp_core.validate_tree(tree))


def test_apply_frontmatter_recomputes_xp_and_date():
    tree = (
        "---\nversion: 3\nxp: 0\nupdated: 2020-01-01\n---\n"
        "## [Build · ROOT] x\n- [✓|artifact] a\n"
    )
    out = ramp_core.apply_frontmatter(tree, date(2026, 6, 22))
    assert "xp: 10" in out
    assert "updated: 2026-06-22" in out


def test_set_review_field_replaces_and_handles_permanent():
    line = "- [✓|exercise] x — r, d: n | next: 2026-01-01 [L1]"
    assert ramp_core.set_review_field(line, "2026-06-25", 2).endswith("| next: 2026-06-25 [L2]")
    assert ramp_core.set_review_field(line, None, 6).endswith("| next: permanent [L6]")


def test_fill_missing_review_dates_fills_only_missing():
    tree = (
        "## [Build · ROOT] x\n"
        "- [✓|artifact] Missing — r, 2026-06-22: n\n"
        "- [✓|exercise] Malformed — r, d: n | next: 2026-99-99 [L1]\n"
        "- [✓|exercise] Has one — r, d: n | next: 2026-06-30 [L3]\n"
    )
    out, filled = ramp_core.fill_missing_review_dates(tree, date(2026, 6, 22))
    assert filled == ["Missing"]                     # only the truly-missing one
    assert "| next: 2026-06-23 [L1]" in out          # filled to L1
    assert "2026-99-99" in out                       # malformed left untouched (flagged elsewhere)
    assert "| next: 2026-06-30 [L3]" in out          # valid one untouched


def test_preserve_demonstrated_blocks_downgrade():
    existing = "## [Build · A] x\n- [✓|exercise] Kept — r, 2026-06-01: proof | next: 2026-07-01 [L3]\n"
    incoming = "## [Build · A] x\n- [ ] Kept\n"
    out, preserved = ramp_core.preserve_demonstrated(existing, incoming)
    assert preserved == ["Kept"]
    assert "[✓|exercise] Kept" in out                # restored, not downgraded
    assert "2026-07-01 [L3]" in out                  # with its schedule


def test_file_lock_is_a_contextmanager(tmp_path):
    with ramp_core.file_lock(tmp_path / ".x.lock") as fd:
        pass  # acquiring + releasing must not raise


# --- read/summary layer (discoverability slice) ---

def test_parse_frontmatter_basic():
    content = "---\nversion: 3\nlevel: Builder\nxp: 240\n---\n# body\n- [✓] x\n"
    fm = ramp_core.parse_frontmatter(content)
    assert fm["level"] == "Builder"
    assert fm["xp"] == "240"          # values are strings
    assert fm["version"] == "3"


def test_parse_frontmatter_absent():
    assert ramp_core.parse_frontmatter("# no frontmatter\n- [ ] x\n") == {}


def test_summarize_graph_counts_and_due():
    today = date(2026, 6, 24)
    content = (
        "---\nlevel: Builder\nxp: 0\n---\n"
        "## [Build · ROOT] x\n"
        "- [✓|exercise] Due node — r, d: n | next: 2026-06-20 [L1]\n"     # past -> due
        "- [✓|artifact] Future node — r, d: n | next: 2026-12-01 [L3]\n"  # future -> not due
        "- [~|reported] Reported node\n"
        "- [ ] Todo node\n"
        "- [·] Locked node\n"
    )
    s = ramp_core.summarize_graph(content, today)
    assert s["level"] == "Builder"
    assert s["counts"] == {"done": 2, "reported": 1, "todo": 1, "locked": 1}
    assert s["due"] == 1                       # only the past-dated [✓]
    # ROOT: 10+10 (two ✓) + 5 (~ floored) = 25
    assert s["xp"] == 25


def test_summarize_graph_malformed_date_not_due():
    today = date(2026, 6, 24)
    content = (
        "---\nlevel: Explorer\nxp: 0\n---\n"
        "## [Build · ROOT] x\n"
        "- [✓|exercise] Bad — r, d: n | next: 2026-99-99 [L1]\n"   # malformed -> not due
        "- [✓|exercise] None — r, d: n\n"                          # absent -> not due
    )
    s = ramp_core.summarize_graph(content, today)
    assert s["due"] == 0
    assert s["counts"]["done"] == 2


def test_summarize_graph_empty_tree_zeros():
    s = ramp_core.summarize_graph("---\nlevel: Explorer\nxp: 0\n---\n", date(2026, 6, 24))
    assert s["xp"] == 0
    assert s["due"] == 0
    assert s["counts"] == {"done": 0, "reported": 0, "todo": 0, "locked": 0}


def test_schema_node_count_prefers_frontmatter():
    # frontmatter wins even when the derived table count would differ
    content = (
        "---\ntopic: t\nnode_count: 12\n---\n## Node definitions\n"
        "### [ROOT] Branch\n"
        "| Node | Mastery criterion | Type | Auto-detect signal | source_url |\n"
        "|------|-------------------|------|--------------------|-----------|\n"
        "| Alpha | crit | Qualitative | None | http://x |\n"
        "| Beta | crit | Qualitative | None | http://x |\n"
    )
    assert ramp_core.schema_node_count(content) == 12


def test_schema_node_count_derives_from_node_definitions_section():
    # real schemas enumerate nodes as a markdown table; the header + separator
    # rows are not nodes, and the saved-tree template (bullets, a different
    # `##` section) is excluded
    content = (
        "---\ntopic: t\n---\n"
        "## Node definitions\n"
        "| Node | Mastery criterion | Type | Auto-detect signal | source_url |\n"
        "|------|-------------------|------|--------------------|-----------|\n"
        "| Alpha | c | Q | None | u |\n"
        "| Beta | c | Q | None | u |\n"
        "| Gamma | c | Q | None | u |\n"
        "## Saved tree file template\n- [✓] example one\n- [✓] example two\n"  # excluded
    )
    assert ramp_core.schema_node_count(content) == 3


def test_list_catalog_joins_catalog_with_progress(tmp_path):
    schema_dir = tmp_path / "schemas"
    graph_dir = tmp_path / "graphs"
    schema_dir.mkdir()
    graph_dir.mkdir()

    # composite (core) + one of its sub-topics + a standalone
    (schema_dir / "claude-code.md").write_text(
        "---\ntopic: claude-code\nnode_count: 81\n"
        "sources: [getting-started]\n"
        "description: Complete Claude Code curriculum.\n---\n## Node definitions\n- [ ] x\n"
    )
    (schema_dir / "getting-started.md").write_text(
        "---\ntopic: getting-started\nnode_count: 12\n"
        "description: Claude Code fundamentals.\n---\n## Node definitions\n- [ ] x\n"
    )
    (schema_dir / "best-practices.md").write_text(
        "---\ntopic: best-practices\nnode_count: 15\n"
        "description: CLAUDE.md design and hygiene.\n---\n## Node definitions\n- [ ] x\n"
    )

    # only claude-code has been started
    (graph_dir / "claude-code.md").write_text(
        "---\nlevel: Builder\nxp: 0\n---\n## [Build · ROOT] x\n"
        "- [✓|exercise] a — r, d: n | next: 2026-06-20 [L1]\n"
    )

    cat = ramp_core.list_catalog(schema_dir, graph_dir, date(2026, 6, 24))
    by_name = {c["name"]: c for c in cat}

    assert by_name["claude-code"]["group"] == "core"
    assert by_name["claude-code"]["sources"] == ["getting-started"]
    assert by_name["claude-code"]["description"] == "Complete Claude Code curriculum."
    assert by_name["claude-code"]["node_count"] == 81
    assert by_name["claude-code"]["started"] is True
    assert by_name["claude-code"]["summary"]["due"] == 1

    assert by_name["getting-started"]["group"] == "sub"
    assert by_name["getting-started"]["started"] is False
    assert by_name["getting-started"]["summary"] is None

    assert by_name["best-practices"]["group"] == "standalone"


def test_list_catalog_sorted_by_name(tmp_path):
    schema_dir = tmp_path / "schemas"
    graph_dir = tmp_path / "graphs"
    schema_dir.mkdir()
    graph_dir.mkdir()
    for n in ("zeta", "alpha", "mu"):
        (schema_dir / f"{n}.md").write_text(
            f"---\ntopic: {n}\nnode_count: 1\ndescription: d.\n---\n## Node definitions\n- [ ] x\n"
        )
    names = [c["name"] for c in ramp_core.list_catalog(schema_dir, graph_dir, date(2026, 6, 24))]
    assert names == ["alpha", "mu", "zeta"]


def test_list_catalog_first_run_signal(tmp_path):
    # §8 first-run signal: zero started graphs ⇒ no entry has started=True
    schema_dir = tmp_path / "schemas"
    graph_dir = tmp_path / "graphs"
    schema_dir.mkdir()
    graph_dir.mkdir()
    (schema_dir / "a.md").write_text(
        "---\ntopic: a\nnode_count: 1\ndescription: d.\n---\n"
    )
    cat = ramp_core.list_catalog(schema_dir, graph_dir, date(2026, 6, 24))
    assert cat and not any(c["started"] for c in cat)


def test_list_catalog_skips_unreadable_schema(tmp_path):
    # a read-only viewer must not crash the catalog over one bad entry (e.g. a
    # broken symlink in the global schema dir). A directory named `*.md`
    # reproduces the read failure portably (IsADirectoryError ⊂ OSError).
    schema_dir = tmp_path / "schemas"
    graph_dir = tmp_path / "graphs"
    schema_dir.mkdir()
    graph_dir.mkdir()
    (schema_dir / "good.md").write_text(
        "---\ntopic: good\nnode_count: 1\ndescription: d.\n---\n"
    )
    (schema_dir / "broken.md").mkdir()  # unreadable: read_text raises OSError
    names = [c["name"] for c in ramp_core.list_catalog(schema_dir, graph_dir, date(2026, 6, 24))]
    assert names == ["good"]


def test_cli_catalog_emits_json(tmp_path):
    # a plugin-root layout: topics/ as the schema dir, empty graph dir via HOME
    plugin_root = tmp_path / "plugin"
    (plugin_root / "topics").mkdir(parents=True)
    (plugin_root / "topics" / "demo.md").write_text(
        "---\ntopic: demo\nnode_count: 3\ndescription: A demo topic.\n---\n"
        "## Node definitions\n- [ ] a\n"
    )
    home = tmp_path / "home"
    (home / ".claude" / "knowledge-graphs").mkdir(parents=True)

    env = dict(os.environ)
    env["HOME"] = str(home)
    env["CLAUDE_PLUGIN_ROOT"] = str(plugin_root)
    core = str(Path(__file__).resolve().parent.parent / "ramp_core.py")

    out = subprocess.check_output(["python3", core, "catalog"], env=env, text=True, cwd=str(tmp_path))
    data = json.loads(out)
    assert isinstance(data, list)
    demo = next(c for c in data if c["name"] == "demo")
    assert demo["description"] == "A demo topic."
    assert demo["started"] is False


def test_cli_summary_missing_graph_is_empty_object(tmp_path):
    home = tmp_path / "home"
    (home / ".claude" / "knowledge-graphs").mkdir(parents=True)
    env = dict(os.environ)
    env["HOME"] = str(home)
    env.pop("CLAUDE_PLUGIN_ROOT", None)
    core = str(Path(__file__).resolve().parent.parent / "ramp_core.py")
    out = subprocess.check_output(["python3", core, "summary", "nope"], env=env, text=True, cwd=str(tmp_path))
    assert json.loads(out) == {}


def test_cli_summary_existing_graph_emits_summary(tmp_path):
    home = tmp_path / "home"
    graphs = home / ".claude" / "knowledge-graphs"
    graphs.mkdir(parents=True)
    (graphs / "demo.md").write_text(
        "---\nversion: 3\ntopic: demo\nlevel: Builder\nxp: 10\n---\n\n"
        "## [Getting Started · ROOT] Core\n\n"
        "- [✓|exercise] Node one — repo, 2020-01-01: did it | next: 2020-01-01 [L1]\n"
        "- [ ] Node two\n"
    )
    env = dict(os.environ)
    env["HOME"] = str(home)
    env.pop("CLAUDE_PLUGIN_ROOT", None)
    core = str(Path(__file__).resolve().parent.parent / "ramp_core.py")
    out = subprocess.check_output(["python3", core, "summary", "demo"], env=env, text=True, cwd=str(tmp_path))
    data = json.loads(out)
    assert data["level"] == "Builder"
    assert data["due"] == 1                    # next: 2020-01-01 is long past
    assert data["counts"]["done"] == 1
    assert data["counts"]["todo"] == 1


def test_all_schemas_declare_consistent_node_count():
    topics_dir = Path(__file__).resolve().parent.parent / "topics"
    schemas = {}
    for path in sorted(topics_dir.glob("*.md")):
        content = path.read_text(encoding="utf-8")
        fm = ramp_core.parse_frontmatter(content)
        assert "node_count" in fm, f"{path.name}: missing node_count frontmatter"
        schemas[path.stem] = (fm, content)

    for name, (fm, content) in schemas.items():
        declared = int(fm["node_count"])
        if "sources" in fm:  # composite: must equal the sum of its sub-topics
            srcs = ramp_core._parse_sources(fm["sources"])
            total = sum(int(schemas[s][0]["node_count"]) for s in srcs)
            assert declared == total, f"{name}: node_count {declared} != sum of sources {total}"
        else:  # leaf: frontmatter must match the derived Node-definitions count
            derived = ramp_core._derived_node_count(content)
            assert declared == derived, f"{name}: node_count {declared} != derived {derived}"


# --- python version contract ---

def test_python_version_error_below_floor():
    assert ramp_core.python_version_error((3, 7)) == "ramp needs Python 3.8+ (found 3.7)."
    assert ramp_core.python_version_error((3, 6, 9)) == "ramp needs Python 3.8+ (found 3.6)."
    assert ramp_core.python_version_error((2, 7, 18)) == "ramp needs Python 3.8+ (found 2.7)."


def test_python_version_error_at_or_above_floor():
    assert ramp_core.python_version_error((3, 8)) is None
    assert ramp_core.python_version_error((3, 12, 1)) is None
    assert ramp_core.python_version_error((4, 0)) is None


def test_python_version_floor_is_declared():
    # the floor the code enforces must match the README badge / Requirements
    assert ramp_core.MIN_PYTHON == (3, 8)
