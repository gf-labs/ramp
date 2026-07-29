"""check-docs.py — docs-consistency gate tests. Builds tiny fake repos in tmp_path."""
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "check-docs.py"

README = """# x
<img src="https://img.shields.io/badge/topics-2-6366f1?style=flat-square" alt="topics">
## The commands
| Command | What it does |
|---------|--------------|
| `/ramp:up [topic]` | engine |
| `/ramp:tree [topic]` | viewer |
## Topics
| Topic | Command | Nodes | Focus |
|-------|---------|-------|-------|
| `alpha` | `/ramp:up` | 3 | a |
| `beta` | `/ramp:up beta` | 4 | b |
| *(your topic)* | `/ramp:up [topic]` | any | custom |
See [docs/notes.md](docs/notes.md).
"""

CLAUDE_MD = """# CLAUDE.md
## Structure
```
commands/up.md               # engine
topics/alpha.md              # schema
docs/                        # docs
```
"""


def make_repo(tmp_path, readme=README, claude=CLAUDE_MD):
    repo = tmp_path / "repo"
    for d in ("commands", "topics", "docs"):
        (repo / d).mkdir(parents=True)
    (repo / "commands" / "up.md").write_text("x")
    (repo / "commands" / "tree.md").write_text("x")
    (repo / "topics" / "alpha.md").write_text("x")
    (repo / "topics" / "beta.md").write_text("x")
    (repo / "docs" / "notes.md").write_text("x")
    (repo / "README.md").write_text(readme)
    (repo / "CLAUDE.md").write_text(claude)
    return repo


def run(repo):
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--repo", str(repo)],
        capture_output=True, text=True,
    )


def test_consistent_repo_passes(tmp_path):
    result = run(make_repo(tmp_path))
    assert result.returncode == 0, result.stdout + result.stderr


def test_command_table_vs_files_mismatch_fails(tmp_path):
    repo = make_repo(tmp_path)
    (repo / "commands" / "extra.md").write_text("x")   # file with no table row
    result = run(repo)
    assert result.returncode == 1
    assert "command" in result.stdout.lower()


def test_topics_badge_mismatch_fails(tmp_path):
    repo = make_repo(tmp_path, readme=README.replace("topics-2", "topics-9"))
    result = run(repo)
    assert result.returncode == 1
    assert "badge" in result.stdout.lower()


def test_missing_topic_schema_fails(tmp_path):
    repo = make_repo(tmp_path)
    (repo / "topics" / "beta.md").unlink()
    result = run(repo)
    assert result.returncode == 1
    assert "beta" in result.stdout


def test_broken_relative_link_fails(tmp_path):
    repo = make_repo(tmp_path)
    (repo / "docs" / "notes.md").unlink()
    result = run(repo)
    assert result.returncode == 1
    assert "notes.md" in result.stdout


def test_docs_links_checked_relative_to_containing_file(tmp_path):
    repo = make_repo(tmp_path)
    (repo / "docs" / "extra.md").write_text("x")
    (repo / "docs" / "notes.md").write_text("[ok](extra.md) [bad](missing.md)")
    result = run(repo)   # extra.md resolves from docs/, missing.md doesn't exist anywhere
    assert result.returncode == 1
    assert "missing.md" in result.stdout and "extra.md" not in result.stdout


def test_structure_listing_missing_path_fails(tmp_path):
    repo = make_repo(tmp_path)
    (repo / "topics" / "alpha.md").unlink()
    (repo / "topics" / "gamma.md").write_text("x")     # keep topic tables valid?  no —
    # alpha is in both the Topics table and the Structure block; removing it must fail
    result = run(repo)
    assert result.returncode == 1
