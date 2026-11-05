"""Observer detection logic.

``matches_rule`` must fire only on the exact tool + pattern, and
``update_node_reported`` must upgrade ``[ ]`` → ``[~|reported]`` while never
downgrading a node that is already demonstrated (the core never-downgrade
invariant the whole tool rests on).
"""

WORKTREE_RULE = {"tool": "Bash", "field": "command", "pattern": r"git\s+worktree\s+add"}


def test_matches_rule_fires_on_pattern(observer):
    assert observer.matches_rule(WORKTREE_RULE, "Bash", {"command": "git worktree add ../wt"})


def test_matches_rule_ignores_other_tool(observer):
    assert not observer.matches_rule(WORKTREE_RULE, "Write", {"command": "git worktree add x"})


def test_matches_rule_ignores_nonmatching_command(observer):
    assert not observer.matches_rule(WORKTREE_RULE, "Bash", {"command": "git status"})


def test_reported_upgrade_from_not_yet(observer):
    tree = "## [Build · ROOT] Agents and Orchestration\n- [ ] Worktrees for parallel development\n"
    new, changed = observer.update_node_reported(
        tree, "Worktrees for parallel development", "my-repo, today: ev"
    )
    assert changed
    assert "[~|reported] Worktrees for parallel development" in new


def test_reported_never_downgrades_demonstrated(observer):
    tree = "- [✓|artifact] Worktrees for parallel development — my-repo, 2026-01-01: ev\n"
    new, changed = observer.update_node_reported(
        tree, "Worktrees for parallel development", "new ev"
    )
    assert not changed
    assert "[✓|artifact]" in new


def _rules_for(observer, node):
    return [r for r in observer.DETECTION_RULES if r["node"] == node]


def test_mcp_rules_watch_the_registries_not_settings_json(observer):
    """Claude Code registers MCP servers in .mcp.json / ~/.claude.json (or via
    `claude mcp add`), never in settings.json — a settings.json rule never fires on a correct registration."""
    rules = _rules_for(observer, "MCP: configure and use servers")
    project = {"file_path": "/repo/.mcp.json", "content": '{"mcpServers": {"kg": {}}}'}
    assert any(observer.matches_rule(r, "Write", project) for r in rules)
    user = {"file_path": "/Users/me/.claude.json", "new_string": '"mcpServers": {'}
    assert any(observer.matches_rule(r, "Edit", user) for r in rules)
    cli = {"command": "claude mcp add -s user knowledge-graph -- /x/start.sh"}
    assert any(observer.matches_rule(r, "Bash", cli) for r in rules)
    settings = {"file_path": "/repo/.claude/settings.json", "content": '{"mcpServers": {}}'}
    assert not any(observer.matches_rule(r, "Write", settings) for r in rules)
    assert not any(observer.matches_rule(r, "Bash", {"command": "claude mcp list"}) for r in rules)
