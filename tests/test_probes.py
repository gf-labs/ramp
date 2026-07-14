"""Detection probe layer — declarative, read-only primitives + the detect runner.

Each primitive reads the filesystem/git and returns a scalar, degrading to its
zero value on any error. `run_probe` is the dispatch; `run_detection` runs a
topic's declared probes. STDLIB-ONLY, like the kernel it lives in.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import ramp_core  # noqa: E402


def test_file_exists_true_and_false(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "CLAUDE.local.md").write_text("x")
    assert ramp_core.run_probe("file-exists", "CLAUDE.local.md") is True
    assert ramp_core.run_probe("file-exists", "nope.md") is False


def test_file_lines_counts_and_zero_when_absent(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "CLAUDE.md").write_text("a\nb\nc\n")
    assert ramp_core.run_probe("file-lines", "CLAUDE.md") == 3
    assert ramp_core.run_probe("file-lines", "absent.md") == 0


def test_glob_count_with_exclude(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    proj = tmp_path / "p"
    (proj / "a").mkdir(parents=True)
    (proj / "a" / "s1.jsonl").write_text("")
    (proj / "a" / "agent-s2.jsonl").write_text("")
    # all .jsonl = 2; excluding agent-* = 1
    assert ramp_core.run_probe("glob-count", "p/**/*.jsonl") == 2
    assert ramp_core.run_probe(
        "glob-count", "p/**/*.jsonl --exclude p/**/agent-*.jsonl"
    ) == 1


def test_dir_count(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    d = tmp_path / "wt"
    d.mkdir()
    (d / "one").mkdir()
    (d / "two").mkdir()
    assert ramp_core.run_probe("dir-count", "wt") == 2
    assert ramp_core.run_probe("dir-count", "absent") == 0


def test_json_has_key_and_value(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".mcp.json").write_text(json.dumps({"mcpServers": {"kg": {}}}))
    (tmp_path / "empty.json").write_text(json.dumps({"mcpServers": {}}))
    assert ramp_core.run_probe("json-has-key", ".mcp.json mcpServers") is True
    assert ramp_core.run_probe("json-has-key", "empty.json mcpServers") is False  # {} is not "has"
    assert ramp_core.run_probe("json-has-key", "absent.json mcpServers") is False
    (tmp_path / "settings.json").write_text(json.dumps({"permissions": {"defaultMode": "plan"}}))
    assert ramp_core.run_probe("json-value", "settings.json permissions.defaultMode") == "plan"
    assert ramp_core.run_probe("json-value", "settings.json permissions.absent") is None


def test_grep_count_recursive(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    (scripts / "run.sh").write_text("claude -p 'hi'\nclaude --print 'yo'\necho done\n")
    # two matching lines under scripts/; Makefile and .github/ absent -> skipped, no error
    assert ramp_core.run_probe("grep-count", '"claude -p|claude --print" scripts/ Makefile .github/') == 2


def test_git_worktree_count_in_a_repo(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=tmp_path, check=True)
    (tmp_path / "f").write_text("x")
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "init"], cwd=tmp_path, check=True)
    # a fresh repo has exactly one worktree (the main checkout)
    assert ramp_core.run_probe("git-worktree-count", "") == 1


def test_git_worktree_count_outside_repo_is_zero(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # not a git repo
    assert ramp_core.run_probe("git-worktree-count", "") == 0


# --- Fix pass 1: robustness guards ------------------------------------------
# Every primitive must degrade to its zero value on error (the probe-layer
# banner contract). These fixes address reproducible crashes found by an
# independent review of Task 1.

# Fix 1: `run_probe` tokenizes `arg_str` with shlex unconditionally; shell-
# hostile input (e.g. an unbalanced quote) must not blow up shlex — it degrades
# to no-tokens and the primitive returns its zero value.

def test_shlex_hostile_args_degrade_not_crash():
    assert ramp_core.run_probe("file-exists", "it's") is False


# Fix 2: token-indexed branches (toks[0]/toks[1]/pos[0]) raise IndexError when
# a `## Probes` row's args cell is empty or shorter than the primitive needs.
# Each must degrade to its documented zero value instead.

def test_file_exists_missing_arg_is_false():
    assert ramp_core.run_probe("file-exists", "") is False


def test_file_lines_missing_arg_is_zero():
    assert ramp_core.run_probe("file-lines", "") == 0


def test_dir_count_missing_arg_is_zero():
    assert ramp_core.run_probe("dir-count", "") == 0


def test_glob_count_exclude_only_is_zero():
    # --exclude consumes both tokens; no positional pattern remains
    assert ramp_core.run_probe("glob-count", "--exclude foo") == 0


def test_json_has_key_missing_args_is_false():
    assert ramp_core.run_probe("json-has-key", "") is False
    assert ramp_core.run_probe("json-has-key", "only-one-token.json") is False


def test_json_value_missing_args_is_none():
    assert ramp_core.run_probe("json-value", "") is None
    assert ramp_core.run_probe("json-value", "only-one-token.json") is None


def test_grep_count_missing_arg_is_zero():
    assert ramp_core.run_probe("grep-count", "") == 0


def test_git_log_grep_missing_arg_is_zero():
    assert ramp_core.run_probe("git-log-grep", "") == 0


# Fix 3: an invalid regex reaches Python's re.compile() uncaught in both
# _probe_grep_count and _probe_git_log_grep's --diff-filter branch. re.error
# (aka re.PatternError) is not an OSError/ValueError, so neither existing
# except clause on those paths would have caught it.

def test_grep_count_bad_regex_is_zero(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert ramp_core.run_probe("grep-count", '"(" .') == 0


def test_git_log_grep_diff_filter_bad_regex_is_zero(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert ramp_core.run_probe("git-log-grep", '"(" --diff-filter=A') == 0


# Minor: positive git-log-grep coverage (previously zero — this gap is how
# Fix 3's crash slipped through Task 1's own review).

def test_git_log_grep_diff_filter_counts_added_files_matching_regex(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=tmp_path, check=True)
    (tmp_path / "foo.py").write_text("x")
    (tmp_path / "bar.md").write_text("x")
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "init"], cwd=tmp_path, check=True)
    # both files are "added" in the root commit; only foo.py matches [.]py$
    assert ramp_core.run_probe("git-log-grep", '"[.]py$" --diff-filter=A') == 1


def test_git_log_grep_bare_commit_message_match(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=tmp_path, check=True)
    (tmp_path / "f").write_text("x")
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "feat: add widget"], cwd=tmp_path, check=True)
    (tmp_path / "f").write_text("y")
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "chore: bump deps"], cwd=tmp_path, check=True)
    # only the "feat: add widget" commit message matches ^feat
    assert ramp_core.run_probe("git-log-grep", '"^feat"') == 1


# --- git-max-commit-files: the no-shell replacement for the removed `cmd`
# probe (Task 6 fork B). up.md's legacy scan took the max "N files changed"
# over the last 10 commits via a shell pipe; this reproduces it with no shell.

def test_git_max_commit_files_counts_max_in_recent_commits(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=tmp_path, check=True)
    (tmp_path / "a").write_text("x")
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "one file"], cwd=tmp_path, check=True)
    for nm in ("b", "c", "d"):
        (tmp_path / nm).write_text("x")
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "three files"], cwd=tmp_path, check=True)
    # last two commits touched 1 and 3 files -> max is 3
    assert ramp_core.run_probe("git-max-commit-files", "10") == 3


def test_git_max_commit_files_outside_repo_is_zero(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # not a git repo
    assert ramp_core.run_probe("git-max-commit-files", "10") == 0


def test_git_max_commit_files_missing_arg_defaults_and_is_zero(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # empty args -> default n=10, no crash, 0 outside repo
    assert ramp_core.run_probe("git-max-commit-files", "") == 0


# --- Fork B: the arbitrary-shell `cmd` primitive + its trust gate were removed
# (Task 6). run_probe must treat `cmd` (and any unknown primitive) as inert and
# NEVER execute a shell — asserted positively here, not just by grep-absence, so
# a silent reintroduction of a shell surface fails the suite.

def test_removed_cmd_primitive_is_inert_and_runs_no_shell(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    sentinel = tmp_path / "PWNED"
    assert ramp_core.run_probe("cmd", f"touch {sentinel}") == "UNKNOWN_PRIMITIVE:cmd"
    assert not sentinel.exists()  # the payload was never executed
    # shell metacharacters in an unknown primitive's args are likewise never run
    assert ramp_core.run_probe("shell", "git status; rm -rf .") == "UNKNOWN_PRIMITIVE:shell"


# --- Item 1 (whole-branch review): the `skill_bash_injection` probe restores the
# base up.md scan for `!`-injection lines under .claude/commands + .claude/agents,
# which build.md's "Skill mechanics" node consumes. Pins the exact args string
# (incl. the "^\\s*!" regex through parse-args -> shlex -> re) declared in build.md.

def test_skill_bash_injection_probe_counts_leading_bang_lines(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    cmds = tmp_path / ".claude" / "commands"
    cmds.mkdir(parents=True)
    (cmds / "clean.md").write_text("---\ndesc: x\n---\n!`git status`\nplain text\n")
    (cmds / "plain.md").write_text("no injection here\n")
    agents = tmp_path / ".claude" / "agents"
    agents.mkdir(parents=True)
    (agents / "r.md").write_text("  !ls\n")  # indented `!` still counts (lstrip semantics)
    assert ramp_core.run_probe(
        "grep-count", '"^\\s*!" .claude/commands .claude/agents'
    ) == 2


# --- Probe-table parsing + composite source union ---------------------------

PROBES_BLOCK = """---
topic: demo
---

