---
topic: mcp-development
node_count: 29
version: 1
source_url: https://modelcontextprotocol.io/
description: Building MCP (Model Context Protocol) servers — expose tools, resources, and prompts that Claude can call. Covers fundamentals through production deployment.
goal: ramp them up on building MCP servers — the tools/resources/prompts model and transport choices, then defining tools with input schemas, structured error handling, local testing, packaging, and production distribution
---

# MCP Development Knowledge Graph Schema

This topic covers **building MCP servers** — not just using them, but creating them. MCP (Model Context Protocol) is the standard for giving Claude access to external tools and data. A developer who completes this tree can build, test, and ship an MCP server that any Claude user can install.

---

## Node definitions

29 nodes across 6 branches.

### [ROOT] MCP fundamentals (always unlocked — 5 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|----|-----|
| What MCP is and why it exists | Can explain the difference between tools (Claude calls, returns result), resources (Claude reads, like files), and prompts (reusable templates); knows why MCP exists vs. inline tool definitions | Qualitative | None (ask via gap question) | https://modelcontextprotocol.io/introduction | mcp-development-what-mcp-is-and-why-it-exists |
| Community vs custom server selection | Can make the build-vs-adopt decision: when to use an existing community server (filesystem, GitHub, web search, database) vs. build a purpose-built one; knows the tradeoffs — community servers save time but may be over-scoped or under-maintained; custom servers allow precise tool naming, input schemas, and access control | Qualitative | None | https://modelcontextprotocol.io/introduction | mcp-development-community-vs-custom-server-selection |
| stdio vs. HTTP transport | Knows when to use stdio (local, single-user, low latency) vs. HTTP/SSE (remote, multi-user, persistent); can explain the tradeoff | Qualitative | None (ask via gap question) | https://modelcontextprotocol.io/docs/concepts/transports | mcp-development-stdio-vs-http-transport |
| Installing and testing an existing MCP server | Has installed ≥1 MCP server in Claude Code settings; made a tool call through it; can describe what the server returned | Artifact / Exercise | MCP servers configured in settings → `[~\|artifact]` | https://docs.anthropic.com/en/docs/claude-code/mcp | mcp-development-installing-and-testing-an-existing-mcp-server |
| Reading MCP server output in Claude sessions | Understands how Claude renders tool results; knows the difference between tool output injected into context vs. rendered in UI | Qualitative | None (ask via gap question) | https://modelcontextprotocol.io/docs/concepts/tools | mcp-development-reading-mcp-server-output-in-claude-sessions |

### [A] Building a basic MCP server (unlocks when ROOT ≥ 2 `[✓]` — 8 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|----|-----|
| Project structure for an MCP server | Has a working project skeleton: entry point, dependency declaration, and a way to run it; knows what `mcp` package or SDK to use for their language | Artifact | repo contains MCP-related source files (mcp, modelcontextprotocol imports) → `[~\|artifact]` | https://modelcontextprotocol.io/quickstart/server | mcp-development-project-structure-for-an-mcp-server |
| Defining a tool with name, description, and input schema | Has declared ≥1 tool with a name, a clear description Claude will use to decide when to call it, and a JSON Schema for inputs | Artifact | repo contains MCP tool definition patterns → `[~\|artifact]` | https://modelcontextprotocol.io/docs/concepts/tools | mcp-development-defining-a-tool-with-name-description-and-input-schema |
| Handling tool calls and returning results | Tool handler receives input, executes logic, returns a `content` array with at least a `text` item; server does not crash on valid inputs | Artifact / Exercise | None | https://modelcontextprotocol.io/docs/concepts/tools | mcp-development-handling-tool-calls-and-returning-results |
| Error handling and exit codes | Server returns proper MCP error responses (not unhandled exceptions); knows how MCP errors differ from tool result errors; understands the `isError` flag for communicating tool-level failures vs. protocol-level errors | Artifact | None | https://modelcontextprotocol.io/docs/concepts/tools | mcp-development-error-handling-and-exit-codes |
| isError flag pattern for tool failures | Can explain when to set `isError: true` in a tool response (the tool ran but failed — e.g., resource not found, permission denied) vs. returning a normal error response (the protocol itself failed); knows that `isError: true` allows the agent to decide how to handle the failure rather than treating it as a crash | Qualitative / Artifact | None | https://modelcontextprotocol.io/docs/concepts/tools | mcp-development-iserror-flag-pattern-for-tool-failures |
| Structured error responses: errorCategory, isRetryable | Has included `errorCategory` (e.g., `"network"`, `"permission"`, `"not_found"`) and `isRetryable` (boolean) in tool error payloads alongside a human-readable description; knows why structured errors let a coordinator make intelligent retry/escalation decisions | Qualitative / Artifact | None | https://modelcontextprotocol.io/docs/concepts/tools | mcp-development-structured-error-responses-errorcategory-isretryable |
| Tool distribution: scoped access per agent role | Knows the 4-5 tool limit for reliable agent behavior; has scoped tool access per agent role (e.g., read-only tools for analyzer agents, write tools only for executor agents); understands that large tool lists increase tool selection errors | Qualitative | custom agent definitions with allowedTools > 0 → `[~\|artifact]` | https://modelcontextprotocol.io/docs/concepts/tools | mcp-development-tool-distribution-scoped-access-per-agent-role |
| Testing locally with claude and mcp-inspector | Has run the server locally and verified Claude calls it; has used `mcp-inspector` or equivalent to inspect tool schema and test calls | Exercise | None | https://modelcontextprotocol.io/docs/tools/inspector | mcp-development-testing-locally-with-claude-and-mcp-inspector |

