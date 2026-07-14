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
import sys
import glob as _glob
import json as _json
import shlex
import subprocess
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

# Supported Python floor. The kernel is stdlib-only and uses nothing past 3.7
# (date.fromisoformat); 3.8 is declared as the floor, enforced by the CLI guard
# in _main, and mirrored by the README badge (locked by a test). The import path
# (observer hook, MCP server) is deliberately NOT guarded — those run best-effort
# under the host's python3 and must never hard-crash a session.
MIN_PYTHON = (3, 8)


def python_version_error(info=None):
    """A one-line error if the running Python is older than MIN_PYTHON, else None.

    Pure (accepts a version_info tuple) so the contract is unit-testable without
    spawning an interpreter.
    """
    info = sys.version_info if info is None else info
    if tuple(info[:2]) < MIN_PYTHON:
        return f"ramp needs Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ (found {info[0]}.{info[1]})."
    return None

# A branch header in EITHER form: "## [SubTopic · TIER]" or "## [TIER]".
# The optional "[^\]]*·\s*" group consumes a subtopic label + middot if present
# but never crosses the closing bracket, so "## [Getting Started]" (no tier)
# yields no match and contributes 0 XP.
_HEADER_RE = re.compile(r"^##\s+\[(?:[^\]]*·\s*)?(ROOT|A|B|C|D|E)\]")


def compute_xp(tree: str) -> int:
    """Total XP for a tree. [✓] = full branch weight, [~] = half (floor), else 0.

    Format-tolerant: accepts both header forms. A branch-like header that yields
    no valid TIER contributes 0 here and is surfaced separately by validate_tree.
    A node NAME that appears more than once counts once, at its first
    occurrence's tier — a misfiled duplicate can't inflate XP (validate_tree
    still flags it for repair). Unnamed bullets are never deduped.
    """
    xp = 0
    current = 0
    seen = set()
    for line in tree.splitlines():
        if line.startswith("## ["):
            m = _HEADER_RE.match(line)
            current = BRANCH_XP.get(m.group(1), 0) if m else 0
            continue
        s = line.strip()
        if not (s.startswith("- [✓") or s.startswith("- [~")):
            continue
        name = node_name(s)
        if name is not None:
            if name in seen:
                continue
            seen.add(name)
        xp += current if s.startswith("- [✓") else current // 2
    return xp


# A review schedule field: "| next: YYYY-MM-DD [LN]" (date must be zero-padded).
_REVIEW_RE = re.compile(r"\|\s*next:\s*(\d{4}-\d{2}-\d{2})\s*\[L(\d)\]")

# The retired form of the field: "| next: permanent [LN]" — no date, but the
# level is real and must be honored (an L6 node can't re-enter the SR cycle).
_PERMANENT_RE = re.compile(r"\|\s*next:\s*permanent\s*\[L(\d)\]")


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


def _node_evidence(line: str):
    """The evidence trail after the node name ('— repo, date: note'), with the
    '| next:' schedule suffix removed. None when the node carries no trail."""
    m = _STATUS_RE.match(line.strip())
    if not m:
        return None
    after = line.strip()[m.end():].split("| next:")[0]
    if "—" not in after:
        return None
    return after.split("—", 1)[1].strip() or None


