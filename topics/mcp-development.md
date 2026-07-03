---
topic: mcp-development
node_count: 29
version: 1
source_url: https://modelcontextprotocol.io/
description: Building MCP (Model Context Protocol) servers — expose tools, resources, and prompts that Claude can call. Covers fundamentals through production deployment.
---

# MCP Development Knowledge Graph Schema

This topic covers **building MCP servers** — not just using them, but creating them. MCP (Model Context Protocol) is the standard for giving Claude access to external tools and data. A developer who completes this tree can build, test, and ship an MCP server that any Claude user can install.

---

## Node definitions

29 nodes across 6 branches.

### [ROOT] MCP fundamentals (always unlocked — 5 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|----|
| What MCP is and why it exists | Can explain the difference between tools (Claude calls, returns result), resources (Claude reads, like files), and prompts (reusable templates); knows why MCP exists vs. inline tool definitions | Qualitative | None (ask via gap question) | https://modelcontextprotocol.io/introduction |
| Community vs custom server selection | Can make the build-vs-adopt decision: when to use an existing community server (filesystem, GitHub, web search, database) vs. build a purpose-built one; knows the tradeoffs — community servers save time but may be over-scoped or under-maintained; custom servers allow precise tool naming, input schemas, and access control | Qualitative | None | https://modelcontextprotocol.io/introduction |
| stdio vs. HTTP transport | Knows when to use stdio (local, single-user, low latency) vs. HTTP/SSE (remote, multi-user, persistent); can explain the tradeoff | Qualitative | None (ask via gap question) | https://modelcontextprotocol.io/docs/concepts/transports |
| Installing and testing an existing MCP server | Has installed ≥1 MCP server in Claude Code settings; made a tool call through it; can describe what the server returned | Artifact / Exercise | MCP servers configured in settings → `[~\|artifact]` | https://docs.anthropic.com/en/docs/claude-code/mcp |
| Reading MCP server output in Claude sessions | Understands how Claude renders tool results; knows the difference between tool output injected into context vs. rendered in UI | Qualitative | None (ask via gap question) | https://modelcontextprotocol.io/docs/concepts/tools |

### [A] Building a basic MCP server (unlocks when ROOT ≥ 2 `[✓]` — 8 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|----|
| Project structure for an MCP server | Has a working project skeleton: entry point, dependency declaration, and a way to run it; knows what `mcp` package or SDK to use for their language | Artifact | repo contains MCP-related source files (mcp, modelcontextprotocol imports) → `[~\|artifact]` | https://modelcontextprotocol.io/quickstart/server |
| Defining a tool with name, description, and input schema | Has declared ≥1 tool with a name, a clear description Claude will use to decide when to call it, and a JSON Schema for inputs | Artifact | repo contains MCP tool definition patterns → `[~\|artifact]` | https://modelcontextprotocol.io/docs/concepts/tools |
| Handling tool calls and returning results | Tool handler receives input, executes logic, returns a `content` array with at least a `text` item; server does not crash on valid inputs | Artifact / Exercise | None | https://modelcontextprotocol.io/docs/concepts/tools |
| Error handling and exit codes | Server returns proper MCP error responses (not unhandled exceptions); knows how MCP errors differ from tool result errors; understands the `isError` flag for communicating tool-level failures vs. protocol-level errors | Artifact | None | https://modelcontextprotocol.io/docs/concepts/tools |
| isError flag pattern for tool failures | Can explain when to set `isError: true` in a tool response (the tool ran but failed — e.g., resource not found, permission denied) vs. returning a normal error response (the protocol itself failed); knows that `isError: true` allows the agent to decide how to handle the failure rather than treating it as a crash | Qualitative / Artifact | None | https://modelcontextprotocol.io/docs/concepts/tools |
| Structured error responses: errorCategory, isRetryable | Has included `errorCategory` (e.g., `"network"`, `"permission"`, `"not_found"`) and `isRetryable` (boolean) in tool error payloads alongside a human-readable description; knows why structured errors let a coordinator make intelligent retry/escalation decisions | Qualitative / Artifact | None | https://modelcontextprotocol.io/docs/concepts/tools |
| Tool distribution: scoped access per agent role | Knows the 4-5 tool limit for reliable agent behavior; has scoped tool access per agent role (e.g., read-only tools for analyzer agents, write tools only for executor agents); understands that large tool lists increase tool selection errors | Qualitative | custom agent definitions with allowedTools > 0 → `[~\|artifact]` | https://modelcontextprotocol.io/docs/concepts/tools |
| Testing locally with claude and mcp-inspector | Has run the server locally and verified Claude calls it; has used `mcp-inspector` or equivalent to inspect tool schema and test calls | Exercise | None | https://modelcontextprotocol.io/docs/tools/inspector |

