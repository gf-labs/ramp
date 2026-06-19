#!/usr/bin/env python3
"""
skill-observer.py — Passive Claude Code knowledge graph observer

Hook that watches sessions and updates ~/.claude/knowledge-graphs/claude-code.md
when knowledge graph evidence is detected from tool calls and lifecycle events.

Install (via plugin — automatic):
  /plugin install ramp@gfl-marketplace
  Hooks are auto-registered. No manual setup needed.

For standalone use, register in ~/.claude/settings.json:
  PostToolUse (matcher: ".*"), SessionStart
  → command: "python3 /path/to/skill-observer.py"

Writes to: ~/.claude/knowledge-graphs/claude-code.md (created automatically if absent)
Note: this observer is Claude Code–specific. For other topics, create a separate
observer script with topic-specific detection rules.

Note: built-in CLI commands (/help, /compact, /cost, /doctor) fire NO hook events —
they are handled by the CLI itself before any tool loop runs. Mastery of these is
captured via /ramp:up assessment, not this observer.

Claude Code passes hook input as JSON on stdin. Event shapes:
  PostToolUse:   {"hook_event_name": "PostToolUse", "tool_name": "Bash", "tool_input": {...}}
  SessionStart:  {"hook_event_name": "SessionStart", "source": "startup|resume|clear|compact"}

Worktree creation is detected via the `git worktree add` PostToolUse Bash rule
(there is no `WorktreeCreate` hook event in Claude Code).

This observer can be registered in more than one scope (plugin + project), so it may
fire more than once for the same event. The read-modify-write of the graph file is
guarded by an exclusive file lock and an atomic replace, making concurrent fires safe
(at worst redundant) rather than corrupting the file.
"""

import json
import os
import re
import sys
from datetime import date
from pathlib import Path

try:
    import fcntl  # POSIX only; used for the cross-process write lock
except ImportError:  # pragma: no cover - non-POSIX fallback
    fcntl = None

# All current detection rules are Claude Code–specific, so always writes to claude-code topic.
# Future topic-specific observers can be separate scripts with their own detection rules
# registered under separate hook matchers (e.g., matcher: "bash_runner_.*").
SKILL_GRAPH_PATH = Path.home() / ".claude" / "knowledge-graphs" / "claude-code.md"
LOCK_PATH = SKILL_GRAPH_PATH.parent / ".claude-code.md.lock"
TODAY = date.today().isoformat()


def read_stdin():
    try:
        return json.loads(sys.stdin.read())
    except Exception:
        return {}


def get_repo_name():
    """Get current git repo name from cwd."""
    try:
        import subprocess
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return Path(result.stdout.strip()).name
    except Exception:
        pass
    return Path.cwd().name


def read_tree() -> str:
    if SKILL_GRAPH_PATH.exists():
        return SKILL_GRAPH_PATH.read_text()
    return ""


def node_already_demonstrated(tree: str, node_pattern: str) -> bool:
    """Return True if the node already has [✓] status in the tree."""
    for line in tree.splitlines():
        if node_pattern in line and line.strip().startswith("- [✓"):
            return True
    return False


def update_node(tree: str, node_pattern: str, status: str, evidence: str) -> tuple[str, bool]:
    """
    Upgrade a node to [✓|historical]. Returns (updated_tree, changed).
    Only upgrades — never downgrades a [✓] node.
    """
    lines = tree.splitlines()
    changed = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("- ["):
            continue
        if node_pattern not in line:
            continue
        # Already [✓] — preserve (never downgrade)
        if stripped.startswith("- [✓"):
            return tree, False
        # Upgrade to [✓|historical]
        m = re.match(r"^(\s*- )\[.*?\] (.+?)(\s*—.*)?$", line)
        if m:
            indent = m.group(1)
            node_name = m.group(2).strip()
            lines[i] = f"{indent}[✓|historical] {node_name} — {evidence}"
            changed = True
            break
    return "\n".join(lines) + ("\n" if tree.endswith("\n") else ""), changed


