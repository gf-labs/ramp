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
