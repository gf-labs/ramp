#!/usr/bin/env python3
"""
knowledge-graph MCP server for ramp

Provides structured read/write access to Claude Code knowledge graphs.
Backend: local files at ~/.claude/ramp/graphs/ by default.
Set KNOWLEDGE_GRAPH_API_URL to proxy reads/writes to a hosted backend,
enabling cross-device sync, team skill matrices, and org analytics.

Setup (opt-in — run scripts/setup-mcp.py manually, or do these steps yourself):
  python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
  claude mcp add -s user knowledge-graph /path/to/ramp/mcp/start.sh

  Register the start.sh wrapper (NOT python3 directly): it execs the repo-local
  .venv python, sidestepping the macOS framework-symlink trap, and never the
  system python3 — which ships a conflicting `mcp` stub. Writes to ~/.claude.json
  (user scope, persists across all projects). See .mcp.json.example for reference.

Environment variables:
  KNOWLEDGE_GRAPH_API_URL  If set, read/write proxies to this backend URL.
                          Enables team/org/global benchmark layers.
                          Format: https://your-backend.example.com
"""

import json
import logging
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

# ramp_core (repo root) is the single source of truth for XP/SR/validation/locking,
# shared with scripts/skill-observer.py so the hook and this server never disagree.
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import ramp_core

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

GRAPH_DIR = Path.home() / ".claude" / "ramp" / "graphs"
API_URL = os.environ.get("KNOWLEDGE_GRAPH_API_URL", "").rstrip("/")
TODAY = date.today().isoformat()

_LOG_FILE = Path.home() / ".claude" / "logs" / "knowledge-graph.log"
_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=_LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger("knowledge-graph")

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

    Returns the full markdown content of ~/.claude/ramp/graphs/{topic}.md,
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
                result = resp.read().decode("utf-8")
            logger.info("READ topic=%s source=api", topic)
            return result
        except Exception:
            pass  # Fall through to local file

    path = GRAPH_DIR / f"{topic}.md"
    exists = path.exists()
    logger.info("READ topic=%s source=%s", topic, "local" if exists else "missing")
    return path.read_text(encoding="utf-8") if exists else "NO_TREE_FILE"


@mcp.tool()
def save_graph(topic: str, content: str) -> str:
    """
    Save the knowledge graph for a topic — the canonical, validated writer.

    Delegates to ramp_core.save_graph (the kernel-owned composition, shared
    with the CLI `save` verb): recomputes xp: in code (overwriting any
    model-supplied value), refuses to downgrade any node that is [✓] on disk,
    fills a MISSING next: date on newly [✓] nodes (L1), surfaces every
    validate_tree problem and repair in the return string, then writes
    atomically under a file lock. Rejects (does not write) only on
    unrepairable structural damage: absent frontmatter.

    Args:
        topic:   Topic name, e.g. 'claude-code'
        content: Full markdown content of the graph (version 3 format)
    """
    result = ramp_core.save_graph(topic, content, graph_dir=GRAPH_DIR)
    if result.startswith("REJECTED"):
        logger.info("SAVE topic=%s rejected", topic)
        return result

    path = GRAPH_DIR / f"{topic}.md"
    saved = path.read_text(encoding="utf-8")  # the kernel-written state, for log + sync
    fm = _parse_frontmatter(saved)
    logger.info(
        "SAVE topic=%s level=%s xp=%d",
        topic, fm.get("level", "unknown"), _safe_xp(fm.get("xp", "0")),
    )

    if API_URL:
        try:
            import urllib.request
            req = urllib.request.Request(
                f"{API_URL}/graphs/{topic}",
                data=saved.encode("utf-8"),
                method="PUT",
                headers={"Content-Type": "text/plain; charset=utf-8"},
            )
            urllib.request.urlopen(req, timeout=5)
        except Exception as e:
            result += f" · backend sync failed: {e}"

    return result


@mcp.tool()
def advance_review(topic: str, node_name: str, outcome: str) -> str:
    """
    Advance (or reset) a [✓] node's spaced-repetition schedule after a review.

    All level + date math is done in code (ramp_core) — review.md no longer
    computes dates. A 'pass' bumps the level one rung and pushes the next date
    out per the ladder; a 'fail' resets to L1. xp: is recomputed (a [✓]-node SR
    pass does not change status, so XP is unchanged — this fixes the cosmetic
    "+XP" overstatement). Writes atomically under a lock.

    Args:
        topic:     Topic name, e.g. 'claude-code'
        node_name: The node's name (text after the status marker)
        outcome:   'pass' or 'fail'
    """
    result = ramp_core.advance_review(topic, node_name, outcome, graph_dir=GRAPH_DIR)
    logger.info("ADVANCE_REVIEW topic=%s node=%s outcome=%s result=%s",
                topic, node_name, outcome, result)
    return result


@mcp.tool()
def list_topics() -> str:
    """
    List all knowledge graph topics with their current level and XP.

    Scans ~/.claude/ramp/graphs/*.md and extracts frontmatter.
    Returns a JSON array of objects: [{topic, level, xp, updated}].
    """
    if not GRAPH_DIR.exists():
        logger.info("LIST topics=0")
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

    logger.info("LIST topics=%d", len(topics))
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
    logger.info("BENCHMARKS topic=%s", topic)
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

    logger.info("EXPORT_DELTA topic=%s since=%s nodes=%d", topic, since_date, len(delta_lines))
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
