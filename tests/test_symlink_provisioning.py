"""SEV-1 regression: schema symlinks must be provisioned on SessionStart even
when the user has no personal knowledge-graph tree yet.

The bug: ``main`` returned early on ``not SKILL_GRAPH_PATH.exists()`` *before*
reaching the symlink step, so a fresh install never linked the topic schemas
into ``~/.claude/ramp/schemas/`` and ``/ramp:up`` failed its first
run with ``SCHEMA_NOT_FOUND``. The fix hoists provisioning above that guard.
"""


def _make_plugin(tmp_path, *topics):
    plugin_root = tmp_path / "plugin"
    topics_dir = plugin_root / "topics"
    topics_dir.mkdir(parents=True)
    for name in topics:
        (topics_dir / name).write_text("# schema\n")
    return plugin_root, topics_dir


def test_main_provisions_symlinks_on_sessionstart_without_tree(observer, tmp_path, monkeypatch):
    """The whole point of the fix: a fresh machine (no personal tree) still gets
    its schemas symlinked when main() runs on SessionStart."""
    plugin_root, topics_dir = _make_plugin(tmp_path, "claude-code.md", "build.md")
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("CLAUDE_PLUGIN_ROOT", str(plugin_root))
    monkeypatch.setenv("HOME", str(home))
    # Simulate a fresh install: no personal tree on disk, and repoint the module's
    # import-time path at that absent location so main() takes the early-return branch.
    absent_tree = home / ".claude" / "ramp" / "graphs" / "claude-code.md"
    monkeypatch.setattr(observer, "SKILL_GRAPH_PATH", absent_tree)
    monkeypatch.setattr(
        observer, "read_stdin",
        lambda: {"hook_event_name": "SessionStart", "source": "startup"},
    )

    observer.main()

    schemas = home / ".claude" / "ramp" / "schemas"
    assert (schemas / "claude-code.md").is_symlink()
    assert (schemas / "build.md").is_symlink()
    assert (schemas / "claude-code.md").resolve() == (topics_dir / "claude-code.md").resolve()


def test_main_migrates_legacy_graphs_on_sessionstart(observer, tmp_path, monkeypatch):
    """SessionStart must run the graph-home migration (main() → ramp_core.
    migrate_graph_home): a legacy ~/.claude/knowledge-graphs graph is copied into
    ~/.claude/ramp/graphs even when no new-home tree exists yet. Deleting the
    migration call from main() must fail this test."""
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.delenv("CLAUDE_PLUGIN_ROOT", raising=False)
    legacy = home / ".claude" / "knowledge-graphs"
    legacy.mkdir(parents=True)
    (legacy / "claude-code.md").write_text("---\nlevel: Builder\nxp: 0\n---\n")
    # Repoint the module's import-time paths at the scratch HOME. After migration
    # the tree EXISTS, so main() proceeds past its guard into the lock — the lock
    # path must not touch the real home.
    new_tree = home / ".claude" / "ramp" / "graphs" / "claude-code.md"
    monkeypatch.setattr(observer, "SKILL_GRAPH_PATH", new_tree)
    monkeypatch.setattr(observer, "LOCK_PATH", new_tree.parent / ".claude-code.md.lock")
    monkeypatch.setattr(
        observer, "read_stdin",
        lambda: {"hook_event_name": "SessionStart", "source": "startup"},
    )

    observer.main()

    assert new_tree.exists()
    assert (legacy / "claude-code.md").exists()      # legacy kept as backup


def test_provision_is_noop_without_plugin_root(observer, tmp_path, monkeypatch):
    """Standalone install (no CLAUDE_PLUGIN_ROOT): must not raise or create anything."""
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.delenv("CLAUDE_PLUGIN_ROOT", raising=False)
    monkeypatch.setenv("HOME", str(home))

    observer.provision_schema_symlinks()  # must be a clean no-op

    assert not (home / ".claude" / "ramp" / "schemas").exists()


def test_provision_is_idempotent_and_preserves_valid_links(observer, tmp_path, monkeypatch):
    """Re-running leaves an existing valid symlink in place (no churn, no error)."""
    plugin_root, topics_dir = _make_plugin(tmp_path, "claude-code.md")
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("CLAUDE_PLUGIN_ROOT", str(plugin_root))
    monkeypatch.setenv("HOME", str(home))

    observer.provision_schema_symlinks()
    observer.provision_schema_symlinks()  # second run must be harmless

    link = home / ".claude" / "ramp" / "schemas" / "claude-code.md"
    assert link.is_symlink()
    assert link.resolve() == (topics_dir / "claude-code.md").resolve()