### [B] Advanced tools (unlocks when Branch A ≥ 3 `[✓]` — 5 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|----|
| Tools with complex input schemas | Has defined a tool with nested objects, arrays, or enum constraints in its JSON Schema; Claude correctly passes structured arguments | Artifact | None | https://modelcontextprotocol.io/docs/concepts/tools |
| Streaming responses from tools | Server returns a streaming response (multiple content chunks); knows when streaming is worth the complexity vs. a single return | Artifact / Qualitative | None | https://modelcontextprotocol.io/docs/concepts/tools |
| Resources (file/data exposure) | Has implemented ≥1 MCP resource (URI-based data Claude can read, list, or subscribe to); understands resources as structured content catalogs — URI-based dataset enumeration that Claude can browse; knows the key distinction: resources expose data (Claude reads), tools execute actions (Claude calls with arguments) | Artifact | None | https://modelcontextprotocol.io/docs/concepts/resources |
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

### [E] Advanced MCP topics (unlocks when Branch D ≥ 2 `[✓]` — 5 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|----|
| Sampling: servers requesting LLM completions via the client | Can explain the sampling primitive: an MCP server can request an LLM completion from the client (not from a separate API call); knows the use case — server-side reasoning without the server needing its own LLM credentials; understands the security boundary (client controls sampling, server cannot bypass it) | Qualitative | None | https://modelcontextprotocol.io/docs/concepts/sampling |
| Progress and logging notifications: real-time feedback to clients | Has implemented or can describe progress notifications (incremental status updates to the client while a long tool call runs) and logging notifications (structured log messages from server to client); knows why these matter for UX in long-running tools | Qualitative / Artifact | None | https://modelcontextprotocol.io/docs/concepts/notifications |
| Roots-based file access: permission and security boundary system | Can explain roots: the client declares which file system paths (roots) the server is allowed to access; the server must respect these boundaries; knows this is the primary mechanism for preventing an MCP server from reading arbitrary files on the user's system | Qualitative | None | https://modelcontextprotocol.io/docs/concepts/roots |
| Transport selection: stdio vs StreamableHTTP tradeoffs | Can make the transport decision: stdio for local single-user servers (no network overhead, process-lifetime scope); StreamableHTTP for remote multi-user servers (survives process restarts, supports server-sent events, scales horizontally); knows that HTTP transport has higher operational complexity | Qualitative | None | https://modelcontextprotocol.io/docs/concepts/transports |
| Production scaling: stateless vs stateful configurations | Can explain the stateless vs. stateful tradeoff: stateless servers (no in-memory session state) can be horizontally scaled and restarted freely; stateful servers (e.g., with in-memory caches or long-lived connections) require sticky sessions or external state storage; knows when each is appropriate | Qualitative | None | https://modelcontextprotocol.io/docs/concepts/transports |

---

## Detection signals

| Collected evidence | Node → status |
|--------------------|---------------|
| MCP servers configured in Claude settings | ROOT: "Installing and testing an existing server" → `[~\|artifact]` |
| Multiple MCP servers configured | D: "Composing multiple MCP servers" → `[✓\|artifact]` |
| repo contains MCP-related source files | A: "Project structure" + "Defining a tool" → `[~\|artifact]` |
| repo contains `isError` in MCP tool handlers | A: "isError flag pattern" → `[~\|artifact]` |
| custom agent definitions with allowedTools | A: "Tool distribution: scoped access per agent role" → `[~\|artifact]` |
| package.json or pyproject.toml with MCP patterns | C: "Packaging for distribution" → `[~\|artifact]` |
| .github/workflows with MCP test patterns | C: "CI testing" → `[~\|artifact]` |
| hooks + MCP servers both configured | D: "Claude Code hooks + MCP" → `[~\|artifact]` |

---

## Gap questions

