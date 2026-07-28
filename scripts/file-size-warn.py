#!/usr/bin/env python3
"""
PostToolUse hook — warns when a .md file exceeds 600 lines.

Receives the hook event as JSON on stdin (Edit|Write matcher). On breach it
prints one line to stderr and exits 2 — PostToolUse runs after the write, so
nothing is blocked, but exit-2 stderr is fed back to Claude (M3: stdout on
exit 0 only reaches the debug transcript, so the old always-print version was
never seen). At or under the limit it exits 0 silently.
"""
import json
import os
import sys
from pathlib import Path

LIMIT = 600


def main(stdin=None) -> int:
    stream = stdin if stdin is not None else sys.stdin
    try:
        data = json.loads(stream.read() or "{}")
        tool_input = data.get("tool_input", {})
        path = tool_input.get("file_path") or tool_input.get("path", "")
        if path and path.endswith(".md") and Path(path).exists():
            with open(path, encoding="utf-8", errors="replace") as fh:
                lines = sum(1 for _ in fh)
            if lines > LIMIT:
                name = os.path.basename(path)
                print(
                    f"[ramp] {name}: {lines} lines — prompt files should stay "
                    f"focused; consider splitting (limit {LIMIT})",
                    file=sys.stderr,
                )
                return 2
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
