#!/usr/bin/env python3
"""
skill-observer.py — Passive Claude Code knowledge tree observer

Hook that watches sessions and updates ~/.claude/knowledge-trees/claude-code.md
when knowledge tree evidence is detected from tool calls and lifecycle events.

Install (via plugin — automatic):
  /plugin install sup@sup-marketplace
  Hooks are auto-registered. No manual setup needed.

For standalone use, register in ~/.claude/settings.json:
  PostToolUse (matcher: ".*"), WorktreeCreate, SessionStart
  → command: "python3 /path/to/skill-observer.py"

Writes to: ~/.claude/knowledge-trees/claude-code.md (created automatically if absent)
Note: this observer is Claude Code–specific. For other topics, create a separate
observer script with topic-specific detection rules.

Note: built-in CLI commands (/help, /compact, /cost, /doctor) fire NO hook events —
they are handled by the CLI itself before any tool loop runs. Mastery of these is
captured via /sup assessment, not this observer.

Claude Code passes hook input as JSON on stdin. Event shapes:
  PostToolUse:   {"hook_event_name": "PostToolUse", "tool_name": "Bash", "tool_input": {...}}
  WorktreeCreate: {"hook_event_name": "WorktreeCreate", "worktree_path": "...", "cwd": "..."}
  SessionStart:  {"hook_event_name": "SessionStart", "source": "startup|resume|clear|compact"}
"""

import json
import os
import re
import sys
from datetime import date
from pathlib import Path

# All current detection rules are Claude Code–specific, so always writes to claude-code topic.
# Future topic-specific observers can be separate scripts with their own detection rules
# registered under separate hook matchers (e.g., matcher: "bash_runner_.*").
SKILL_TREE_PATH = Path.home() / ".claude" / "knowledge-trees" / "claude-code.md"
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
            capture_output=True, text=True, timeout=2
        )
        if result.returncode == 0:
            return Path(result.stdout.strip()).name
    except Exception:
        pass
    return Path.cwd().name


def read_tree() -> str:
    if SKILL_TREE_PATH.exists():
        return SKILL_TREE_PATH.read_text()
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


def save_tree(tree: str):
    # Update the `updated:` date in frontmatter
    lines = tree.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("updated:"):
            lines[i] = f"updated: {TODAY}"
            break
    SKILL_TREE_PATH.parent.mkdir(parents=True, exist_ok=True)
    SKILL_TREE_PATH.write_text("\n".join(lines) + ("\n" if tree.endswith("\n") else ""))


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
    # Bash: claude -p → C: Bash mode / D: Agent teams
    {
        "tool": "Bash",
        "field": "command",
        "pattern": r"claude\s+(-p|--print)\b",
        "node": "Bash mode (!command) and -p",
    },
    {
        "tool": "Bash",
        "field": "command",
        "pattern": r"claude\s+(-p|--print)\b",
        "node": "Agent teams and headless mode",
    },
    # Write/Edit to ~/.claude/agents/*.md → D: Custom subagent defs
    {
        "tool": "Write",
        "field": "file_path",
        "pattern": r"\.claude/agents/.*\.md$",
        "node": "Custom subagent definitions",
    },
    {
        "tool": "Edit",
        "field": "file_path",
        "pattern": r"\.claude/agents/.*\.md$",
        "node": "Custom subagent definitions",
    },
    # Write/Edit to .claude/commands/*.md → D: Custom slash commands
    {
        "tool": "Write",
        "field": "file_path",
        "pattern": r"\.claude/commands/.*\.md$",
        "node": "Custom slash commands",
    },
    {
        "tool": "Edit",
        "field": "file_path",
        "pattern": r"\.claude/commands/.*\.md$",
        "node": "Custom slash commands",
    },
    # Write/Edit to .github/workflows/ with 'claude' → D: Agent teams
    {
        "tool": "Write",
        "field": "file_path",
        "pattern": r"\.github/workflows/",
        "content_pattern": r"claude",
        "node": "Agent teams and headless mode",
    },
    # Write/Edit to ~/.claude/settings.json with 'hooks' → E: hooks
    {
        "tool": "Write",
        "field": "file_path",
        "pattern": r"settings\.json$",
        "content_field": "content",
        "content_pattern": r'"hooks"',
        "node": "PostToolUse hooks",  # generic — could be any hook type
    },
    {
        "tool": "Edit",
        "field": "file_path",
        "pattern": r"settings\.json$",
        "content_field": "new_string",
        "content_pattern": r'"hooks"',
        "node": "PostToolUse hooks",
    },
    # Write/Edit to settings.json with 'mcpServers' → D: MCP servers
    {
        "tool": "Write",
        "field": "file_path",
        "pattern": r"settings\.json$",
        "content_field": "content",
        "content_pattern": r'"mcpServers"',
        "node": "MCP servers configured and used",
    },
    {
        "tool": "Edit",
        "field": "file_path",
        "pattern": r"settings\.json$",
        "content_field": "new_string",
        "content_pattern": r'"mcpServers"',
        "node": "MCP servers configured and used",
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


def main():
    data = read_stdin()
    hook_event = data.get("hook_event_name", "PostToolUse")  # default for legacy payloads

    tree = read_tree()
    if not tree:
        # No tree yet — nothing to update
        return

    repo = get_repo_name()
    changed = False

    if hook_event == "WorktreeCreate":
        worktree_path = data.get("worktree_path", "")
        node = "Worktrees for parallel development"
        if not node_already_demonstrated(tree, node):
            evidence = f"{repo}, {TODAY}: worktree created at {worktree_path or 'unknown path'}"
            tree, did_change = update_node(tree, node, "[✓|historical]", evidence)
            if did_change:
                changed = True

    elif hook_event == "SessionStart":
        # Plugin path: auto-symlink schemas from plugin cache to ~/.claude/knowledge-trees/schemas/
        # This runs when installed as a plugin (CLAUDE_PLUGIN_ROOT is set by Claude Code).
        # On standalone installs, CLAUDE_PLUGIN_ROOT is not set — skipped.
        plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
        if plugin_root:
            topics_dir = Path(plugin_root) / "topics"
            schemas_dir = Path.home() / ".claude" / "knowledge-trees" / "schemas"
            if topics_dir.is_dir():
                schemas_dir.mkdir(parents=True, exist_ok=True)
                for topic_file in topics_dir.glob("*.md"):
                    dst = schemas_dir / topic_file.name
                    if dst.is_symlink():
                        if dst.resolve() != topic_file.resolve():
                            dst.unlink()
                            dst.symlink_to(topic_file)
                    elif not dst.exists():
                        dst.symlink_to(topic_file)
                    # Real file (manually placed) → leave it alone

        source = data.get("source", "")
        if source == "compact":
            node = "Context window and /compact usage"
            if not node_already_demonstrated(tree, node):
                evidence = f"{repo}, {TODAY}: session started via /compact"
                tree, did_change = update_node_reported(tree, node, evidence)
                if did_change:
                    changed = True
        elif source == "resume":
            node = "Session naming and resumption"
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
            if node_already_demonstrated(tree, node):
                continue
            evidence = f"{repo}, {TODAY}: detected via {tool_name} tool call"
            tree, did_change = update_node(tree, node, "[✓|historical]", evidence)
            if did_change:
                changed = True

    if changed:
        save_tree(tree)


if __name__ == "__main__":
    main()