def graph_nodes(content: str) -> list:
    """One tree -> per-node dicts for the deep (tree) render. Pure parse; the
    stored status is read verbatim, never recomputed.

    `branch` is the tier letter (the XP weight); `section` is the full `## [...]`
    header text the node sits under. The real graph has several sections sharing
    a tier (5 ROOT sections, etc.), so the tier alone cannot reconstruct the
    tree — the tree view groups by `section`.
    """
    nodes = []
    branch = None
    section = None
    for line in content.splitlines():
        if line.startswith("## ["):
            m = _HEADER_RE.match(line)
            branch = m.group(1) if m else None
            section = line.strip()[3:].strip()  # the header text after "## "
            continue
        if not line.strip().startswith("- ["):
            continue
        token, typ = _node_status_type(line)
        weight = BRANCH_XP.get(branch, 0)
        if token == "done":
            xp = weight
        elif token == "reported":
            xp = weight // 2
        else:
            xp = 0
        parsed = parse_review_field(line)
        marker = _STATUS_RE.match(line.strip())
        nodes.append({
            "name": node_name(line),
            "status": token,
            "type": typ,
            "xp": xp,
            "branch": branch,
            "section": section,
            "next_date": parsed[0].isoformat() if parsed else None,
            "level": parsed[1] if parsed else None,
            "evidence": _node_evidence(line),
            "target": bool(marker) and marker.group(1).strip() == "★",
        })
    return nodes


def due_nodes(content: str, today: date = None) -> list:
    """graph_nodes filtered to the SR queue: [✓] nodes whose next: date is valid
    and <= today. Malformed, absent, or 'permanent' fields are never due — the
    same "flag, don't fabricate" rule as summarize_graph, so the two can't
    disagree. This is the single source review.md renders its queue from."""
    if today is None:
        today = date.today()
    cutoff = today.isoformat()
    return [
        n for n in graph_nodes(content)
        if n["status"] == "done" and n["next_date"] and n["next_date"] <= cutoff
    ]


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
# Detection probe layer — the topic-driven half of environment detection.
# up.md used to hardcode ~15 Claude-Code-specific !bash scans; those move into
# each schema's `## Probes` table, wiring probe NAMES to these declarative,
# read-only primitives. `detect <topic>` runs the active topic's probes and
# emits the name=value evidence block Phase 2 Step 1 reads. STDLIB-ONLY.
# Every primitive degrades to its zero value on error — detection is
# best-effort, matching the old scans' `2>/dev/null || echo 0`.
# ---------------------------------------------------------------------------

def _probe_file_exists(path: str) -> bool:
    return Path(os.path.expanduser(path)).exists()


def _probe_file_lines(path: str) -> int:
    try:
        with Path(os.path.expanduser(path)).open("r", encoding="utf-8", errors="replace") as fh:
            return sum(1 for _ in fh)
    except OSError:
        return 0


def _probe_glob_count(pattern: str, exclude: str = None) -> int:
    hits = set(_glob.glob(os.path.expanduser(pattern), recursive=True))
    if exclude:
        hits -= set(_glob.glob(os.path.expanduser(exclude), recursive=True))
    return len(hits)


def _probe_dir_count(path: str) -> int:
    try:
        return sum(1 for _ in Path(os.path.expanduser(path)).iterdir())
    except OSError:
        return 0