| Branch | Gap | Ask this |
|--------|-----|----------|
| [ROOT] | No MCP server usage evidence | "Have you installed any MCP servers in Claude Code? If so, which one and what did you use it for?" |
| [ROOT] | No build-vs-adopt decision evidence | "When would you build a custom MCP server rather than adopting an existing community server like the GitHub or filesystem server?" |
| [ROOT] | No transport knowledge | "Do you know when you'd use stdio transport vs. HTTP for an MCP server? If so, give me one scenario for each." |
| [A] | No MCP implementation evidence | "Have you written any part of an MCP server — even a tool skeleton? If so, what language and what did the tool do?" |
| [A] | No error handling evidence | "When a tool call fails partway through — say a database query returns permission denied — how should your MCP server communicate that to the agent? What fields go in the response?" |
| [B] | No advanced schema evidence | "Have you defined an MCP tool with nested inputs — like an object parameter with required fields? If so, what was the schema?" |
| [B] | No resources evidence | "What's the difference between an MCP resource and an MCP tool? Give an example of something that should be a resource rather than a tool." |
| [C] | No distribution evidence | "Is your MCP server installable by someone else — via npm, pip, or a binary? If so, how do they install it?" |
| [E] | No sampling evidence | "What is MCP sampling, and why would an MCP server use it instead of making its own API call to a language model?" |
| [E] | No roots evidence | "How does the roots system in MCP control what files a server can access? Who declares the roots, and who enforces them?" |

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
- Branch E unlocks when Branch D ≥ 2 `[✓]`

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
MCP fundamentals
    [?] What MCP is and why it exists
    [?] Community vs custom server selection
    [?] stdio vs. HTTP transport
    [?] Installing and testing an existing MCP server
    [?] Reading MCP server output in Claude sessions

Building a basic MCP server   [if locked: "(unlock: complete 2 MCP fundamentals)"]
    [?] Project structure for an MCP server
    [?] Defining a tool with name, description, and input schema
    [?] Handling tool calls and returning results
    [?] Error handling and exit codes
    [?] isError flag pattern for tool failures
    [?] Structured error responses: errorCategory, isRetryable
    [?] Tool distribution: scoped access per agent role
    [?] Testing locally with claude and mcp-inspector

Advanced tools   [if locked: "(unlock: complete 3 Basic Server skills)"]
    [?] Tools with complex input schemas
    [?] Streaming responses from tools
    [?] Resources (file/data exposure)
    [?] Prompts (reusable prompt templates)
    [?] Authentication and secrets management

Production and distribution   [if locked: "(unlock: complete 3 Advanced Tools skills)"]
    [?] Packaging for distribution
    [?] Writing a compelling server description
    [?] CI testing of MCP tool behavior

Integration patterns   [if locked: "(unlock: complete 2 Production skills)"]
    [?] Composing multiple MCP servers
    [?] MCP server for internal APIs
    [?] Claude Code hooks + MCP

Advanced MCP topics   [if locked: "(unlock: complete 2 Integration patterns)"]
    [?] Sampling: servers requesting LLM completions via the client
    [?] Progress and logging notifications: real-time feedback to clients
    [?] Roots-based file access: permission and security boundary system
    [?] Transport selection: stdio vs StreamableHTTP tradeoffs
    [?] Production scaling: stateless vs stateful configurations
```

Replace every `[?]` with: `[✓]`, `[~]`, `[ ]`, `[★]`, or `[·]`.
If a branch is fully locked (`[·]`), collapse it to just the branch header line.

---

## Saved tree file template

When writing to `~/.claude/ramp/graphs/mcp-development.md`, use this format:

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

# MCP Development Knowledge Graph

*[✓] Demonstrated · [~] Self-reported · [ ] Not yet · [★] Mastery target · [·] Locked*

## [ROOT] MCP fundamentals
- [STATUS|TYPE] What MCP is and why it exists
- [STATUS|TYPE] Community vs custom server selection
- [STATUS|TYPE] stdio vs. HTTP transport
- [STATUS|TYPE] Installing and testing an existing MCP server
- [STATUS|TYPE] Reading MCP server output in Claude sessions

## [A] Building a basic MCP server
- [STATUS|TYPE] Project structure for an MCP server
- [STATUS|TYPE] Defining a tool with name, description, and input schema
- [STATUS|TYPE] Handling tool calls and returning results
- [STATUS|TYPE] Error handling and exit codes
- [STATUS|TYPE] isError flag pattern for tool failures
- [STATUS|TYPE] Structured error responses: errorCategory, isRetryable
- [STATUS|TYPE] Tool distribution: scoped access per agent role
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

## [E] Advanced MCP topics
- [STATUS|TYPE] Sampling: servers requesting LLM completions via the client
- [STATUS|TYPE] Progress and logging notifications: real-time feedback to clients
- [STATUS|TYPE] Roots-based file access: permission and security boundary system
- [STATUS|TYPE] Transport selection: stdio vs StreamableHTTP tradeoffs
- [STATUS|TYPE] Production scaling: stateless vs stateful configurations

## Frontier
- [frontier node name] — [criterion one-liner]

## Notes
<!-- Add personal notes here -->
```

**Demonstration evidence trail:** For `[✓]` nodes only, append `— [repo-name], [YYYY-MM-DD]: [brief note] | next: [YYYY-MM-DD] [L1]`.
Spaced repetition levels: L1=1d, L2=3d, L3=7d, L4=21d, L5=60d, L6=permanent.