### [B] Advanced tools (unlocks when Branch A ≥ 3 `[✓]` — 5 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|----|-----|
| Tools with complex input schemas | Has defined a tool with nested objects, arrays, or enum constraints in its JSON Schema; Claude correctly passes structured arguments | Artifact | None | https://modelcontextprotocol.io/docs/concepts/tools | mcp-development-tools-with-complex-input-schemas |
| Streaming responses from tools | Server returns a streaming response (multiple content chunks); knows when streaming is worth the complexity vs. a single return | Artifact / Qualitative | None | https://modelcontextprotocol.io/docs/concepts/tools | mcp-development-streaming-responses-from-tools |
| Resources (file/data exposure) | Has implemented ≥1 MCP resource (URI-based data Claude can read, list, or subscribe to); understands resources as structured content catalogs — URI-based dataset enumeration that Claude can browse; knows the key distinction: resources expose data (Claude reads), tools execute actions (Claude calls with arguments) | Artifact | None | https://modelcontextprotocol.io/docs/concepts/resources | mcp-development-resources-file-data-exposure |
| Prompts (reusable prompt templates) | Has defined ≥1 MCP prompt (a parameterized prompt template Claude can invoke); understands the use case vs. system prompts | Artifact | None | https://modelcontextprotocol.io/docs/concepts/prompts | mcp-development-prompts-reusable-prompt-templates |
| Authentication and secrets management | Has handled API keys or auth tokens in a server without hardcoding them; uses env vars or a secrets mechanism the user configures | Artifact / Qualitative | None | https://modelcontextprotocol.io/docs/guides/authentication | mcp-development-authentication-and-secrets-management |

### [C] Production and distribution (unlocks when Branch B ≥ 3 `[✓]` — 3 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|----|-----|
| Packaging for distribution | Has packaged a server for distribution via npm, PyPI, or as a binary; another user can install it in one command | Artifact | package.json or pyproject.toml with MCP server entry → `[~\|artifact]` | https://modelcontextprotocol.io/quickstart/server | mcp-development-packaging-for-distribution |
| Writing a compelling server description | Server's tool descriptions are specific enough that Claude picks the right tool for ambiguous queries without prompting; tested with multiple query phrasings | Exercise / Qualitative | None | https://modelcontextprotocol.io/docs/concepts/tools | mcp-development-writing-a-compelling-server-description |
| CI testing of MCP tool behavior | Has a CI job that starts the server, calls tools programmatically, and asserts on outputs | Artifact | .github/workflows with MCP test patterns → `[~\|artifact]` | https://modelcontextprotocol.io/docs/tools/inspector | mcp-development-ci-testing-of-mcp-tool-behavior |

### [D] Integration patterns (unlocks when Branch C ≥ 2 `[✓]` — 3 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|----|-----|
| Composing multiple MCP servers | Understands that Claude can use multiple MCP servers simultaneously; has configured ≥2 servers and used tools from both in one session | Artifact / Exercise | multiple MCP servers in settings → `[✓\|artifact]` | https://docs.anthropic.com/en/docs/claude-code/mcp | mcp-development-composing-multiple-mcp-servers |
| MCP server for internal APIs | Has built an MCP server that wraps an internal or private API; teammates can use Claude to query the API without knowing its endpoints | Artifact | None | https://modelcontextprotocol.io/quickstart/server | mcp-development-mcp-server-for-internal-apis |
| Claude Code hooks + MCP | Has combined a Claude Code hook (PreToolUse/PostToolUse) with an MCP tool in the same workflow; can explain the interaction | Artifact | hooks + MCP servers both configured → `[~\|artifact]` | https://docs.anthropic.com/en/docs/claude-code/hooks | mcp-development-claude-code-hooks-mcp |

