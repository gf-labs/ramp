---
version: 3
topic: claude-code
repo: ramp
updated: 2026-03-15
---

# claude-code Knowledge Graph — ramp

*Project evidence log — nodes demonstrated in this codebase. Merges with personal tree on /ramp:up run.*

## Evidence

- [✓|exercise] Troubleshooting: diagnose and recover — ramp, 2026-03-15: traced MCP not loading to ~/.claude.json vs settings.json; verified with claude mcp get + JSON-RPC handshake test; diagnosed stale sup paths; registered via claude mcp add -s user; fixed setup-mcp.py for idempotency | next: 2026-03-16 [L1]
- [✓|artifact] MCP: configure and use servers — ramp, 2026-03-15: registered via claude mcp add -s user; writes to ~/.claude.json; verified connected via claude mcp get | next: 2026-03-07 [L1]
- [✓|artifact] MCP project config (.mcp.json) — ramp, 2026-03-15: correct registration is claude mcp add -s user → ~/.claude.json; scope model: local/user/project | next: 2026-03-07 [L1]
- [✓|artifact] Hook handler scripts (stdin, exit codes, response) — ramp, 2026-03-15: wrote setup-mcp.py as idempotent SessionStart hook; checks ~/.claude.json directly, calls claude mcp add -s user | next: 2026-03-07 [L1]
