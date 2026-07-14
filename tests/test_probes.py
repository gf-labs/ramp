"""Detection probe layer — declarative, read-only primitives + the detect runner.

Each primitive reads the filesystem/git and returns a scalar, degrading to its
zero value on any error. `run_probe` is the dispatch; `run_detection` runs a
topic's declared probes. STDLIB-ONLY, like the kernel it lives in.
"""
import json
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


def test_cmd_gated_when_untrusted():
    assert ramp_core.run_probe("cmd", "echo hi", trusted=False) == "SKIPPED_UNTRUSTED"


def test_cmd_runs_when_trusted():
    assert ramp_core.run_probe("cmd", "echo hi", trusted=True) == "hi"


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
# banner contract). These three fixes address reproducible crashes found by
# an independent review of Task 1.

# Fix 1: `run_probe` tokenizes `arg_str` with shlex unconditionally, even
# though `cmd` never uses the tokens — shell-hostile input (e.g. an
# apostrophe) blows up shlex before `cmd`'s own branch is ever reached.

def test_cmd_survives_shell_hostile_quoting():
    result = ramp_core.run_probe("cmd", "echo it's fine", trusted=True)
    assert isinstance(result, str)


def test_cmd_runs_real_shell_syntax():
    assert ramp_core.run_probe("cmd", "echo hi | tr a-z A-Z", trusted=True) == "HI"


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
