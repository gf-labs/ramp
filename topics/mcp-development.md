---
topic: mcp-development
version: 1
source_url: https://modelcontextprotocol.io/
description: Building MCP (Model Context Protocol) servers — expose tools, resources, and prompts that Claude can call. Covers fundamentals through production deployment.
---

# MCP Development Knowledge Tree Schema

This topic covers **building MCP servers** — not just using them, but creating them. MCP (Model Context Protocol) is the standard for giving Claude access to external tools and data. A developer who completes this tree can build, test, and ship an MCP server that any Claude user can install.

---

## Node definitions

20 nodes across 5 branches.

### [ROOT] MCP fundamentals (always unlocked — 4 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|----|
| What MCP is and why it exists | Can explain the difference between tools (Claude calls, returns result), resources (Claude reads, like files), and prompts (reusable templates); knows why MCP exists vs. inline tool definitions | Qualitative | None (ask via gap question) | https://modelcontextprotocol.io/introduction |
| stdio vs. HTTP transport | Knows when to use stdio (local, single-user, low latency) vs. HTTP/SSE (remote, multi-user, persistent); can explain the tradeoff | Qualitative | None (ask via gap question) | https://modelcontextprotocol.io/docs/concepts/transports |
| Installing and testing an existing MCP server | Has installed ≥1 MCP server in Claude Code settings; made a tool call through it; can describe what the server returned | Artifact / Exercise | MCP servers configured in settings → `[~\|artifact]` | https://docs.anthropic.com/en/docs/claude-code/mcp |
| Reading MCP server output in Claude sessions | Understands how Claude renders tool results; knows the difference between tool output injected into context vs. rendered in UI | Qualitative | None (ask via gap question) | https://modelcontextprotocol.io/docs/concepts/tools |

### [A] Building a basic MCP server (unlocks when ROOT ≥ 2 `[✓]` — 5 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|----|
| Project structure for an MCP server | Has a working project skeleton: entry point, dependency declaration, and a way to run it; knows what `mcp` package or SDK to use for their language | Artifact | repo contains MCP-related source files (mcp, modelcontextprotocol imports) → `[~\|artifact]` | https://modelcontextprotocol.io/quickstart/server |
| Defining a tool with name, description, and input schema | Has declared ≥1 tool with a name, a clear description Claude will use to decide when to call it, and a JSON Schema for inputs | Artifact | repo contains MCP tool definition patterns → `[~\|artifact]` | https://modelcontextprotocol.io/docs/concepts/tools |
| Handling tool calls and returning results | Tool handler receives input, executes logic, returns a `content` array with at least a `text` item; server does not crash on valid inputs | Artifact / Exercise | None | https://modelcontextprotocol.io/docs/concepts/tools |
| Error handling and exit codes | Server returns proper MCP error responses (not unhandled exceptions); knows how MCP errors differ from tool result errors | Artifact | None | https://modelcontextprotocol.io/docs/concepts/tools |
| Testing locally with claude and mcp-inspector | Has run the server locally and verified Claude calls it; has used `mcp-inspector` or equivalent to inspect tool schema and test calls | Exercise | None | https://modelcontextprotocol.io/docs/tools/inspector |

### [B] Advanced tools (unlocks when Branch A ≥ 3 `[✓]` — 5 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|----|
| Tools with complex input schemas | Has defined a tool with nested objects, arrays, or enum constraints in its JSON Schema; Claude correctly passes structured arguments | Artifact | None | https://modelcontextprotocol.io/docs/concepts/tools |
| Streaming responses from tools | Server returns a streaming response (multiple content chunks); knows when streaming is worth the complexity vs. a single return | Artifact / Qualitative | None | https://modelcontextprotocol.io/docs/concepts/tools |
| Resources (file/data exposure) | Has implemented ≥1 MCP resource (URI-based data Claude can read); knows the difference between a resource and a tool | Artifact | None | https://modelcontextprotocol.io/docs/concepts/resources |
| Prompts (reusable prompt templates) | Has defined ≥1 MCP prompt (a parameterized prompt template Claude can invoke); understands the use case vs. system prompts | Artifact | None | https://modelcontextprotocol.io/docs/concepts/prompts |
| Authentication and secrets management | Has handled API keys or auth tokens in a server without hardcoding them; uses env vars or a secrets mechanism the user configures | Artifact / Qualitative | None | https://modelcontextprotocol.io/docs/guides/authentication |