def update_node_reported(tree: str, node_pattern: str, evidence: str) -> tuple[str, bool]:
    """
    Set a node to [~|reported] if it is currently [ ] (not yet).
    Does not upgrade [~] or [✓] nodes — those are already at equal or higher status.
    Returns (updated_tree, changed).
    """
    lines = tree.splitlines()
    changed = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("- ["):
            continue
        if node_pattern not in line:
            continue
        # Already [~] or [✓] — preserve
        if stripped.startswith("- [✓") or stripped.startswith("- [~"):
            return tree, False
        # Upgrade [ ] → [~|reported]
        m = re.match(r"^(\s*- )\[.*?\] (.+?)(\s*—.*)?$", line)
        if m:
            indent = m.group(1)
            node_name = m.group(2).strip()
            lines[i] = f"{indent}[~|reported] {node_name} — {evidence}"
            changed = True
            break
    return "\n".join(lines) + ("\n" if tree.endswith("\n") else ""), changed


BRANCH_XP = {"ROOT": 10, "A": 15, "B": 20, "C": 25, "D": 35, "E": 50}


def compute_xp(tree: str) -> int:
    """Compute total XP from the tree file content.

    Branch tier is determined by the nearest ## [ header above each node.
    Header format: ## [SubTopic · BRANCH] Section name
    XP: [✓ = full, [~ = half (floor), [ ] = 0
    """
    xp = 0
    current_branch_xp = 0
    for line in tree.splitlines():
        if line.startswith("## ["):
            m = re.search(r"\·\s*(ROOT|A|B|C|D|E)\]", line)
            current_branch_xp = BRANCH_XP.get(m.group(1), 0) if m else 0
        elif line.strip().startswith("- [✓"):
            xp += current_branch_xp
        elif line.strip().startswith("- [~"):
            xp += current_branch_xp // 2
    return xp


def save_tree(tree: str):
    # Update the `updated:` date and recompute `xp:` in frontmatter
    new_xp = compute_xp(tree)
    lines = tree.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("updated:"):
            lines[i] = f"updated: {TODAY}"
        elif line.startswith("xp:"):
            lines[i] = f"xp: {new_xp}"
    SKILL_GRAPH_PATH.parent.mkdir(parents=True, exist_ok=True)
    content = "\n".join(lines) + ("\n" if tree.endswith("\n") else "")
    # Atomic replace: write to a temp file in the same dir, then os.replace (atomic on POSIX).
    # A partial write can never leave the graph truncated even under concurrent fires.
    tmp = SKILL_GRAPH_PATH.with_suffix(f".md.tmp.{os.getpid()}")
    tmp.write_text(content)
    os.replace(tmp, SKILL_GRAPH_PATH)


# Detection rules: (tool_name, input_field, pattern, node_pattern, node_label)
# Each rule: check if tool_name matches, look for pattern in input_field value,
# then update the node identified by node_pattern.

