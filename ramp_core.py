#!/usr/bin/env python3
"""ramp_core — the single source of truth for ramp's deterministic pedagogy.

XP weights, the spaced-repetition interval ladder, tree validation, file
locking, and the frontmatter/review-field writers all live here. Imported by
BOTH scripts/skill-observer.py (system python3 hook) and mcp/server.py (.venv
MCP server) so the two can never disagree. STDLIB-ONLY — the hook runs under a
python3 with no .venv, so no third-party imports, ever.
"""
import os
import re
from contextlib import contextmanager
from datetime import date, timedelta
from pathlib import Path

try:
    import fcntl  # POSIX only; the cross-process write lock
except ImportError:  # pragma: no cover - non-POSIX fallback
    fcntl = None

# --- constants: the single definition of these values in the codebase ---
BRANCH_XP = {"ROOT": 10, "A": 15, "B": 20, "C": 25, "D": 35, "E": 50}
SR_LADDER = {1: 1, 2: 3, 3: 7, 4: 21, 5: 60, 6: None}  # interval days; None = permanent

# A branch header in EITHER form: "## [SubTopic · TIER]" or "## [TIER]".
# The optional "[^\]]*·\s*" group consumes a subtopic label + middot if present
# but never crosses the closing bracket, so "## [Getting Started]" (no tier)
# yields no match and contributes 0 XP.
_HEADER_RE = re.compile(r"^##\s+\[(?:[^\]]*·\s*)?(ROOT|A|B|C|D|E)\]")


def compute_xp(tree: str) -> int:
    """Total XP for a tree. [✓] = full branch weight, [~] = half (floor), else 0.

    Format-tolerant: accepts both header forms. A branch-like header that yields
    no valid TIER contributes 0 here and is surfaced separately by validate_tree.
    """
    xp = 0
    current = 0
    for line in tree.splitlines():
        if line.startswith("## ["):
            m = _HEADER_RE.match(line)
            current = BRANCH_XP.get(m.group(1), 0) if m else 0
        else:
            s = line.strip()
            if s.startswith("- [✓"):
                xp += current
            elif s.startswith("- [~"):
                xp += current // 2
    return xp


# A review schedule field: "| next: YYYY-MM-DD [LN]" (date must be zero-padded).
_REVIEW_RE = re.compile(r"\|\s*next:\s*(\d{4}-\d{2}-\d{2})\s*\[L(\d)\]")