### [C] Production and distribution (unlocks when Branch B ≥ 3 `[✓]` — 3 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|----|
| Packaging for distribution | Has packaged a server for distribution via npm, PyPI, or as a binary; another user can install it in one command | Artifact | package.json or pyproject.toml with MCP server entry → `[~\|artifact]` | https://modelcontextprotocol.io/quickstart/server |
| Writing a compelling server description | Server's tool descriptions are specific enough that Claude picks the right tool for ambiguous queries without prompting; tested with multiple query phrasings | Exercise / Qualitative | None | https://modelcontextprotocol.io/docs/concepts/tools |
| CI testing of MCP tool behavior | Has a CI job that starts the server, calls tools programmatically, and asserts on outputs | Artifact | .github/workflows with MCP test patterns → `[~\|artifact]` | https://modelcontextprotocol.io/docs/tools/inspector |

### [D] Integration patterns (unlocks when Branch C ≥ 2 `[✓]` — 3 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|----|
| Composing multiple MCP servers | Understands that Claude can use multiple MCP servers simultaneously; has configured ≥2 servers and used tools from both in one session | Artifact / Exercise | multiple MCP servers in settings → `[✓\|artifact]` | https://docs.anthropic.com/en/docs/claude-code/mcp |
| MCP server for internal APIs | Has built an MCP server that wraps an internal or private API; teammates can use Claude to query the API without knowing its endpoints | Artifact | None | https://modelcontextprotocol.io/quickstart/server |
| Claude Code hooks + MCP | Has combined a Claude Code hook (PreToolUse/PostToolUse) with an MCP tool in the same workflow; can explain the interaction | Artifact | hooks + MCP servers both configured → `[~\|artifact]` | https://docs.anthropic.com/en/docs/claude-code/hooks |

---

## Detection signals

| Collected evidence | Node → status |
|--------------------|---------------|
| MCP servers configured in Claude settings | ROOT: "Installing and testing an existing server" → `[~\|artifact]` |
| Multiple MCP servers configured | D: "Composing multiple MCP servers" → `[✓\|artifact]` |
| repo contains MCP-related source files | A: "Project structure" + "Defining a tool" → `[~\|artifact]` |
| package.json or pyproject.toml with MCP patterns | C: "Packaging for distribution" → `[~\|artifact]` |
| .github/workflows with MCP test patterns | C: "CI testing" → `[~\|artifact]` |
| hooks + MCP servers both configured | D: "Claude Code hooks + MCP" → `[~\|artifact]` |

---

## Gap questions

| Branch | Gap | Ask this |
|--------|-----|----------|
| [ROOT] | No MCP server usage evidence | "Have you installed any MCP servers in Claude Code? If so, which one and what did you use it for?" |
| [ROOT] | No transport knowledge | "Do you know when you'd use stdio transport vs. HTTP for an MCP server? If so, give me one scenario for each." |
| [A] | No MCP implementation evidence | "Have you written any part of an MCP server — even a tool skeleton? If so, what language and what did the tool do?" |
| [B] | No advanced schema evidence | "Have you defined an MCP tool with nested inputs — like an object parameter with required fields? If so, what was the schema?" |
| [C] | No distribution evidence | "Is your MCP server installable by someone else — via npm, pip, or a binary? If so, how do they install it?" |

### Qualitative rubric for answers

- **`[✓]` Demonstrated**: Specific, verifiable detail only someone who has done it would know
- **`[~]` Self-reported**: Affirmative but vague
- **`[ ]` Not yet**: Negative, "not sure," or "heard of it but haven't tried"

### Answer → node mapping

| Answer contains | Node → status |
|-----------------|---------------|
| Specific MCP server name + use case | ROOT: "Installing and testing" → `[✓\|reported]` |
| Vague "yes, I've installed MCP servers" | ROOT: "Installing and testing" → `[~\|reported]` |
| Specific stdio vs. HTTP tradeoff | ROOT: "stdio vs. HTTP transport" → `[✓\|reported]` |
| Vague awareness of transports | ROOT: "stdio vs. HTTP transport" → `[~\|reported]` |
| Describes a tool definition (name, schema, handler) | A: "Project structure" + "Defining a tool" + "Handling calls" → `[~\|reported]` |
| Specific error handling or schema detail | A: "Error handling" or "Complex schemas" → `[✓\|reported]` |
| Distribution mechanism described | C: "Packaging" → `[✓\|reported]` |

---

## Unlock thresholds