def _json_load(path: str):
    try:
        return _json.loads(Path(os.path.expanduser(path)).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _dotted_get(obj, dotted: str):
    cur = obj
    for key in dotted.split("."):
        if isinstance(cur, dict) and key in cur:
            cur = cur[key]
        else:
            return None
    return cur


def _probe_json_has_key(path: str, dotted: str) -> bool:
    val = _dotted_get(_json_load(path), dotted)
    return val is not None and val != {} and val != []


def _probe_json_value(path: str, dotted: str):
    return _dotted_get(_json_load(path), dotted)


def _iter_files(base: Path):
    if base.is_dir():
        for f in base.rglob("*"):
            if f.is_file():
                yield f
    elif base.is_file():
        yield base


def _probe_grep_count(regex: str, paths) -> int:
    try:
        rx = re.compile(regex)
    except re.error:
        return 0
    count = 0
    for base in paths:
        for f in _iter_files(Path(os.path.expanduser(base))):
            try:
                with f.open("r", encoding="utf-8", errors="replace") as fh:
                    count += sum(1 for line in fh if rx.search(line))
            except OSError:
                continue
    return count


def _git(args) -> str:
    """git stdout on success, '' on any failure (not a repo, git absent)."""
    try:
        out = subprocess.run(["git"] + list(args), capture_output=True, text=True, timeout=10)
        return out.stdout if out.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""


def _probe_git_log_grep(regex: str, diff_filter: str = None, path: str = None) -> int:
    if diff_filter:
        # count ADDED file paths (across all history) whose name matches regex
        args = ["log", "--all", "--diff-filter=" + diff_filter, "--name-only", "--pretty=format:"]
        if path:
            args += ["--", path]
        try:
            rx = re.compile(regex)
        except re.error:
            return 0
        return sum(1 for ln in _git(args).splitlines() if ln.strip() and rx.search(ln))
    # count COMMITS whose message matches regex (extended-regex --grep)
    out = _git(["log", "--all", "--oneline", "-E", "--grep", regex])
    return sum(1 for ln in out.splitlines() if ln.strip())


def _probe_git_worktree_count() -> int:
    return sum(1 for ln in _git(["worktree", "list"]).splitlines() if ln.strip())


def _probe_git_max_commit_files(n: int = 10) -> int:
    """Max files touched in any of the last n commits, read from `git log
    --stat` summary lines (' N files changed, ...'). 0 on no history / not a
    repo. Replaces up.md's legacy shell pipe with no shell."""
    best = 0
    for ln in _git(["log", "--stat", "--oneline", "-" + str(n)]).splitlines():
        m = re.match(r"\s+(\d+) files? changed", ln)
        if m:
            best = max(best, int(m.group(1)))
    return best


def run_probe(primitive: str, arg_str: str):
    """Dispatch a single probe. `arg_str` is the raw args cell from the schema
    table (pipes already unescaped by parse_probes). All primitives are
    read-only and shell-free; each degrades to its zero value on error."""
    try:
        toks = shlex.split(arg_str) if arg_str else []
    except ValueError:
        toks = []
    if primitive == "file-exists":
        return _probe_file_exists(toks[0]) if toks else False
    if primitive == "file-lines":
        return _probe_file_lines(toks[0]) if toks else 0
    if primitive == "glob-count":
        exclude, pos, i = None, [], 0
        while i < len(toks):
            if toks[i] == "--exclude" and i + 1 < len(toks):
                exclude = toks[i + 1]; i += 2
            else:
                pos.append(toks[i]); i += 1
        return _probe_glob_count(pos[0], exclude) if pos else 0
    if primitive == "dir-count":
        return _probe_dir_count(toks[0]) if toks else 0
    if primitive == "json-has-key":
        return _probe_json_has_key(toks[0], toks[1]) if len(toks) >= 2 else False
    if primitive == "json-value":
        return _probe_json_value(toks[0], toks[1]) if len(toks) >= 2 else None
    if primitive == "grep-count":
        return _probe_grep_count(toks[0], toks[1:]) if toks else 0
    if primitive == "git-log-grep":
        diff_filter, path, pos, i = None, None, [], 0
        while i < len(toks):
            if toks[i].startswith("--diff-filter="):
                diff_filter = toks[i].split("=", 1)[1]; i += 1
            elif toks[i] == "--diff-filter" and i + 1 < len(toks):
                diff_filter = toks[i + 1]; i += 2
            elif toks[i] == "--path" and i + 1 < len(toks):
                path = toks[i + 1]; i += 2
            else:
                pos.append(toks[i]); i += 1
        return _probe_git_log_grep(pos[0], diff_filter, path) if pos else 0
    if primitive == "git-worktree-count":
        return _probe_git_worktree_count()
    if primitive == "git-max-commit-files":
        try:
            n = int(toks[0]) if toks else 10
        except ValueError:
            n = 10
        return _probe_git_max_commit_files(n)
    return "UNKNOWN_PRIMITIVE:" + primitive


def parse_probes(content: str) -> list:
    """A schema's `## Probes` table -> [(name, primitive, args)].

    Rows are `| name | primitive | args |`. Header (`name`) and `|---|`
    separator rows are skipped. A `\\|` inside the args cell is a literal pipe
    (markdown escaping) and is restored; an em-dash args cell means "no args"
    -> empty string. Scoped strictly to the `## Probes` section."""
    rows = []
    in_probes = False
    for line in content.splitlines():
        if line.startswith("## "):
            in_probes = line.strip().lower().startswith("## probes")
            continue
        if not in_probes:
            continue
        s = line.strip()
        if not s.startswith("|"):
            continue
        raw = s.strip("|").replace("\\|", "\x00")  # protect escaped pipes
        cells = [c.replace("\x00", "|").strip() for c in raw.split("|")]
        if len(cells) < 3:
            continue
        name, primitive, args = cells[0], cells[1], cells[2]
        if not name or name.lower() == "name" or set(name) <= {"-", ":"}:
            continue
        rows.append((name, primitive, "" if args == "—" else args))
    return rows


def load_topic_probes(topic: str, schema_dir):
    """Union the topic's own `## Probes` with those of its `sources:` sub-schemas.
    First declaration of a probe name wins (compute_xp's dedup rule). Returns
    {name: (primitive, args)}."""
    schema_dir = Path(schema_dir)

    def read(name):
        try:
            return (schema_dir / (name + ".md")).read_text(encoding="utf-8")
        except OSError:
            return ""

    fm = parse_frontmatter(read(topic))
    names = [topic] + (_parse_sources(fm["sources"]) if "sources" in fm else [])
    probes = {}
    for n in names:
        for pname, primitive, args in parse_probes(read(n)):
            probes.setdefault(pname, (primitive, args))  # first wins
    return probes


def run_detection(topic: str, schema_dir=None) -> dict:
    """Run every probe the active topic declares (own + sourced), returning
    {name: value}. Insertion order follows first-declaration order."""
    schema_dir = _schema_dir() if schema_dir is None else Path(schema_dir)
    probes = load_topic_probes(topic, schema_dir)
    return {
        name: run_probe(primitive, args)
        for name, (primitive, args) in probes.items()
    }


def _fmt_value(v) -> str:
    if isinstance(v, bool):  # bool before int — bool is an int subclass
        return "true" if v else "false"
    if v is None:
        return "none"
    return str(v)


def format_detection(result: dict) -> str:
    """The name=value evidence block up.md injects. One line per probe."""
    return "\n".join(f"{name}={_fmt_value(val)}" for name, val in result.items())


# ---------------------------------------------------------------------------
# CLI shim — the no-MCP path. Read verbs emit JSON data (the prompts render
# layout); the save verb is the validated writer, full tree on stdin. Guarded
# so importing the module (observer, MCP server) never runs this. Verbs:
# catalog, summary, nodes, save. (summary -> summarize_graph; nodes ->
# graph_nodes, the deep per-node read; save -> save_graph, exit 2 on REJECTED.)
# ---------------------------------------------------------------------------

def _graph_dir() -> Path:
    return Path.home() / ".claude" / "ramp" / "graphs"


def _schema_dir() -> Path:
    """First existing schema dir by precedence: project-local, global, plugin.

    Only the global home moved to ~/.claude/ramp/ (the workspace+legibility
    slice); the project-local team path stays .claude/knowledge-graphs/schemas
    until the team layer lands (its own migration)."""
    candidates = [
        Path(".claude/knowledge-graphs/schemas"),
        Path.home() / ".claude" / "ramp" / "schemas",
    ]
    root = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if root:
        candidates.append(Path(root) / "topics")
    for c in candidates:
        if c.is_dir() and any(c.glob("*.md")):
            return c
    return candidates[-1] if candidates else Path("topics")


def migrate_graph_home() -> bool:
    """One-time, idempotent copy of legacy ~/.claude/knowledge-graphs/*.md into
    the ~/.claude/ramp/graphs/ home. Never clobbers an existing new-home file;
    leaves the legacy dir in place as a one-release backup. Schemas are
    observer-provisioned symlinks, not copied. Returns True iff it copied at
    least one file. Called best-effort from the observer's SessionStart, never
    from the read path."""
    legacy = Path.home() / ".claude" / "knowledge-graphs"
    if not legacy.is_dir():
        return False
    new_graphs = _graph_dir()
    new_graphs.mkdir(parents=True, exist_ok=True)
    copied = False
    for src in sorted(legacy.glob("*.md")):
        dst = new_graphs / src.name
        if dst.exists():
            continue
        try:
            # bytes, not text: a non-UTF-8 legacy file must copy, not abort the sweep
            dst.write_bytes(src.read_bytes())
        except OSError:
            continue
        copied = True
    return copied


# ---------------------------------------------------------------------------
# Write path — the canonical validated writer. Kernel-owned: the MCP server's
# save_graph tool delegates here, and the CLI `save` verb exposes the same
# writer on no-MCP installs, so XP/SR invariants hold on every install.
# ---------------------------------------------------------------------------

def _atomic_write(path, content: str) -> None:
    """Write atomically: temp file in the same dir, then os.replace. A partial
    write can never leave a graph truncated, even under concurrent fires (the
    observer and the MCP server may both write)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(f".md.tmp.{os.getpid()}")
    try:
        tmp.write_text(content, encoding="utf-8")
        os.replace(tmp, path)
    except Exception:
        tmp.unlink(missing_ok=True)
        raise


def save_graph(topic: str, content: str, graph_dir=None) -> str:
    """Save a full tree for `topic` — the single validated write composition.

    Gate on frontmatter (REJECTED, no write) -> preserve_demonstrated against
    the on-disk file (never-downgrade) -> fill_missing_review_dates (L1-seed
    MISSING next: fields only) -> validate_tree (flag, don't fabricate) ->
    apply_frontmatter (xp:/updated: recomputed in code) -> file_lock + atomic
    write. Returns 'saved · {topic} · {level} · {xp} XP → {path}' plus any
    notes and a '⚠ problems' suffix. `graph_dir` overrides the personal home
    (the MCP server passes its GRAPH_DIR through; tests isolate via it)."""
    graph_dir = _graph_dir() if graph_dir is None else Path(graph_dir)
    path = graph_dir / f"{topic}.md"
    if not parse_frontmatter(content):
        return "REJECTED: content has no YAML frontmatter — refusing to write"

    today = date.today()
    notes = []
    if path.exists():
        content, preserved = preserve_demonstrated(
            path.read_text(encoding="utf-8"), content
        )
        if preserved:
            notes.append(f"preserved {len(preserved)} on-disk [✓]: {', '.join(preserved)}")

    content, filled = fill_missing_review_dates(content, today)
    if filled:
        notes.append(f"filled next: on {len(filled)}: {', '.join(filled)}")

    problems = validate_tree(content)
    content = apply_frontmatter(content, today)

    with file_lock(graph_dir / f".{topic}.md.lock"):
        _atomic_write(path, content)

    fm = parse_frontmatter(content)
    level = fm.get("level", "unknown")
    try:
        xp = int(fm.get("xp", "0"))
    except (TypeError, ValueError):
        xp = 0
    msg = f"saved · {topic} · {level} · {xp} XP → {path}"
    if notes:
        msg += " · " + " · ".join(notes)
    if problems:
        msg += " · ⚠ " + "; ".join(problems)
    return msg


def advance_review(topic: str, node: str, outcome: str, graph_dir=None) -> str:
    """Advance (pass) or reset (fail) a [✓] node's SR schedule — the single
    review-write composition, shared by the MCP tool and the CLI `advance` verb.

    Matches the node EXACTLY by name (never a substring — advancing "Recursion"
    must not touch "Recursion basics"). All level/date math is the ladder above;
    xp: is recomputed by apply_frontmatter (an SR pass changes no status, so XP
    is unchanged). Writes atomically under the graph lock."""
    if outcome not in ("pass", "fail"):
        return f"Invalid outcome {outcome!r} — use 'pass' or 'fail'"
    graph_dir = _graph_dir() if graph_dir is None else Path(graph_dir)
    path = graph_dir / f"{topic}.md"
    if not path.exists():
        return f"NO_TREE_FILE: {topic}"

    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()
    today = date.today()
    found = False
    new_level = new_date = None
    for i, line in enumerate(lines):
        if not line.strip().startswith("- [✓"):
            continue
        if node_name(line) != node:
            continue
        parsed = parse_review_field(line)
        if parsed:
            cur_level = parsed[1]
        else:
            # "permanent [LN]" has no parseable date but a real level — honor it
            # so a pass can't demote L6 back into the cycle. Any other malformed
            # or absent field reads as L1 (the repair path the server tests pin).
            perm = _PERMANENT_RE.search(line)
            cur_level = int(perm.group(1)) if perm else 1
        new_level = advance_level(cur_level) if outcome == "pass" else reset_level()
        new_date = next_review_date(new_level, today)
        lines[i] = set_review_field(line, new_date, new_level)
        found = True
        break
    if not found:
        return f"Node not found or not [✓]: {node!r}"

    new_content = "\n".join(lines) + ("\n" if content.endswith("\n") else "")
    new_content = apply_frontmatter(new_content, today)
    with file_lock(graph_dir / f".{topic}.md.lock"):
        _atomic_write(path, new_content)
    when = new_date if new_date else "permanent"
    return f"advanced · {node} · {outcome} → L{new_level}, next {when}"


def _main(argv) -> int:
    err = python_version_error()
    if err:
        print(err, file=sys.stderr)
        return 2
    import argparse
    import json

    parser = argparse.ArgumentParser(prog="ramp_core")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("catalog")
    p_sum = sub.add_parser("summary")
    p_sum.add_argument("topic")
    p_nodes = sub.add_parser("nodes")
    p_nodes.add_argument("topic")
    p_due = sub.add_parser("due")
    p_due.add_argument("topic")
    p_save = sub.add_parser("save")
    p_save.add_argument("topic")
    p_adv = sub.add_parser("advance")
    p_adv.add_argument("topic")
    p_adv.add_argument("node")
    p_adv.add_argument("outcome", choices=["pass", "fail"])
    p_detect = sub.add_parser("detect")
    p_detect.add_argument("topic")
    args = parser.parse_args(argv)

    if args.cmd == "catalog":
        data = list_catalog(_schema_dir(), _graph_dir(), date.today())
        print(json.dumps(data))
        return 0

    if args.cmd == "save":
        # full tree on stdin; prints the writer's result string
        result = save_graph(args.topic, sys.stdin.read())
        print(result)
        return 2 if result.startswith("REJECTED") else 0

    if args.cmd == "advance":
        result = advance_review(args.topic, args.node, args.outcome)
        print(result)
        return 0 if result.startswith("advanced") else 2

    if args.cmd == "detect":
        print(format_detection(run_detection(args.topic, _schema_dir())))
        return 0

    # args.cmd in ("summary", "nodes", "due") — all read a single topic graph; a
    # missing graph yields the empty shape ({} for summary, [] for nodes/due).
    graph_path = _graph_dir() / f"{args.topic}.md"
    if not graph_path.exists():
        print(json.dumps({} if args.cmd == "summary" else []))
        return 0
    content = graph_path.read_text(encoding="utf-8")
    if args.cmd == "summary":
        print(json.dumps(summarize_graph(content, date.today())))
    elif args.cmd == "due":
        print(json.dumps(due_nodes(content, date.today())))
    else:  # nodes
        print(json.dumps(graph_nodes(content)))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv[1:]))