DETECTION_RULES = [
    # Bash: git worktree add → D: Worktrees
    {
        "tool": "Bash",
        "field": "command",
        "pattern": r"git\s+worktree\s+add",
        "node": "Worktrees for parallel development",
    },
    # Bash: claude -p → C: Headless mode / Build ROOT: Agent teams
    {
        "tool": "Bash",
        "field": "command",
        "pattern": r"claude\s+(-p|--print)\b",
        "node": "Headless mode (-p flag, non-interactive)",
    },
    {
        "tool": "Bash",
        "field": "command",
        "pattern": r"claude\s+(-p|--print)\b",
        "node": "Agent teams: orchestration patterns",
    },
    # Write/Edit to ~/.claude/agents/*.md → Build ROOT: Custom subagent defs
    {
        "tool": "Write",
        "field": "file_path",
        "pattern": r"\.claude/agents/.*\.md$",
        "node": "Custom subagent definitions (.claude/agents/)",
    },
    {
        "tool": "Edit",
        "field": "file_path",
        "pattern": r"\.claude/agents/.*\.md$",
        "node": "Custom subagent definitions (.claude/agents/)",
    },
    # Write/Edit to .claude/commands/*.md → Build A: Skills
    {
        "tool": "Write",
        "field": "file_path",
        "pattern": r"\.claude/commands/.*\.md$",
        "node": "Skills (slash commands): creation and syntax",
    },
    {
        "tool": "Edit",
        "field": "file_path",
        "pattern": r"\.claude/commands/.*\.md$",
        "node": "Skills (slash commands): creation and syntax",
    },
    # Write/Edit to .github/workflows/ with 'claude' → Build ROOT: Agent teams
    {
        "tool": "Write",
        "field": "file_path",
        "pattern": r"\.github/workflows/",
        "content_pattern": r"claude",
        "node": "Agent teams: orchestration patterns",
    },
    # Write/Edit to settings.json with 'hooks' → Build B: hooks
    {
        "tool": "Write",
        "field": "file_path",
        "pattern": r"settings\.json$",
        "content_field": "content",
        "content_pattern": r'"hooks"',
        "node": "PostToolUse hooks (linting, reactions)",
    },
    {
        "tool": "Edit",
        "field": "file_path",
        "pattern": r"settings\.json$",
        "content_field": "new_string",
        "content_pattern": r'"hooks"',
        "node": "PostToolUse hooks (linting, reactions)",
    },
    # Write/Edit to settings.json with 'mcpServers' → Build C: MCP servers
    {
        "tool": "Write",
        "field": "file_path",
        "pattern": r"settings\.json$",
        "content_field": "content",
        "content_pattern": r'"mcpServers"',
        "node": "MCP: configure and use servers",
    },
    {
        "tool": "Edit",
        "field": "file_path",
        "pattern": r"settings\.json$",
        "content_field": "new_string",
        "content_pattern": r'"mcpServers"',
        "node": "MCP: configure and use servers",
    },
    # General activity rules — produce [~|historical] (corroborating evidence, not proof)
    # Glob (any) → Getting Started ROOT: Core feature surface [~]
    {
        "tool": "Glob",
        "field": "pattern",
        "pattern": r".*",
        "node": "Core feature surface (interactive vs. headless, key tools)",
        "reported": True,
    },
    # Grep (any) → Getting Started ROOT: Core feature surface [~]
    {
        "tool": "Grep",
        "field": "pattern",
        "pattern": r".*",
        "node": "Core feature surface (interactive vs. headless, key tools)",
        "reported": True,
    },
    # Agent (any) → Build ROOT: Subagent basics [~]
    {
        "tool": "Agent",
        "field": "prompt",
        "pattern": r".*",
        "node": "Subagent basics: spawning and tool access",
        "reported": True,
    },
    # Bash: git workflow → Getting Started A: Common workflow patterns [~]
    {
        "tool": "Bash",
        "field": "command",
        "pattern": r"git\s+(commit|push|diff|log|status|pull|merge)\b",
        "node": "Common workflow patterns",
        "reported": True,
    },
    # Bash: test runner → Getting Started A: Reading and verifying Claude's output [~]
    {
        "tool": "Bash",
        "field": "command",
        "pattern": r"\b(pytest|npm\s+test|yarn\s+test|go\s+test|cargo\s+test|make\s+test)\b",
        "node": "Reading and verifying Claude's output",
        "reported": True,
    },
    # Bash: git commit (implies reviewing before committing) → same node [~]
    {
        "tool": "Bash",
        "field": "command",
        "pattern": r"git\s+commit\b",
        "node": "Reading and verifying Claude's output",
        "reported": True,
    },
]


def matches_rule(rule: dict, tool_name: str, tool_input: dict) -> bool:
    if rule["tool"] != tool_name:
        return False
    field_value = str(tool_input.get(rule["field"], ""))
    if not re.search(rule["pattern"], field_value):
        return False
    # Optional: check content field for additional pattern
    if "content_pattern" in rule:
        if "content_field" in rule:
            content = str(tool_input.get(rule["content_field"], ""))
        else:
            # For Write to .github/workflows, check content field
            content = str(tool_input.get("content", ""))
        if not re.search(rule["content_pattern"], content):
            return False
    return True


