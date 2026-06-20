"""setup-mcp.py idempotency.

The SessionStart hook re-fires every session; ``already_registered`` is the
fast-path guard that keeps it a no-op once the server is in ``~/.claude.json``.
It must also degrade gracefully on a missing or malformed config rather than
raising into the hook runner.
"""


def test_registered_when_server_present(setup_mcp, tmp_path, monkeypatch):
    cfg = tmp_path / ".claude.json"
    cfg.write_text('{"mcpServers": {"knowledge-graph": {"command": "x"}}}')
    monkeypatch.setattr(setup_mcp, "CLAUDE_JSON", cfg)
    assert setup_mcp.already_registered() is True


def test_not_registered_when_file_missing(setup_mcp, tmp_path, monkeypatch):
    monkeypatch.setattr(setup_mcp, "CLAUDE_JSON", tmp_path / "absent.json")
    assert setup_mcp.already_registered() is False


def test_not_registered_when_server_absent(setup_mcp, tmp_path, monkeypatch):
    cfg = tmp_path / ".claude.json"
    cfg.write_text('{"mcpServers": {"other": {}}}')
    monkeypatch.setattr(setup_mcp, "CLAUDE_JSON", cfg)
    assert setup_mcp.already_registered() is False


def test_malformed_json_is_not_registered(setup_mcp, tmp_path, monkeypatch):
    cfg = tmp_path / ".claude.json"
    cfg.write_text("{ not valid json")
    monkeypatch.setattr(setup_mcp, "CLAUDE_JSON", cfg)
    assert setup_mcp.already_registered() is False
