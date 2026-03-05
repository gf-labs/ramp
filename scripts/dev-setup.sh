#!/usr/bin/env bash
# sup — dev setup
# Creates project-scope symlinks so /sup, /tree, /review, /cheatsheet work in this repo.
# Also symlinks schemas globally so they work in other repos too.
#
# For testing in OTHER repos without a global install, use:
#   claude --plugin-dir /path/to/sup
# (Commands will be namespaced: /sup:sup, /sup:tree, etc.)
set -e

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOCAL_COMMANDS="$REPO_DIR/.claude/commands"
DEST_SCHEMAS="${HOME}/.claude/knowledge-trees/schemas"

echo "Setting up sup dev mode..."

# Project-scope commands: symlink .claude/commands/ -> commands/
# These activate /sup, /tree, /review, /cheatsheet when CC opens in this repo.
mkdir -p "$LOCAL_COMMANDS"
ln -sf "$REPO_DIR/commands/sup.md"        "$LOCAL_COMMANDS/sup.md"
ln -sf "$REPO_DIR/commands/tree.md"       "$LOCAL_COMMANDS/tree.md"
ln -sf "$REPO_DIR/commands/review.md"     "$LOCAL_COMMANDS/review.md"
ln -sf "$REPO_DIR/commands/cheatsheet.md" "$LOCAL_COMMANDS/cheatsheet.md"

# Global schemas: symlink topics/ -> ~/.claude/knowledge-trees/schemas/
# Required so /sup can load topic schemas in any repo.
mkdir -p "$DEST_SCHEMAS"
ln -sf "$REPO_DIR/topics/claude-code.md"      "$DEST_SCHEMAS/claude-code.md"
ln -sf "$REPO_DIR/topics/best-practices.md"   "$DEST_SCHEMAS/best-practices.md"
ln -sf "$REPO_DIR/topics/mcp-development.md"  "$DEST_SCHEMAS/mcp-development.md"
ln -sf "$REPO_DIR/topics/anthropic-api.md"    "$DEST_SCHEMAS/anthropic-api.md"

echo "Dev mode active."
echo "  - /sup, /tree, /review, /cheatsheet work in this repo (project-scope)"
echo "  - Topic schemas symlinked globally"
echo "  - Edit commands/ or topics/ — changes reflected immediately"
echo ""
echo "To test in other repos: claude --plugin-dir $REPO_DIR"
echo "To return to a normal install: bash scripts/dev-teardown.sh"