### [E] Advanced MCP topics (unlocks when Branch D ≥ 2 `[✓]` — 5 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|----|-----|
| Sampling: servers requesting LLM completions via the client | Can explain the sampling primitive: an MCP server can request an LLM completion from the client (not from a separate API call); knows the use case — server-side reasoning without the server needing its own LLM credentials; understands the security boundary (client controls sampling, server cannot bypass it) | Qualitative | None | https://modelcontextprotocol.io/docs/concepts/sampling | mcp-development-sampling-servers-requesting-llm-completions-via-the-client |
| Progress and logging notifications: real-time feedback to clients | Has implemented or can describe progress notifications (incremental status updates to the client while a long tool call runs) and logging notifications (structured log messages from server to client); knows why these matter for UX in long-running tools | Qualitative / Artifact | None | https://modelcontextprotocol.io/docs/concepts/notifications | mcp-development-progress-and-logging-notifications-real-time-feedback-to-clients |
| Roots-based file access: permission and security boundary system | Can explain roots: the client declares which file system paths (roots) the server is allowed to access; the server must respect these boundaries; knows this is the primary mechanism for preventing an MCP server from reading arbitrary files on the user's system | Qualitative | None | https://modelcontextprotocol.io/docs/concepts/roots | mcp-development-roots-based-file-access-permission-and-security-boundary-system |
| Transport selection: stdio vs StreamableHTTP tradeoffs | Can make the transport decision: stdio for local single-user servers (no network overhead, process-lifetime scope); StreamableHTTP for remote multi-user servers (survives process restarts, supports server-sent events, scales horizontally); knows that HTTP transport has higher operational complexity | Qualitative | None | https://modelcontextprotocol.io/docs/concepts/transports | mcp-development-transport-selection-stdio-vs-streamablehttp-tradeoffs |
| Production scaling: stateless vs stateful configurations | Can explain the stateless vs. stateful tradeoff: stateless servers (no in-memory session state) can be horizontally scaled and restarted freely; stateful servers (e.g., with in-memory caches or long-lived connections) require sticky sessions or external state storage; knows when each is appropriate | Qualitative | None | https://modelcontextprotocol.io/docs/concepts/transports | mcp-development-production-scaling-stateless-vs-stateful-configurations |

---

## Probes

| name | primitive | args |
|------|-----------|------|
| mcp_user             | json-has-key | ~/.claude.json mcpServers |
| mcp_project          | json-has-key | .mcp.json mcpServers |
| mcp_source_imports   | grep-count   | "from mcp\|import mcp\|modelcontextprotocol" mcp/ src/ |
| mcp_iserror          | grep-count   | "isError" mcp/ src/ |
| agent_allowedtools   | grep-count   | "allowedTools\|allowed-tools" .claude/agents/ |
| mcp_package_manifest | grep-count   | "mcp\|modelcontextprotocol" package.json pyproject.toml |
| mcp_ci               | grep-count   | "mcp\|modelcontextprotocol" .github/workflows/ |
| hooks_project        | json-has-key | .claude/settings.json hooks |
| hooks_global         | json-has-key | ~/.claude/settings.json hooks |

**Notes.** Source probes are scoped to `mcp/` and `src/` on purpose (precision
bias): greping the repo root would match an *installed* `mcp` package under
`.venv/` and false-positive "has built a server" on someone who only installed
one. The closed primitive set cannot count JSON object keys, so "multiple MCP
servers" is approximated by cross-scope presence (`mcp_user` **and**
`mcp_project`) and seeds `[~|artifact]` — config presence does not witness the
criterion's "used tools from both in one session", so teach-back verifies it.

---

## Detection signals

