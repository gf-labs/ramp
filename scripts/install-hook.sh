#!/usr/bin/env bash
# sup — passive observer hook install
# Registers skill-observer.py as PostToolUse + WorktreeCreate + SessionStart hooks in ~/.claude/settings.json
set -e

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
HOOK_SRC="$REPO_DIR/scripts/skill-observer.py"
HOOK_DEST="${HOME}/.claude/hooks/skill-observer.py"
SETTINGS="${HOME}/.claude/settings.json"

echo "Installing passive observer hook..."

mkdir -p "${HOME}/.claude/hooks"
cp "$HOOK_SRC" "$HOOK_DEST"
chmod +x "$HOOK_DEST"

# Add hook to settings.json if not already present
if ! grep -q "skill-observer" "$SETTINGS" 2>/dev/null; then
  python3 - <<EOF
import json, os

settings_path = os.path.expanduser("~/.claude/settings.json")
try:
    with open(settings_path) as f:
        settings = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    settings = {}

hook_cmd = {"type": "command", "command": "python3 ~/.claude/hooks/skill-observer.py"}

hooks = settings.setdefault("hooks", {})
added = []

# PostToolUse (with matcher)
post_tool = hooks.setdefault("PostToolUse", [])
if not any("skill-observer" in str(r) for r in post_tool):
    post_tool.append({"matcher": ".*", "hooks": [hook_cmd]})
    added.append("PostToolUse")

# WorktreeCreate (no matcher needed)
worktree = hooks.setdefault("WorktreeCreate", [])
if not any("skill-observer" in str(r) for r in worktree):
    worktree.append({"hooks": [hook_cmd]})
    added.append("WorktreeCreate")

# SessionStart (no matcher needed)
session_start = hooks.setdefault("SessionStart", [])
if not any("skill-observer" in str(r) for r in session_start):
    session_start.append({"hooks": [hook_cmd]})
    added.append("SessionStart")

if added:
    with open(settings_path, "w") as f:
        json.dump(settings, f, indent=2)
    print(f"Hooks registered: {', '.join(added)}")
else:
    print("All hooks already registered.")
EOF
else
  echo "Hook already registered in $SETTINGS"
fi

echo "Observer active. It will update your knowledge tree automatically as you work."