- Branch A unlocks when ROOT ≥ 2 `[✓]`
- Branch B unlocks when Branch A ≥ 3 `[✓]`
- Branch C unlocks when Branch B ≥ 3 `[✓]`
- Branch D unlocks when Branch C ≥ 2 `[✓]`

Both `[✓]` and `[~]` count toward unlock thresholds.

---

## Tier definitions

| Tier | Criterion |
|------|-----------|
| Explorer | ROOT incomplete — knows MCP exists but hasn't installed or built anything |
| Builder | Has installed servers and built a basic tool server that works locally |
| Practitioner | Handles advanced schemas, resources, and prompts; server is production-ready |
| Expert | Ships distributable servers; CI-tested; designs for composition and internal API integration |

---

## Tree render template

```
[ROOT] MCP fundamentals
    [?] What MCP is and why it exists
    [?] stdio vs. HTTP transport
    [?] Installing and testing an existing MCP server
    [?] Reading MCP server output in Claude sessions

[A] Building a basic MCP server   [if locked: "(unlock: complete 2 MCP fundamentals)"]
    [?] Project structure for an MCP server
    [?] Defining a tool with name, description, and input schema
    [?] Handling tool calls and returning results
    [?] Error handling and exit codes
    [?] Testing locally with claude and mcp-inspector

[B] Advanced tools   [if locked: "(unlock: complete 3 Basic Server skills)"]
    [?] Tools with complex input schemas
    [?] Streaming responses from tools
    [?] Resources (file/data exposure)
    [?] Prompts (reusable prompt templates)
    [?] Authentication and secrets management

[C] Production and distribution   [if locked: "(unlock: complete 3 Advanced Tools skills)"]
    [?] Packaging for distribution
    [?] Writing a compelling server description
    [?] CI testing of MCP tool behavior

[D] Integration patterns   [if locked: "(unlock: complete 2 Production skills)"]
    [?] Composing multiple MCP servers
    [?] MCP server for internal APIs
    [?] Claude Code hooks + MCP
```

Replace every `[?]` with: `[✓]`, `[~]`, `[ ]`, `[★]`, or `[·]`.
If a branch is fully locked (`[·]`), collapse it to just the branch header line.

---

## Saved tree file template

When writing to `~/.claude/knowledge-graphs/mcp-development.md`, use this format:

```markdown
---
version: 3
topic: mcp-development
user: [git config user.name or "unknown"]
email: [git config user.email or "unknown"]
updated: [today's date YYYY-MM-DD]
level: [Explorer / Builder / Practitioner / Expert]
xp: [CURRENT_XP]
---

# MCP Development Knowledge Tree

*[✓] Demonstrated · [~] Self-reported · [ ] Not yet · [★] Mastery target · [·] Locked*

## [ROOT] MCP fundamentals
- [STATUS|TYPE] What MCP is and why it exists
- [STATUS|TYPE] stdio vs. HTTP transport
- [STATUS|TYPE] Installing and testing an existing MCP server
- [STATUS|TYPE] Reading MCP server output in Claude sessions

## [A] Building a basic MCP server
- [STATUS|TYPE] Project structure for an MCP server
- [STATUS|TYPE] Defining a tool with name, description, and input schema
- [STATUS|TYPE] Handling tool calls and returning results
- [STATUS|TYPE] Error handling and exit codes
- [STATUS|TYPE] Testing locally with claude and mcp-inspector

## [B] Advanced tools
- [STATUS|TYPE] Tools with complex input schemas
- [STATUS|TYPE] Streaming responses from tools
- [STATUS|TYPE] Resources (file/data exposure)
- [STATUS|TYPE] Prompts (reusable prompt templates)
- [STATUS|TYPE] Authentication and secrets management

## [C] Production and distribution
- [STATUS|TYPE] Packaging for distribution
- [STATUS|TYPE] Writing a compelling server description
- [STATUS|TYPE] CI testing of MCP tool behavior

## [D] Integration patterns
- [STATUS|TYPE] Composing multiple MCP servers
- [STATUS|TYPE] MCP server for internal APIs
- [STATUS|TYPE] Claude Code hooks + MCP

## Frontier
- [frontier node name] — [criterion one-liner]

## Notes
<!-- Add personal notes here -->
```

**Demonstration evidence trail:** For `[✓]` nodes only, append `— [repo-name], [YYYY-MM-DD]: [brief note] | next: [YYYY-MM-DD] [L1]`.
Spaced repetition levels: L1=1d, L2=3d, L3=7d, L4=21d, L5=60d, L6=permanent.