def is_valid_iso_date(s: str) -> bool:
    """True only for a real, zero-padded YYYY-MM-DD calendar date."""
    if not isinstance(s, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return False
    try:
        date.fromisoformat(s)
        return True
    except ValueError:
        return False


def next_review_date(level: int, today: date):
    """today + the ladder interval for `level`, as an ISO string; None at L6."""
    days = SR_LADDER.get(level)
    if days is None:
        return None
    return (today + timedelta(days=days)).isoformat()


def advance_level(level: int) -> int:
    return min(level + 1, 6)


def reset_level() -> int:
    return 1


def parse_review_field(line: str):
    """Extract (date, level) from a node line's '| next: D [LN]' field, or None."""
    m = _REVIEW_RE.search(line)
    if not m or not is_valid_iso_date(m.group(1)):
        return None
    return (date.fromisoformat(m.group(1)), int(m.group(2)))


_NODE_NAME_RE = re.compile(r"-\s*\[[^\]]*\]\s*(.+?)(?:\s*—|\s*\|\s*next:|$)")


def node_name(line: str):
    """The node's name: text after the status marker, before evidence or schedule."""
    m = _NODE_NAME_RE.match(line.strip())
    return m.group(1).strip() if m else None


def validate_tree(tree: str) -> list:
    """Return a list of human-readable problems; empty list means clean.

    Checks: branch-like headers with no valid TIER; [✓] nodes whose next: date
    is malformed or absent; duplicate node names; frontmatter xp: disagreeing
    with compute_xp. Never mutates the tree.
    """
    problems = []
    seen = {}
    declared_xp = None
    in_front = False
    front_seen = False
    for lineno, line in enumerate(tree.splitlines(), 1):
        stripped = line.strip()
        if stripped == "---":
            if not in_front and not front_seen:
                in_front = True
            elif in_front:
                in_front = False
                front_seen = True
            continue
        if in_front:
            m = re.match(r"^xp:\s*(.+)$", stripped)
            if m:
                try:
                    declared_xp = int(m.group(1))
                except ValueError:
                    problems.append(f"line {lineno}: xp: {m.group(1)!r} is not an integer")
            continue
        if line.startswith("## ["):
            if not _HEADER_RE.match(line):
                problems.append(f"line {lineno}: branch header has no valid TIER: {stripped!r}")
            continue
        if stripped.startswith("- ["):
            name = node_name(line) or stripped
            if name in seen:
                problems.append(f"line {lineno}: duplicate node name: {name!r}")
            else:
                seen[name] = lineno
            if stripped.startswith("- [✓"):
                rev = _REVIEW_RE.search(stripped)
                if rev is None:
                    if "next:" in stripped:
                        problems.append(f"line {lineno}: malformed review field on [✓] node {name!r}")
                    else:
                        problems.append(f"line {lineno}: [✓] node missing next: review field: {name!r}")
                elif not is_valid_iso_date(rev.group(1)):
                    problems.append(f"line {lineno}: invalid review date {rev.group(1)} on node {name!r}")
    if declared_xp is not None:
        actual = compute_xp(tree)
        if declared_xp != actual:
            problems.append(f"frontmatter xp: {declared_xp} disagrees with computed xp: {actual}")
    return problems


@contextmanager
def file_lock(path):
    """Exclusive cross-process lock for a graph read-modify-write.

    Serializes concurrent writers (the observer may fire in two scopes; the MCP
    server writes too). No-op fallback off-POSIX (fcntl absent).
    """
    if fcntl is None:
        yield None
        return
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = open(path, "w")
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield fd
    finally:
        try:
            fcntl.flock(fd, fcntl.LOCK_UN)
        finally:
            fd.close()


def _preserve_trailing_newline(original: str, lines: list) -> str:
    return "\n".join(lines) + ("\n" if original.endswith("\n") else "")


def apply_frontmatter(tree: str, today: date) -> str:
    """Recompute the xp: field and set updated: to today, in YAML frontmatter."""
    new_xp = compute_xp(tree)
    lines = tree.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("updated:"):
            lines[i] = f"updated: {today.isoformat()}"
        elif line.startswith("xp:"):
            lines[i] = f"xp: {new_xp}"
    return _preserve_trailing_newline(tree, lines)


def set_review_field(line: str, date_str, level: int) -> str:
    """Replace (or append) the '| next: ...' field on a node line."""
    base = re.sub(r"\s*\|\s*next:.*$", "", line.rstrip())
    if date_str is None:  # L6 permanent — a non-date value never matches the due-filter
        return f"{base} | next: permanent [L6]"
    return f"{base} | next: {date_str} [L{level}]"


def fill_missing_review_dates(tree: str, today: date):
    """Add '| next: <L1 date> [L1]' to any [✓] node that has NO next: field.

    A *malformed* next: date is left untouched (validate_tree flags it; its real
    value is unknowable — see spec §9). Returns (new_tree, filled_node_names).
    """
    filled = []
    lines = tree.splitlines()
    for i, line in enumerate(lines):
        if not line.strip().startswith("- [✓"):
            continue
        if _REVIEW_RE.search(line) or "next:" in line:
            continue  # valid (skip) or malformed (leave for validate_tree)
        lines[i] = set_review_field(line, next_review_date(1, today), 1)
        filled.append(node_name(line) or "?")
    return _preserve_trailing_newline(tree, lines), filled


def preserve_demonstrated(existing: str, incoming: str):
    """Never-downgrade: if a node is [✓] on disk, keep that line in `incoming`.

    Returns (new_incoming, preserved_node_names). Matches nodes by name.
    """
    done = {}
    for line in existing.splitlines():
        if line.strip().startswith("- [✓"):
            k = node_name(line)
            if k:
                done[k] = line
    preserved = []
    out = []
    for line in incoming.splitlines():
        s = line.strip()
        if s.startswith("- [") and not s.startswith("- [✓"):
            k = node_name(line)
            if k and k in done:
                out.append(done[k])  # restore the demonstrated line verbatim
                preserved.append(k)
                continue
        out.append(line)
    return _preserve_trailing_newline(incoming, out), preserved
