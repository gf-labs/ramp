#!/usr/bin/env python3
r"""Docs-consistency gate: README tables/badges, CLAUDE.md structure listing, links.

Checks (all mechanical; prose truthfulness is out of scope):
  1. Every `commands/*.md` has a `| \`/ramp:` row in README "## The commands" — and
     every row has a file.
  2. Every backticked topic row in README "## Topics" has `topics/<name>.md`, and the
     `topics-N` badge equals the row count. (The `*(your topic)*` row has no backtick
     and is skipped — sub-topic schemas are internal detail, per docs-standard.md.)
  3. Every path token in CLAUDE.md's "## Structure" code block exists.
  4. Every relative link in README.md, GETTING-STARTED.md, and docs/*.md resolves —
     each checked relative to its containing file's directory.

Parsing contract: rows are identified by their first-cell backtick token under the
section heading; cosmetic prose edits are safe, adding/removing rows or files is caught.
"""
import argparse
import re
import sys
from pathlib import Path


def section(text, heading):
    """Return the text between `heading` and the next '## ' heading (or EOF)."""
    m = re.search(r"^" + re.escape(heading) + r"\s*$(.*?)(?=^## |\Z)",
                  text, re.M | re.S)
    return m.group(1) if m else ""


def check_commands(repo, readme, problems):
    rows = set(re.findall(r"^\|\s*`/ramp:([a-z-]+)", section(readme, "## The commands"), re.M))
    files = {p.stem for p in (repo / "commands").glob("*.md")}
    for missing_row in sorted(files - rows):
        problems.append(f"command file with no README table row: commands/{missing_row}.md")
    for missing_file in sorted(rows - files):
        problems.append(f"README command row with no file: /ramp:{missing_file}")


def check_topics(repo, readme, problems):
    rows = re.findall(r"^\|\s*`([a-z-]+)`", section(readme, "## Topics"), re.M)
    for name in rows:
        if not (repo / "topics" / (name + ".md")).exists():
            problems.append(f"README topic row with no schema: topics/{name}.md ({name})")
    badge = re.search(r"badge/topics-(\d+)-", readme)
    if badge and int(badge.group(1)) != len(rows):
        problems.append(f"topics badge says {badge.group(1)} but the Topics table has {len(rows)} rows")


def check_structure_listing(repo, problems):
    claude = repo / "CLAUDE.md"
    if not claude.exists():
        return
    block = section(claude.read_text(encoding="utf-8"), "## Structure")
    for line in block.splitlines():
        m = re.match(r"^([A-Za-z0-9_.\-/]+?)\s{2,}#", line.strip())
        if not m:
            continue
        token = m.group(1)
        if not (repo / token).exists():
            problems.append(f"CLAUDE.md Structure lists a missing path: {token}")


def check_links(repo, problems):
    docs = [repo / "README.md", repo / "GETTING-STARTED.md"]
    docs += sorted((repo / "docs").glob("*.md"))
    for doc in docs:
        if not doc.exists():
            continue
        text = doc.read_text(encoding="utf-8")
        for target in re.findall(r"\]\((?!https?://|#|mailto:)([^)\s]+)\)", text):
            path = target.split("#")[0]
            if path and not (doc.parent / path).exists():
                problems.append(f"{doc.name} links to a missing path: {target}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", default=".", help="repo root (default: cwd)")
    repo = Path(ap.parse_args().repo).resolve()
    readme = (repo / "README.md").read_text(encoding="utf-8")

    problems = []
    check_commands(repo, readme, problems)
    check_topics(repo, readme, problems)
    check_structure_listing(repo, problems)
    check_links(repo, problems)

    if problems:
        print(f"check-docs: {len(problems)} problem(s)")
        for p in problems:
            print("  - " + p)
        return 1
    print("check-docs: OK (commands, topics badge, structure listing, links)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
