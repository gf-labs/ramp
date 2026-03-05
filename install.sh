#!/usr/bin/env bash
# sup — global install script
# Installs /sup, /tree, /review, and /cheatsheet commands + topic schemas to ~/.claude/
set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
DEST_COMMANDS="${HOME}/.claude/commands"
DEST_SCHEMAS="${HOME}/.claude/knowledge-trees/schemas"

echo "Installing sup..."

mkdir -p "$DEST_COMMANDS" "$DEST_SCHEMAS"

cp "$REPO_DIR/commands/sup.md"        "$DEST_COMMANDS/sup.md"
cp "$REPO_DIR/commands/tree.md"       "$DEST_COMMANDS/tree.md"
cp "$REPO_DIR/commands/review.md"     "$DEST_COMMANDS/review.md"
cp "$REPO_DIR/commands/cheatsheet.md" "$DEST_COMMANDS/cheatsheet.md"
cp "$REPO_DIR/topics/"*.md               "$DEST_SCHEMAS/"

echo "Done. Run /sup in any repo to start."
echo ""
echo "Optional — passive observer (auto-updates your knowledge tree as you work):"
echo "  bash $REPO_DIR/scripts/install-hook.sh"