## Probes

| name | primitive | args |
|------|-----------|------|
| sessions             | glob-count   | ~/.claude/projects/**/*.jsonl --exclude ~/.claude/projects/**/agent-*.jsonl |
| claude_md_lines      | file-lines   | CLAUDE.md |
| headless_invocations | grep-count   | "claude -p\\|claude --print" scripts/ Makefile .github/ |
| worktrees            | git-worktree-count | — |

## Detection signals

| Collected evidence | Node -> status |
|--------------------|----------------|
| sessions > 5 | A -> [~] |
"""


def test_parse_probes_reads_rows_and_unescapes_pipes():
    rows = ramp_core.parse_probes(PROBES_BLOCK)
    by_name = {r[0]: (r[1], r[2]) for r in rows}
    assert by_name["sessions"] == (
        "glob-count",
        "~/.claude/projects/**/*.jsonl --exclude ~/.claude/projects/**/agent-*.jsonl",
    )
    assert by_name["claude_md_lines"] == ("file-lines", "CLAUDE.md")
    # the escaped table pipe is restored to a literal | in the args
    assert by_name["headless_invocations"] == (
        "grep-count",
        '"claude -p|claude --print" scripts/ Makefile .github/',
    )
    # an em-dash "no args" cell becomes an empty string
    assert by_name["worktrees"] == ("git-worktree-count", "")
    # only the Probes table is read, not the Detection signals table
    assert "sessions > 5" not in {r[0] for r in rows}


def _write_schema(d, name, frontmatter, probes_rows):
    body = "---\n" + frontmatter + "---\n\n## Probes\n\n| name | primitive | args |\n|--|--|--|\n"
    for row in probes_rows:
        body += "| " + " | ".join(row) + " |\n"
    (d / (name + ".md")).write_text(body)


def test_load_topic_probes_unions_sources_first_wins(tmp_path):
    d = tmp_path / "schemas"
    d.mkdir()
    # composite declares no probes of its own, sources two sub-schemas
    _write_schema(d, "combo", "topic: combo\nsources: [subA, subB]\n", [])
    _write_schema(d, "subA", "topic: subA\n", [
        ("sessions", "glob-count", "a/**/*.jsonl"),
        ("shared", "file-lines", "A.md"),
    ])
    _write_schema(d, "subB", "topic: subB\n", [
        ("worktrees", "git-worktree-count", "—"),
        ("shared", "file-lines", "B.md"),  # duplicate name: first (subA) wins
    ])
    probes = ramp_core.load_topic_probes("combo", d)
    assert probes["sessions"] == ("glob-count", "a/**/*.jsonl")
    assert probes["worktrees"] == ("git-worktree-count", "")
    assert probes["shared"] == ("file-lines", "A.md")  # first declaration wins


def test_run_detection_end_to_end(tmp_path, monkeypatch):
    # a synthetic repo + schema; assert the runner wires probes -> values.
    # The `headless` grep-count probe is declared with an ESCAPED pipe (\|) so this
    # test pins the full markdown -> parse_probes (unescape) -> shlex -> re path in
    # CI — the exact escape path the regex-bearing probes take, and the layer most
    # likely to silently regress. Without this, that path is only checked by the
    # un-committed, machine-dependent Task 6 gate.
    home = tmp_path / "home"
    (home / ".claude" / "projects" / "x").mkdir(parents=True)
    (home / ".claude" / "projects" / "x" / "s1.jsonl").write_text("")
    (home / ".claude" / "projects" / "x" / "agent-s2.jsonl").write_text("")
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "CLAUDE.md").write_text("a\nb\n")
    (repo / ".mcp.json").write_text(json.dumps({"mcpServers": {"kg": {}}}))
    scripts = repo / "scripts"
    scripts.mkdir()
    (scripts / "run.sh").write_text("claude -p hi\nclaude --print yo\necho skip\n")
    schemas = tmp_path / "schemas"
    schemas.mkdir()
    (schemas / "demo.md").write_text(
        "---\ntopic: demo\n---\n\n## Probes\n\n"
        "| name | primitive | args |\n|--|--|--|\n"
        "| sessions        | glob-count   | ~/.claude/projects/**/*.jsonl --exclude ~/.claude/projects/**/agent-*.jsonl |\n"
        "| claude_md_lines | file-lines   | CLAUDE.md |\n"
        "| mcp_project     | json-has-key | .mcp.json mcpServers |\n"
        "| claude_local    | file-exists  | CLAUDE.local.md |\n"
        "| headless        | grep-count   | \"claude -p\\|claude --print\" scripts/ |\n"
    )
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.chdir(repo)
    result = ramp_core.run_detection("demo", schemas)
    assert result == {
        "sessions": 1,          # s1.jsonl counted, agent-s2 excluded
        "claude_md_lines": 2,
        "mcp_project": True,
        "claude_local": False,
        "headless": 2,          # \| in the table cell -> real alternation at re; both lines match
    }
    text = ramp_core.format_detection(result)
    assert "sessions=1" in text
    assert "mcp_project=true" in text
    assert "claude_local=false" in text
    assert "headless=2" in text


def test_cli_detect_emits_name_value_block(tmp_path):
    plugin_root = tmp_path / "plugin"
    topics = plugin_root / "topics"
    topics.mkdir(parents=True)
    (topics / "demo.md").write_text(
        "---\ntopic: demo\n---\n\n## Probes\n\n"
        "| name | primitive | args |\n|--|--|--|\n"
        "| claude_md_lines | file-lines  | CLAUDE.md |\n"
        "| claude_local    | file-exists | CLAUDE.local.md |\n"
    )
    work = tmp_path / "work"
    work.mkdir()
    (work / "CLAUDE.md").write_text("one\ntwo\nthree\n")
    home = tmp_path / "home"
    (home / ".claude" / "ramp" / "graphs").mkdir(parents=True)

    env = dict(os.environ)
    env["HOME"] = str(home)
    env["CLAUDE_PLUGIN_ROOT"] = str(plugin_root)
    core = str(Path(__file__).resolve().parent.parent / "ramp_core.py")
    out = subprocess.check_output(["python3", core, "detect", "demo"], env=env, text=True, cwd=str(work))
    lines = set(out.strip().splitlines())
    assert "claude_md_lines=3" in lines
    assert "claude_local=false" in lines


def test_cli_detect_unknown_topic_is_empty(tmp_path):
    home = tmp_path / "home"
    (home / ".claude" / "ramp" / "graphs").mkdir(parents=True)
    env = dict(os.environ)
    env["HOME"] = str(home)
    env.pop("CLAUDE_PLUGIN_ROOT", None)
    core = str(Path(__file__).resolve().parent.parent / "ramp_core.py")
    out = subprocess.check_output(["python3", core, "detect", "nope"], env=env, text=True, cwd=str(tmp_path))
    assert out.strip() == ""
