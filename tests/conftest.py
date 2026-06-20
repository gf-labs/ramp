"""Shared fixtures for the ramp test suite.

Run from the repo root:

    python3 -m pip install -r requirements-dev.txt
    python3 -m pytest tests/ -q

The scripts under ``scripts/`` have hyphenated filenames (``skill-observer.py``,
``setup-mcp.py``), so they cannot be imported by name — we load them from their
path with ``importlib``. Importing is side-effect-free: each script guards its
entrypoint behind ``if __name__ == "__main__"`` and does no I/O at module load.
These tests deliberately depend only on the standard library, so they run
without the MCP server's ``.venv``.
"""
import importlib.util
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def observer():
    """The skill-observer hook module (detection rules + XP computation)."""
    return _load("skill_observer", "skill-observer.py")


@pytest.fixture(scope="session")
def setup_mcp():
    """The setup-mcp SessionStart hook module (idempotent MCP registration)."""
    return _load("setup_mcp", "setup-mcp.py")
