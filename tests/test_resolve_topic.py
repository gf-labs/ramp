"""Topic-argument resolution — the kebab-case names users type as words.

Every /ramp: command routes its argument through resolve_topic. Before it
existed each command matched only the first word, which made every
hyphenated topic (object-oriented-design, mcp-development) unreachable: the
argument silently fell back to the default and the user got the wrong tree.
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import ramp_core  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

NAMES = [
    "claude-code",
    "claude-code-internals",
    "getting-started",
    "git",
    "mcp-development",
    "object-oriented-design",
]


def _schemas(tmp_path):
    d = tmp_path / "schemas"
    d.mkdir()
    for name in NAMES:
        (d / f"{name}.md").write_text(f"---\ntopic: {name}\n---\n", encoding="utf-8")
    return d


def test_multi_word_argument_resolves_to_kebab_topic(tmp_path):
    got = ramp_core.resolve_topic("object oriented design", _schemas(tmp_path))
    assert got == {
        "topic": "object-oriented-design",
        "remainder": "",
        "matched": True,
    }


def test_already_hyphenated_argument_still_resolves(tmp_path):
    got = ramp_core.resolve_topic("object-oriented-design", _schemas(tmp_path))
    assert got["topic"] == "object-oriented-design"
    assert got["matched"] is True


def test_partially_hyphenated_argument_resolves(tmp_path):
    # 2 words, 3 segments — the case that makes the scan bound by segments
    # rather than by word count.
    got = ramp_core.resolve_topic("object-oriented design", _schemas(tmp_path))
    assert got["topic"] == "object-oriented-design"


def test_longest_match_wins_over_shorter_prefix(tmp_path):
    # "claude code" is itself a topic; the longer name must not be shadowed.
    got = ramp_core.resolve_topic("claude code internals", _schemas(tmp_path))
    assert got["topic"] == "claude-code-internals"
    assert got["remainder"] == ""


def test_trailing_context_is_preserved_verbatim(tmp_path):
    got = ramp_core.resolve_topic(
        "mcp development I'm building a server", _schemas(tmp_path))
    assert got["topic"] == "mcp-development"
    assert got["remainder"] == "I'm building a server"


def test_consultant_mode_punctuation_survives_in_remainder(tmp_path):
    # up.md's Mode D triggers on a literal "?" in the remainder — stripping
    # punctuation for matching must not strip it from what is handed back.
    got = ramp_core.resolve_topic(
        "git, which skills apply here?", _schemas(tmp_path))
    assert got["topic"] == "git"
    assert got["remainder"] == "which skills apply here?"


def test_case_is_normalized(tmp_path):
    got = ramp_core.resolve_topic("Object Oriented Design", _schemas(tmp_path))
    assert got["topic"] == "object-oriented-design"


def test_unknown_topic_falls_back_and_reports_no_match(tmp_path):
    got = ramp_core.resolve_topic("kubernetes please", _schemas(tmp_path))
    assert got == {
        "topic": "claude-code",
        "remainder": "kubernetes please",
        "matched": False,
    }


def test_empty_argument_falls_back(tmp_path):
    got = ramp_core.resolve_topic("", _schemas(tmp_path))
    assert (got["topic"], got["remainder"], got["matched"]) == (
        "claude-code", "", False)


def test_default_is_caller_supplied(tmp_path):
    # calibrate.md places newcomers on getting-started, not claude-code.
    got = ramp_core.resolve_topic(
        "", _schemas(tmp_path), default="getting-started")
    assert got["topic"] == "getting-started"


def test_graph_only_topic_is_resolvable(tmp_path):
    # /ramp:tree must still open a graph whose schema is no longer installed.
    graphs = tmp_path / "graphs"
    graphs.mkdir()
    (graphs / "retired-topic.md").write_text("---\n---\n", encoding="utf-8")
    got = ramp_core.resolve_topic(
        "retired topic", _schemas(tmp_path), graph_dir=graphs)
    assert got["topic"] == "retired-topic"


def test_missing_schema_dir_falls_back_without_raising(tmp_path):
    got = ramp_core.resolve_topic("git", tmp_path / "nope")
    assert got["topic"] == "claude-code"
    assert got["matched"] is False


def test_lock_files_are_not_resolvable_topics(tmp_path):
    # The graph home holds .<topic>.md.lock siblings; a dotfile is never a topic.
    graphs = tmp_path / "graphs"
    graphs.mkdir()
    (graphs / ".claude-code.md").write_text("", encoding="utf-8")
    assert ".claude-code" not in ramp_core.known_topics(
        _schemas(tmp_path), graphs)


def _cli(tmp_path, *argv):
    """Run the CLI against a fixture schema home, never the real corpus —
    _schema_dir() finds $HOME/.claude/ramp/schemas before the plugin's
    topics/, so pointing HOME at tmp_path pins what is resolvable."""
    home = tmp_path / "home" / ".claude" / "ramp" / "schemas"
    home.mkdir(parents=True)
    for name in NAMES:
        (home / f"{name}.md").write_text(f"topic: {name}\n", encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(ROOT / "ramp_core.py"), *argv],
        capture_output=True, text=True, cwd=str(tmp_path),
        env={"PATH": "/usr/bin:/bin", "HOME": str(tmp_path / "home")},
    )


def test_cli_bare_form_prints_only_the_name(tmp_path):
    out = _cli(tmp_path, "resolve", "--", "object oriented design")
    assert out.returncode == 0
    assert out.stdout.strip() == "object-oriented-design"


def test_cli_json_form_carries_remainder_and_match(tmp_path):
    out = _cli(tmp_path, "resolve", "--json", "--",
               "object oriented design and more")
    assert out.returncode == 0
    got = json.loads(out.stdout)
    assert got["topic"] == "object-oriented-design"
    assert got["remainder"] == "and more"
    assert got["matched"] is True


def test_cli_honors_the_default_flag(tmp_path):
    out = _cli(tmp_path, "resolve", "--default", "getting-started", "--", "")
    assert out.returncode == 0
    assert out.stdout.strip() == "getting-started"
