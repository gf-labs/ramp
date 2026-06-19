#!/usr/bin/env python3
"""
Auto-register the knowledge-graph MCP server via `claude mcp add -s user`.

Runs on SessionStart — idempotent, skips silently if already registered.
Writes to ~/.claude.json (user scope), available across all projects.

Delivery notes (why this is more than a one-liner):
  - A plugin install copies the repo to the plugin cache with NO `.venv`. The system
    `python3` ships a conflicting `mcp` stub, so registering the server under it would
    import the wrong package and the server would never start. We therefore provision a
    repo-local `.venv` on first run and register `mcp/start.sh`, which execs the venv
    python directly (avoiding the macOS framework-symlink resolution trap).
  - If the venv can't be provisioned (e.g. a read-only plugin cache, no network), we do
    NOT fall back to system python3 — we leave the server unregistered (ramp works fine
    without it) and print actionable manual steps, recording a skip marker so we don't
    retry the heavy build on every subsequent session.
"""

import json
import os
import shutil
import subprocess
from pathlib import Path

PLUGIN_ROOT = Path(os.environ.get("CLAUDE_PLUGIN_ROOT", Path(__file__).parent.parent))
SERVER_SCRIPT = PLUGIN_ROOT / "mcp" / "server.py"
START_SH = PLUGIN_ROOT / "mcp" / "start.sh"
REQUIREMENTS = PLUGIN_ROOT / "requirements.txt"
VENV_DIR = PLUGIN_ROOT / ".venv"
VENV_PYTHON = VENV_DIR / "bin" / "python3"
CLAUDE_JSON = Path.home() / ".claude.json"
SKIP_MARKER = Path.home() / ".claude" / ".ramp-mcp-setup-skip"
SERVER_NAME = "knowledge-graph"


def already_registered() -> bool:
    """Check ~/.claude.json directly — faster than `claude mcp list`."""
    if not CLAUDE_JSON.exists():
        return False
    try:
        data = json.loads(CLAUDE_JSON.read_text(encoding="utf-8"))
        return SERVER_NAME in data.get("mcpServers", {})
    except (json.JSONDecodeError, OSError):
        return False


def venv_has_mcp() -> bool:
    """True only if the repo-local venv exists AND can import the real `mcp` package."""
    if not VENV_PYTHON.exists():
        return False
    try:
        r = subprocess.run(
            [str(VENV_PYTHON), "-c", "import mcp"],
            capture_output=True, timeout=10,
        )
        return r.returncode == 0
    except Exception:
        return False


def provision_venv() -> bool:
    """Create the repo-local venv and install requirements. Returns True on success."""
    try:
        subprocess.run(
            ["python3", "-m", "venv", str(VENV_DIR)],
            check=True, timeout=120, capture_output=True,
        )
        pip = VENV_DIR / "bin" / "pip"
        subprocess.run(
            [str(pip), "install", "-q", "-r", str(REQUIREMENTS)],
            check=True, timeout=300, capture_output=True,
        )
        return venv_has_mcp()
    except Exception:
        return False


def manual_hint() -> str:
    return (
        "[ramp] knowledge-graph MCP server not enabled (optional — ramp works without it).\n"
        f"       To enable it manually:\n"
        f"         python3 -m venv {VENV_DIR}\n"
        f"         {VENV_DIR / 'bin' / 'pip'} install -r {REQUIREMENTS}\n"
        f"         claude mcp add -s user {SERVER_NAME} {START_SH}\n"
        "       then restart Claude Code. (Not registering system python3 — it ships a "
        "conflicting 'mcp' stub.)"
    )


def main() -> None:
    if already_registered():
        return

    claude = shutil.which("claude")
    if not claude:
        print("[ramp] 'claude' not found in PATH — skipping MCP setup")
        return

    # Ensure the venv exists and imports the real mcp package. Provision once if missing,
    # unless a prior attempt already failed (avoid rebuilding every session).
    if not venv_has_mcp():
        if SKIP_MARKER.exists():
            return
        print("[ramp] provisioning knowledge-graph MCP venv (one-time)…")
        if not provision_venv():
            try:
                SKIP_MARKER.parent.mkdir(parents=True, exist_ok=True)
                SKIP_MARKER.write_text("mcp venv provisioning failed; remove this file to retry\n")
            except OSError:
                pass
            print(manual_hint())
            return

    # Register via start.sh so the venv python is resolved without the symlink trap.
    try:
        subprocess.run(
            [claude, "mcp", "add", "-s", "user", SERVER_NAME, str(START_SH)],
            check=True, timeout=15, capture_output=True,
        )
        print(f"[ramp] registered MCP server '{SERVER_NAME}' (user scope) → restart Claude Code to activate")
    except subprocess.CalledProcessError as e:
        print(f"[ramp] failed to register MCP server: {e.stderr.decode().strip()}")


if __name__ == "__main__":
    main()
