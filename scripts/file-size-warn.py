#!/usr/bin/env python3
"""
PostToolUse hook — warns when a .md file exceeds 600 lines.

Receives hook event as JSON on stdin (Edit|Write matcher).
Prints file name and line count; warns if >600 lines.
"""
import json
import os
import sys
from pathlib import Path

try:
    data = json.loads(sys.stdin.read() or "{}")
    tool_input = data.get("tool_input", {})
    path = tool_input.get("file_path") or tool_input.get("path", "")
    if path and path.endswith(".md") and Path(path).exists():
        lines = sum(1 for _ in open(path))
        name = os.path.basename(path)
        if lines > 600:
            print(f"[sup] {name}: {lines} lines — prompt files should stay focused")
        else:
            print(f"[sup] {name}: {lines} lines")
except Exception:
    pass
