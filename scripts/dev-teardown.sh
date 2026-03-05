#!/usr/bin/env bash
# sup — dev teardown
# Removes project-scope .claude/commands/ symlinks.
# Replaces global schema symlinks with real copies (production install state).
set -e

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOCAL_COMMANDS="$REPO_DIR/.claude/commands"
DEST_SCHEMAS="${HOME}/.claude/knowledge-trees/schemas"

echo "Tearing down sup dev mode..."

# Remove project-scope command symlinks
for f in sup.md tree.md review.md cheatsheet.md; do
  if [ -L "$LOCAL_COMMANDS/$f" ]; then
    rm "$LOCAL_COMMANDS/$f"
    echo "  Removed .claude/commands/$f"
  fi
done

# Replace global schema symlinks with real copies
for f in claude-code.md best-practices.md mcp-development.md anthropic-api.md; do
  if [ -L "$DEST_SCHEMAS/$f" ]; then
    cp --remove-destination "$REPO_DIR/topics/$f" "$DEST_SCHEMAS/$f"
    echo "  Copied topics/$f -> schemas/$f"
  fi
done

echo "Done. ~/.claude/knowledge-trees/schemas/ now has real copies."
echo "Edits to topics/ no longer affect the installed schemas."
