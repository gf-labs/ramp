#!/usr/bin/env python3
"""
knowledge-graph MCP server for ramp

Provides structured read/write access to Claude Code knowledge graphs.
Backend: local files at ~/.claude/knowledge-graphs/ by default.
Set KNOWLEDGE_GRAPH_API_URL to proxy reads/writes to a hosted backend,
enabling cross-device sync, team skill matrices, and org analytics.

Quick setup:
  pip install mcp

Register via Claude Code CLI (user scope, persists across all projects):
  claude mcp add -s user knowledge-graph /path/to/ramp/.venv/bin/python3 /path/to/ramp/mcp/server.py

  This is handled automatically by scripts/setup-mcp.py on SessionStart.
  Writes to ~/.claude.json. See .mcp.json.example for reference.

Environment variables:
  KNOWLEDGE_GRAPH_API_URL  If set, read/write proxies to this backend URL.
                          Enables team/org/global benchmark layers.
                          Format: https://your-backend.example.com
"""

import json
import os
import re
import asyncio
from datetime import date, datetime
from pathlib import Path

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    raise SystemExit(
        "mcp package not found.\n"
        "Install with: pip install mcp\n"
        "Or: uv add mcp"
    )

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

GRAPH_DIR = Path.home() / ".claude" / "knowledge-graphs"
API_URL = os.environ.get("KNOWLEDGE_GRAPH_API_URL", "").rstrip("/")
TODAY = date.today().isoformat()

# ---------------------------------------------------------------------------
# Server
# ---------------------------------------------------------------------------

mcp = FastMCP("knowledge-graph")

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter key-value pairs from a tree file."""
    fields: dict = {}
    in_front = False
    for line in content.splitlines():
        stripped = line.strip()
        if stripped == "---":
            if not in_front:
                in_front = True
                continue
            else:
                break
        if in_front:
            m = re.match(r"^(\w+):\s*(.+)$", stripped)
            if m:
                fields[m.group(1)] = m.group(2).strip()
    return fields


def _atomic_write(path: Path, content: str) -> None:
    """Write content atomically via a temp file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    try:
        tmp.write_text(content, encoding="utf-8")
        tmp.rename(path)
    except Exception:
        tmp.unlink(missing_ok=True)
        raise


def _safe_xp(value: str) -> int:
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0

# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool()
def read_graph(topic: str) -> str:
    """
    Read the knowledge graph for a topic.

    Returns the full markdown content of ~/.claude/knowledge-graphs/{topic}.md,
    or 'NO_TREE_FILE' if not found. When KNOWLEDGE_GRAPH_API_URL is set,
    fetches from the remote backend instead (local file is a fallback cache).

    Args:
        topic: Topic name, e.g. 'claude-code', 'best-practices'
    """
    if API_URL:
        try:
            import urllib.request
            req = urllib.request.Request(
                f"{API_URL}/graphs/{topic}",
                headers={"Accept": "text/plain"},
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                return resp.read().decode("utf-8")
        except Exception:
            pass  # Fall through to local file

    path = GRAPH_DIR / f"{topic}.md"
    return path.read_text(encoding="utf-8") if path.exists() else "NO_TREE_FILE"


@mcp.tool()
def save_graph(topic: str, content: str) -> str:
    """
    Save the knowledge graph for a topic.

    Performs an atomic write to ~/.claude/knowledge-graphs/{topic}.md.
    When KNOWLEDGE_GRAPH_API_URL is set, also syncs to the remote backend.
    Returns a confirmation string with topic, level, and XP.

    Args:
        topic:   Topic name, e.g. 'claude-code'
        content: Full markdown content of the graph (version 3 format)
    """
    path = GRAPH_DIR / f"{topic}.md"
    _atomic_write(path, content)

    fm = _parse_frontmatter(content)
    level = fm.get("level", "unknown")
    xp = _safe_xp(fm.get("xp", "0"))

    if API_URL:
        try:
            import urllib.request
            data = content.encode("utf-8")
            req = urllib.request.Request(
                f"{API_URL}/graphs/{topic}",
                data=data,
                method="PUT",
                headers={"Content-Type": "text/plain; charset=utf-8"},
            )
            urllib.request.urlopen(req, timeout=5)
        except Exception as e:
            return f"saved locally · synced to backend failed: {e} · {topic} · {level} · {xp} XP → {path}"

    return f"saved · {topic} · {level} · {xp} XP → {path}"


@mcp.tool()
def list_topics() -> str:
    """
    List all knowledge graph topics with their current level and XP.

    Scans ~/.claude/knowledge-graphs/*.md and extracts frontmatter.
    Returns a JSON array of objects: [{topic, level, xp, updated}].
    """
    if not GRAPH_DIR.exists():
        return json.dumps([])

    topics = []
    for path in sorted(GRAPH_DIR.glob("*.md")):
        try:
            fm = _parse_frontmatter(path.read_text(encoding="utf-8"))
            topics.append({
                "topic": path.stem,
                "level": fm.get("level", "unknown"),
                "xp": _safe_xp(fm.get("xp", "0")),
                "updated": fm.get("updated", ""),
            })
        except Exception:
            continue

    return json.dumps(topics, indent=2)


@mcp.tool()
def get_benchmarks(topic: str) -> str:
    """
    Get peer benchmarks for a topic: team median XP, common gaps, org percentile.

    In local mode (no KNOWLEDGE_GRAPH_API_URL), returns personal stats only.
    Set KNOWLEDGE_GRAPH_API_URL to enable team and org benchmark layers.
    Returns JSON.

    Args:
        topic: Topic name, e.g. 'claude-code'
    """
    # Read personal stats from local tree
    user_stats: dict = {"level": None, "xp": None}
    path = GRAPH_DIR / f"{topic}.md"
    if path.exists():
        fm = _parse_frontmatter(path.read_text(encoding="utf-8"))
        user_stats = {
            "level": fm.get("level"),
            "xp": _safe_xp(fm.get("xp", "0")),
        }

    if API_URL:
        try:
            import urllib.request
            req = urllib.request.Request(
                f"{API_URL}/benchmarks/{topic}",
                headers={"Accept": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                remote = json.loads(resp.read().decode("utf-8"))
                remote["user"] = user_stats  # local stats always override
                return json.dumps(remote, indent=2)
        except Exception as e:
            return json.dumps({
                "topic": topic,
                "user": user_stats,
                "team": None,
                "org": None,
                "global": None,
                "error": f"Backend fetch failed: {e}",
            }, indent=2)

    return json.dumps({
        "topic": topic,
        "user": user_stats,
        "team": None,
        "org": None,
        "global": None,
        "backend_url": None,
        "message": (
            "Local mode — personal stats only. "
            "Set KNOWLEDGE_GRAPH_API_URL for team/org benchmarks."
        ),
    }, indent=2)


@mcp.tool()
def export_delta(topic: str, since_date: str) -> str:
    """
    Export demonstrated ([✓]) nodes added since a given date.

    Returns a markdown delta in the project-local tree format, suitable for
    committing to .claude/knowledge-graphs/{topic}.md to share with teammates,
    or for seeding a remote backend.

    Args:
        topic:      Topic name, e.g. 'claude-code'
        since_date: ISO date string (YYYY-MM-DD). Nodes with evidence on or
                    after this date are included.
    """
    path = GRAPH_DIR / f"{topic}.md"
    if not path.exists():
        return f"NO_TREE_FILE: {topic}"

    try:
        cutoff = datetime.strptime(since_date, "%Y-%m-%d").date()
    except ValueError:
        return f"Invalid date '{since_date}' — use YYYY-MM-DD"

    content = path.read_text(encoding="utf-8")
    repo = Path.cwd().name
    delta_lines = []

    # Match evidence date: "— repo, YYYY-MM-DD: note | next: ..." pattern
    # The evidence date comes between "—" and the first colon after it.
    evidence_date_re = re.compile(r"—[^,]+,\s*(\d{4}-\d{2}-\d{2}):")

    for line in content.splitlines():
        stripped = line.strip()
        if not stripped.startswith("- [✓"):
            continue
        m = evidence_date_re.search(stripped)
        if not m:
            continue
        try:
            evidence_date = datetime.strptime(m.group(1), "%Y-%m-%d").date()
        except ValueError:
            continue
        if evidence_date >= cutoff:
            delta_lines.append(stripped)

    if not delta_lines:
        return f"No demonstrated nodes found since {since_date} in topic '{topic}'"

    header = (
        f"---\n"
        f"version: 3\n"
        f"topic: {topic}\n"
        f"repo: {repo}\n"
        f"updated: {TODAY}\n"
        f"---\n\n"
        f"# {topic} Knowledge Graph — {repo}\n\n"
        f"*Project evidence log — nodes demonstrated since {since_date}. "
        f"Merges with personal graph on /ramp:up run.*\n\n"
        f"## Evidence\n"
    )
    return header + "\n".join(delta_lines) + "\n"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
