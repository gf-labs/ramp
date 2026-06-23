"""SessionStart normalization keeps the personal tree's XP/dates honest."""
from datetime import date


def test_normalize_fills_missing_dates_and_recomputes_xp(observer):
    tree = (
        "---\nversion: 3\nxp: 0\nupdated: 2020-01-01\n---\n"
        "## [Build · ROOT] x\n"
        "- [✓|artifact] Needs date — r, 2026-06-22: n\n"
    )
    out, problems = observer.normalize_personal_tree(tree, date(2026, 6, 22))
    assert "| next: 2026-06-23 [L1]" in out   # missing date filled
    assert "xp: 10" in out                    # recomputed
    assert "updated: 2026-06-22" in out


def test_normalize_flags_but_keeps_malformed_date(observer):
    tree = (
        "---\nxp: 10\nupdated: 2026-06-22\n---\n## [Build · ROOT] x\n"
        "- [✓|artifact] Bad — r, d: n | next: 2026-99-99 [L1]\n"
    )
    out, problems = observer.normalize_personal_tree(tree, date(2026, 6, 22))
    assert "2026-99-99" in out                              # NOT rewritten
    assert any("2026-99-99" in p for p in problems)         # but flagged
