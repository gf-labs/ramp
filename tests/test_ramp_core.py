"""Tier-1 unit tests for the ramp_core deterministic kernel."""
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