| Collected evidence | Node → status |
|--------------------|---------------|
| mcp_user or mcp_project is true | ROOT: "Installing and testing an existing MCP server" → `[~\|artifact]` |
| mcp_user and mcp_project both true (≥2 server configs) | D: "Composing multiple MCP servers" → `[~\|artifact]` |
| mcp_source_imports > 0 | A: "Project structure" + "Defining a tool" → `[~\|artifact]` |
| mcp_iserror > 0 | A: "isError flag pattern" → `[~\|artifact]` |
| agent_allowedtools > 0 | A: "Tool distribution: scoped access per agent role" → `[~\|artifact]` |
| mcp_package_manifest > 0 | C: "Packaging for distribution" → `[~\|artifact]` |
| mcp_ci > 0 | C: "CI testing" → `[~\|artifact]` |
| (hooks_global or hooks_project) and (mcp_user or mcp_project) | D: "Claude Code hooks + MCP" → `[~\|artifact]` |

---

## Gap questions

| Branch | Gap | Ask this |
|--------|-----|----------|
| [ROOT] | What MCP is | "Explain the three things an MCP server can expose — tools, resources, prompts. What's the difference, and why does MCP exist instead of just inlining tool definitions?" |
| [ROOT] | Build-vs-adopt | "When would you build a custom MCP server rather than adopting an existing community server like the GitHub or filesystem server?" |
| [ROOT] | Transport choice | "Do you know when you'd use stdio transport vs. HTTP for an MCP server? If so, give me one scenario for each." |
| [ROOT] | Installing a server | "Have you installed any MCP servers in Claude Code? If so, which one and what did you use it for?" |
| [ROOT] | Reading output | "When an MCP tool returns a result, where does it go — injected into Claude's context, rendered in the UI, or both? How do you know what Claude actually 'sees'?" |
| [A] | Project structure | "Have you written any part of an MCP server — even a tool skeleton? If so, what language and SDK, and how do you run it?" |
| [A] | Defining a tool | "Walk me through declaring one MCP tool — what three things does it need, and which one does Claude use to decide *when* to call it?" |
| [A] | Handling calls | "Your tool handler receives the input and runs. What shape does it return so Claude gets a usable result — and what keeps the server from crashing on a valid call?" |
| [A] | Error handling | "When a tool call fails partway through — say a database query returns permission denied — how should your MCP server communicate that to the agent? What fields go in the response?" |
| [A] | isError flag | "When do you set `isError: true` in a tool response versus returning a protocol-level error? What does `isError` let the agent do that a crash wouldn't?" |
| [A] | Structured errors | "Beyond a plain message, what would you put in a tool's error payload so a coordinator can decide whether to retry or escalate?" |
| [A] | Tool scoping | "How many tools can an agent reliably choose between, and how do you scope tool access by agent role? Why does a big tool list hurt?" |
| [A] | Local testing | "How do you test an MCP server before shipping it — have you used mcp-inspector or run it against a live Claude session? What did you check?" |
| [B] | Complex schemas | "Have you defined an MCP tool with nested inputs — like an object parameter with required fields, or an enum? If so, what was the schema?" |
| [B] | Streaming | "Have you had a tool return a streaming response — multiple content chunks? When is that worth the extra complexity over a single return?" |
| [B] | Resources | "What's the difference between an MCP resource and an MCP tool? Give an example of something that should be a resource rather than a tool." |
| [B] | Prompts | "Have you defined an MCP prompt — a parameterized template Claude can invoke? How's that different from a system prompt?" |
| [B] | Secrets | "If your MCP server needs an API key, how do you handle it without hardcoding? Where does the secret come from?" |
| [C] | Packaging | "Is your MCP server installable by someone else — via npm, pip, or a binary? If so, how do they install it?" |
| [C] | Description quality | "How do you write tool descriptions specific enough that Claude picks the right tool for an ambiguous query? Have you tested it with different phrasings?" |
| [C] | CI testing | "Do you have CI that starts the server, calls its tools, and asserts on the outputs? What does it check?" |
| [D] | Composing servers | "Have you run two or more MCP servers at once and used tools from both in a single session? What were they?" |
| [D] | Internal API wrapper | "Have you wrapped an internal or private API in an MCP server so teammates can query it through Claude without knowing the endpoints?" |
| [D] | Hooks + MCP | "Have you combined a Claude Code hook with an MCP tool in one workflow? How do the two interact?" |
| [E] | Sampling | "What is MCP sampling, and why would an MCP server use it instead of making its own API call to a language model?" |
| [E] | Notifications | "For a long-running tool, how does the server give the client real-time feedback? What's the difference between progress notifications and logging notifications?" |
| [E] | Roots | "How does the roots system in MCP control what files a server can access? Who declares the roots, and who enforces them?" |
| [E] | Transport tradeoffs | "Beyond local-vs-remote, what makes you pick StreamableHTTP over stdio? What operational cost does HTTP add?" |
| [E] | Scaling | "What's the difference between a stateless and a stateful MCP server for scaling? When does statefulness force you into sticky sessions or external storage?" |

