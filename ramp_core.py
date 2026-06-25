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


# ---------------------------------------------------------------------------
# Read/summary layer — the read analog of the write kernel above. Pure parses;
# nothing here mutates or writes. summarize_graph / schema_node_count /
# list_catalog are the single source of read truth, consumed by the list/help
# viewers (and, in the deferred tail, tree). STDLIB-ONLY like the rest.
# ---------------------------------------------------------------------------

def parse_frontmatter(content: str) -> dict:
    """Minimal YAML-ish frontmatter -> {field: str}. Empty dict if no block."""
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    out = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            out[m.group(1)] = m.group(2).strip()
    return out


# A node bullet's status marker: "- [<status>]" or "- [<status>|<type>]".
_STATUS_RE = re.compile(r"-\s*\[([^\]|]*)(?:\|([^\]]*))?\]")
# Raw marker char -> normalized token. "" and " " are an unchecked box: todo.
_STATUS_TOKENS = {
    "✓": "done", "~": "reported", "": "todo", " ": "todo",
    "·": "locked", "★": "todo",  # ★ frontier target still un-demonstrated -> todo
}


def _node_status_type(line: str):
    """(token, type) for a node bullet, or (None, None) if the line isn't one."""
    m = _STATUS_RE.match(line.strip())
    if not m:
        return None, None
    token = _STATUS_TOKENS.get(m.group(1).strip(), "todo")
    typ = m.group(2).strip() if m.group(2) else None
    return token, typ


def summarize_graph(content: str, today: date = None) -> dict:
    """One tree -> {level, xp, due, counts:{done,reported,todo,locked}}.

    xp via compute_xp (deterministic recompute, matches the write path). due =
    [✓] nodes whose next: date is valid AND <= today; a malformed or absent date
    is never counted due (the unit-1 "flag, don't fabricate" rule, read side).
    """
    if today is None:
        today = date.today()
    fm = parse_frontmatter(content)
    counts = {"done": 0, "reported": 0, "todo": 0, "locked": 0}
    due = 0
    for line in content.splitlines():
        if not line.strip().startswith("- ["):
            continue
        token, _ = _node_status_type(line)
        if token in counts:
            counts[token] += 1
        if token == "done":
            parsed = parse_review_field(line)  # None if malformed/absent
            if parsed and parsed[0] <= today:
                due += 1
    return {
        "level": fm.get("level", "unknown"),
        "xp": compute_xp(content),
        "due": due,
        "counts": counts,
    }


def _derived_node_count(content: str) -> int:
    """Count node-definition rows inside the schema's `## Node definitions`
    section. Schemas enumerate nodes as a markdown table (one row per node,
    grouped under `### [TIER]` subheadings), so count table *data* rows: lines
    that start with `|` whose first cell is non-empty, isn't the `Node` header,
    and isn't a `|---|` alignment separator. Excludes the saved-tree template
    (a different `##` section) and the `### [TIER] … (N nodes)` prose subheaders
    (which start with `###`, not `## `, so they don't reset the section flag)."""
    count = 0
    in_defs = False
    for line in content.splitlines():
        if line.startswith("## "):
            in_defs = line.strip().lower().startswith("## node definitions")
            continue
        if not in_defs:
            continue
        s = line.strip()
        if not s.startswith("|"):
            continue
        first = s.strip("|").split("|")[0].strip()
        if not first or first.lower() == "node" or set(first) <= {"-", ":"}:
            continue
        count += 1
    return count


def schema_node_count(content: str) -> int:
    """Authoritative node count for a topic schema: the `node_count:` frontmatter
    field when a valid int, else the derived count (`_derived_node_count`, which
    scopes to `## Node definitions` and excludes the saved-tree template)."""
    fm = parse_frontmatter(content)
    if "node_count" in fm:
        try:
            return int(fm["node_count"])
        except ValueError:
            pass
    return _derived_node_count(content)


def _parse_sources(value: str) -> list:
    """'[a, b, c]' or 'a, b' -> ['a','b','c']; '' -> []."""
    inner = value.strip().strip("[]")
    return [s.strip() for s in inner.split(",") if s.strip()]


def list_catalog(schema_dir, graph_dir, today: date) -> list:
    """catalog (schema_dir/*.md) LEFT-JOIN progress (graph_dir/{name}.md),
    keyed by topic name. Personal layer only. Returns dicts sorted by name."""
    schema_dir = Path(schema_dir)
    graph_dir = Path(graph_dir)
    schemas = {}  # name -> (frontmatter dict, raw content)
    for path in sorted(schema_dir.glob("*.md")):
        try:
            content = path.read_text(encoding="utf-8")
        except OSError:
            continue  # skip unreadable entries (broken symlink, dir, perms) —
            #          a read-only viewer never crashes the catalog over one file
        schemas[path.stem] = (parse_frontmatter(content), content)

    # which names are claimed as a sub-topic by some composite's sources:
    sub_names = set()
    for fm, _ in schemas.values():
        if "sources" in fm:
            sub_names.update(_parse_sources(fm["sources"]))

    catalog = []
    for name in sorted(schemas):
        fm, content = schemas[name]
        sources = _parse_sources(fm["sources"]) if "sources" in fm else None
        if sources is not None:
            group = "core"
        elif name in sub_names:
            group = "sub"
        else:
            group = "standalone"
        graph_path = graph_dir / f"{name}.md"
        started = graph_path.exists()
        summary = (
            summarize_graph(graph_path.read_text(encoding="utf-8"), today)
            if started else None
        )
        catalog.append({
            "name": name,
            "description": fm.get("description", ""),
            "node_count": schema_node_count(content),
            "group": group,
            "sources": sources,
            "started": started,
            "summary": summary,
        })
    return catalog


# ---------------------------------------------------------------------------
# CLI shim — the no-MCP read path. Emits JSON data; the prompts render layout.
# Guarded so importing the module (observer, MCP server) never runs this.
# MVP verbs: catalog, summary. (The `nodes` verb + graph_nodes are the deferred
# tail — added with the tree migration.)
# ---------------------------------------------------------------------------

def _graph_dir() -> Path:
    return Path.home() / ".claude" / "knowledge-graphs"


def _schema_dir() -> Path:
    """First existing schema dir by precedence: project-local, global, plugin."""
    candidates = [
        Path(".claude/knowledge-graphs/schemas"),
        Path.home() / ".claude" / "knowledge-graphs" / "schemas",
    ]
    root = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if root:
        candidates.append(Path(root) / "topics")
    for c in candidates:
        if c.is_dir() and any(c.glob("*.md")):
            return c
    return candidates[-1] if candidates else Path("topics")


def _main(argv) -> int:
    import argparse
    import json

    parser = argparse.ArgumentParser(prog="ramp_core")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("catalog")
    p_sum = sub.add_parser("summary")
    p_sum.add_argument("topic")
    args = parser.parse_args(argv)

    if args.cmd == "catalog":
        data = list_catalog(_schema_dir(), _graph_dir(), date.today())
        print(json.dumps(data))
        return 0

    # args.cmd == "summary"
    graph_path = _graph_dir() / f"{args.topic}.md"
    if not graph_path.exists():
        print(json.dumps({}))
        return 0
    content = graph_path.read_text(encoding="utf-8")
    print(json.dumps(summarize_graph(content, date.today())))
    return 0


if __name__ == "__main__":
    import sys as _sys
    raise SystemExit(_main(_sys.argv[1:]))