def _acquire_lock():
    """Best-effort exclusive lock for the graph read-modify-write.

    The observer may be registered in more than one scope (plugin + project), so two
    processes can fire for the same event. Holding this lock serializes their
    read-modify-write so neither clobbers the other. Released automatically when this
    short-lived hook process exits. Returns the open fd (kept alive by the caller) or None.
    """
    if fcntl is None:
        return None
    try:
        LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
        lock_fd = open(LOCK_PATH, "w")
        fcntl.flock(lock_fd, fcntl.LOCK_EX)
        return lock_fd
    except Exception:
        return None


def main():
    data = read_stdin()
    hook_event = data.get("hook_event_name", "PostToolUse")  # default for legacy payloads

    if not SKILL_GRAPH_PATH.exists():
        # No tree yet — nothing to update (skip the lock entirely)
        return

    # Serialize concurrent fires before reading, so the tree we modify is the latest
    # on-disk state. `_lock` must stay referenced for the lock to be held.
    _lock = _acquire_lock()  # noqa: F841 — holds the lock for this process's lifetime

    tree = read_tree()
    if not tree:
        return

    repo = get_repo_name()
    changed = False

    if hook_event == "SessionStart":
        # Plugin path: auto-symlink schemas from plugin cache to ~/.claude/knowledge-graphs/schemas/
        # This runs when installed as a plugin (CLAUDE_PLUGIN_ROOT is set by Claude Code).
        # On standalone installs, CLAUDE_PLUGIN_ROOT is not set — skipped.
        plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
        if plugin_root:
            topics_dir = Path(plugin_root) / "topics"
            schemas_dir = Path.home() / ".claude" / "knowledge-graphs" / "schemas"
            if topics_dir.is_dir():
                schemas_dir.mkdir(parents=True, exist_ok=True)
                for topic_file in topics_dir.glob("*.md"):
                    dst = schemas_dir / topic_file.name
                    if dst.is_symlink():
                        try:
                            dst.resolve(strict=True)  # raises OSError if symlink is broken
                            # Valid symlink — leave it alone regardless of target path
                        except OSError:
                            # Broken symlink — replace it
                            dst.unlink(missing_ok=True)
                            dst.symlink_to(topic_file)
                    elif not dst.exists():
                        dst.symlink_to(topic_file)
                    # Real file (manually placed) → leave it alone

        source = data.get("source", "")
        if source == "compact":
            node = "Common workflow patterns"
            if not node_already_demonstrated(tree, node):
                evidence = f"{repo}, {TODAY}: session started via /compact"
                tree, did_change = update_node_reported(tree, node, evidence)
                if did_change:
                    changed = True
        elif source == "resume":
            node = "Interactive mode features"
            if not node_already_demonstrated(tree, node):
                evidence = f"{repo}, {TODAY}: session resumed"
                tree, did_change = update_node_reported(tree, node, evidence)
                if did_change:
                    changed = True

    else:
        # PostToolUse (default)
        tool_name = data.get("tool_name", "")
        tool_input = data.get("tool_input", {})

        if not tool_name or not tool_input:
            return

        for rule in DETECTION_RULES:
            if not matches_rule(rule, tool_name, tool_input):
                continue
            node = rule["node"]
            evidence = f"{repo}, {TODAY}: detected via {tool_name} tool call"
            if rule.get("reported", False):
                # General-activity rule → [~|historical] (update_node_reported skips [~ and [✓)
                tree, did_change = update_node_reported(tree, node, evidence)
            else:
                # Specific-evidence rule → [✓|historical]
                if node_already_demonstrated(tree, node):
                    continue
                tree, did_change = update_node(tree, node, "[✓|historical]", evidence)
            if did_change:
                changed = True

    if changed:
        save_tree(tree)


if __name__ == "__main__":
    main()