### Qualitative rubric for answers

- **`[✓]` Demonstrated**: Specific, verifiable detail only someone who has done it would know
- **`[~]` Self-reported**: Affirmative but vague
- **`[ ]` Not yet**: Negative, "not sure," or "heard of it but haven't tried"

### Answer → node mapping

| Answer contains | Node → status |
|-----------------|---------------|
| Explains tools vs. resources vs. prompts + why MCP over inline tools | ROOT: "What MCP is and why it exists" → `[✓\|reported]` |
| Specific build-vs-adopt tradeoff with an example | ROOT: "Community vs custom server selection" → `[✓\|reported]` |
| Specific stdio vs. HTTP tradeoff | ROOT: "stdio vs. HTTP transport" → `[✓\|reported]` |
| Specific MCP server name + use case (vague "yes I've installed one" → `[~]`) | ROOT: "Installing and testing" → `[✓\|reported]` |
| Distinguishes context-injected tool output from UI-rendered output | ROOT: "Reading MCP server output" → `[✓\|reported]` |
| Project skeleton described (entry point, deps, run command, SDK) | A: "Project structure" → `[~\|reported]` |
| Names the tool's name/description/input_schema and which drives call selection | A: "Defining a tool with name, description, and input schema" → `[✓\|reported]` |
| Describes returning a content array with a text item, no crash on valid input | A: "Handling tool calls and returning results" → `[✓\|reported]` |
| Specific error-response fields described (isError / structured payload) | A: "Error handling and exit codes" → `[✓\|reported]` |
| Explains `isError: true` (tool ran but failed) vs. protocol error, and what it enables | A: "isError flag pattern for tool failures" → `[✓\|reported]` |
| Names errorCategory + isRetryable and why a coordinator needs them | A: "Structured error responses" → `[✓\|reported]` |
| States the ~4-5 tool limit and scopes access by agent role | A: "Tool distribution: scoped access per agent role" → `[✓\|reported]` |
| Describes testing via mcp-inspector or a live Claude call | A: "Testing locally with claude and mcp-inspector" → `[✓\|reported]` |
| Nested-object or enum input schema described | B: "Tools with complex input schemas" → `[✓\|reported]` |
| Streaming (multi-chunk) response described with the complexity tradeoff | B: "Streaming responses from tools" → `[✓\|reported]` |
| Distinguishes a resource (Claude reads) from a tool (Claude calls) with an example | B: "Resources (file/data exposure)" → `[✓\|reported]` |
| Parameterized MCP prompt described vs. a system prompt | B: "Prompts (reusable prompt templates)" → `[✓\|reported]` |
| Secret handled via env var or user-configured mechanism, not hardcoded | B: "Authentication and secrets management" → `[✓\|reported]` |
| Distribution mechanism described (npm/pip/binary, one-command install) | C: "Packaging for distribution" → `[✓\|reported]` |
| Tool descriptions tuned + tested across phrasings for correct selection | C: "Writing a compelling server description" → `[✓\|reported]` |
| CI that starts the server, calls tools, and asserts outputs described | C: "CI testing of MCP tool behavior" → `[✓\|reported]` |
| ≥2 servers configured and tools from both used in one session | D: "Composing multiple MCP servers" → `[✓\|reported]` |
| Server wrapping an internal or private API described | D: "MCP server for internal APIs" → `[✓\|reported]` |
| Hook + MCP tool combined in one workflow, interaction explained | D: "Claude Code hooks + MCP" → `[✓\|reported]` |
| Explains sampling: server requests a completion via the client + the security boundary | E: "Sampling" → `[✓\|reported]` |
| Progress vs. logging notifications distinguished with a UX rationale | E: "Progress and logging notifications" → `[✓\|reported]` |
| Explains roots: client declares allowed paths, server must respect them | E: "Roots-based file access" → `[✓\|reported]` |
| StreamableHTTP-vs-stdio tradeoff with the operational cost of HTTP | E: "Transport selection: stdio vs StreamableHTTP tradeoffs" → `[✓\|reported]` |
| Stateless vs. stateful scaling tradeoff (sticky sessions / external state) | E: "Production scaling: stateless vs stateful configurations" → `[✓\|reported]` |

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
