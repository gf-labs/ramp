"""Adapter tests for the knowledge-graph MCP server (save_graph, advance_review).

mcp/server.py needs the .venv's real FastMCP. Run from the repo root, the repo's
own `mcp/` directory (a namespace package, no __init__.py) shadows the import, so
under the system python3 (no real mcp) importing the FastMCP entrypoint runs the
local mcp/server.py and raises SystemExit — not ImportError. So importorskip is
insufficient: catch BaseException and skip the whole module when FastMCP isn't
importable, and run where the .venv provides it.
"""
import importlib.util
import sys
from pathlib import Path

import pytest

try:
    from mcp.server.fastmcp import FastMCP  # noqa: F401  (the .venv's real package)
except BaseException:
    pytest.skip(
        "mcp .venv not available (system python3 lacks FastMCP)",
        allow_module_level=True,
    )

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


@pytest.fixture()
def server(monkeypatch, tmp_path):
    spec = importlib.util.spec_from_file_location("kg_server", ROOT / "mcp" / "server.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    monkeypatch.setattr(mod, "GRAPH_DIR", tmp_path)  # isolate writes
    monkeypatch.setattr(mod, "API_URL", "")          # never touch a real backend
    return mod


def test_save_graph_recomputes_xp(server, tmp_path):
    content = (
        "---\nversion: 3\nlevel: Builder\nxp: 999\nupdated: 2020-01-01\n---\n"
        "## [Build · ROOT] x\n- [✓|artifact] a — r, 2026-06-22: n | next: 2026-06-23 [L1]\n"
    )
    server.save_graph("t", content)
    saved = (tmp_path / "t.md").read_text()
    assert "xp: 10" in saved          # overwrote the model's 999
    assert "xp: 999" not in saved


def test_save_graph_never_downgrades(server, tmp_path):
    (tmp_path / "t.md").write_text(
        "---\nxp: 15\nupdated: 2026-06-01\n---\n## [Build · A] x\n"
        "- [✓|exercise] Kept — r, 2026-06-01: proof | next: 2026-07-01 [L3]\n"
    )
    incoming = "---\nxp: 0\nupdated: 2026-06-22\n---\n## [Build · A] x\n- [ ] Kept\n"
    result = server.save_graph("t", incoming)
    saved = (tmp_path / "t.md").read_text()
    assert "[✓|exercise] Kept" in saved        # restored
    assert "preserved" in result.lower()


def test_save_graph_fills_missing_review_date(server, tmp_path):
    content = (
        "---\nxp: 0\nupdated: 2026-06-22\n---\n## [Build · ROOT] x\n"
        "- [✓|artifact] NoDate — r, 2026-06-22: n\n"
    )
    server.save_graph("t", content)
    saved = (tmp_path / "t.md").read_text()
    assert "| next:" in saved


def test_save_graph_rejects_frontmatterless(server):
    result = server.save_graph("t", "## [Build · ROOT] x\n- [✓] a\n")
    assert result.startswith("REJECTED")


def test_advance_review_pass_advances_level_and_date(server, tmp_path):
    (tmp_path / "t.md").write_text(
        "---\nxp: 15\nupdated: 2026-06-01\n---\n## [Build · A] x\n"
        "- [✓|exercise] Recursion — r, 2026-06-01: n | next: 2026-06-22 [L1]\n"
    )
    result = server.advance_review("t", "Recursion", "pass")
    saved = (tmp_path / "t.md").read_text()
    assert "[L2]" in saved                # L1 -> L2
    assert "L2" in result


def test_advance_review_fail_resets_to_l1(server, tmp_path):
    (tmp_path / "t.md").write_text(
        "---\nxp: 15\nupdated: 2026-06-01\n---\n## [Build · A] x\n"
        "- [✓|exercise] Recursion — r, 2026-06-01: n | next: 2026-06-22 [L4]\n"
    )
    server.advance_review("t", "Recursion", "fail")
    saved = (tmp_path / "t.md").read_text()
    assert "[L1]" in saved                # reset


def test_advance_review_unknown_node(server, tmp_path):
    (tmp_path / "t.md").write_text("---\nxp: 0\n---\n## [Build · A] x\n- [ ] Other\n")
    assert "not found" in server.advance_review("t", "Nope", "pass").lower()


def test_advance_review_exact_node_match_not_substring(server, tmp_path):
    # Finding #1: a substring match would wrongly advance "Recursion basics" when
    # asked for "Recursion". Exact node_name matching must target only "Recursion".
    (tmp_path / "t.md").write_text(
        "---\nxp: 35\nupdated: 2026-06-01\n---\n## [Build · A] x\n"
        "- [✓|exercise] Recursion basics — r, 2026-06-01: n | next: 2026-06-22 [L1]\n"
        "- [✓|exercise] Recursion — r, 2026-06-01: n | next: 2026-06-22 [L1]\n"
    )
    server.advance_review("t", "Recursion", "pass")
    saved = (tmp_path / "t.md").read_text().splitlines()
    basics = next(ln for ln in saved if "Recursion basics" in ln)
    target = next(ln for ln in saved if "] Recursion —" in ln)
    assert "[L1]" in basics                # untouched — not the requested node
    assert "[L2]" in target                # the exact match advanced


def test_advance_review_repairs_malformed_level_on_pass(server, tmp_path):
    # Regression: a real dogfood graph carried `| next: 2026-06-01 [B]` — a section
    # tier letter had leaked into the SR-level slot where `[L<n>]` belongs.
    # parse_review_field can't read `[B]`, so advance_review must not get stuck: the
    # `cur_level = parsed[1] if parsed else 1` fallback treats the unparseable level
    # as L1 and set_review_field rewrites a clean, forward-dated field — the malformed
    # token is never carried forward.
    (tmp_path / "t.md").write_text(
        "---\nxp: 35\nupdated: 2026-06-01\n---\n## [Administration · B] x\n"
        "- [✓|exercise] Token limits — r, 2026-05-31: n | next: 2026-06-01 [B]\n"
    )
    result = server.advance_review("t", "Token limits", "pass")
    line = next(ln for ln in (tmp_path / "t.md").read_text().splitlines()
                if "Token limits" in ln)
    assert "[B]" not in line                # malformed token removed — not stuck
    assert "[L2]" in line                   # unparseable level -> L1 default -> pass -> L2
    assert "2026-06-01" not in line         # stale date rewritten forward
    assert line.count("| next:") == 1       # field replaced, never duplicated
    assert "L2" in result


def test_advance_review_repairs_malformed_level_on_fail(server, tmp_path):
    (tmp_path / "t.md").write_text(
        "---\nxp: 35\nupdated: 2026-06-01\n---\n## [Administration · B] x\n"
        "- [✓|exercise] Token limits — r, 2026-05-31: n | next: 2026-06-01 [B]\n"
    )
    server.advance_review("t", "Token limits", "fail")
    line = next(ln for ln in (tmp_path / "t.md").read_text().splitlines()
                if "Token limits" in ln)
    assert "[B]" not in line                # repaired regardless of outcome
    assert "[L1]" in line                   # fail always resets to L1
