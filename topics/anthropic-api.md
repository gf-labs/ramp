---
topic: anthropic-api
node_count: 18
version: 1
source_url: https://docs.anthropic.com/en/api/
description: Using the Claude API and Anthropic SDK to build custom applications, pipelines, and agentic systems — from basic completions through production tool-use loops.
goal: ramp them up on building with the Claude API — authenticated completion requests and model choice, then system prompts, multi-turn and streaming, the tool-use loop, and production patterns like prompt caching and batching
---

# Anthropic API Knowledge Graph Schema

This topic covers **building with the Claude API** — making completion requests, handling tool use, managing multi-turn conversations, and deploying production pipelines. A developer who completes this tree can build a reliable Claude-powered application from scratch.

---

## Node definitions

18 nodes across 4 branches.

### [ROOT] API fundamentals (always unlocked — 4 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|----|-----|
| Authentication and API key management | Has made an authenticated API request; stores key via env var (not hardcoded); knows the `ANTHROPIC_API_KEY` convention | Artifact / Exercise | `from anthropic` or `@anthropic-ai` import in repo → `[~\|artifact]` | https://docs.anthropic.com/en/api/getting-started | anthropic-api-authentication-and-api-key-management |
| Making a basic completion request | Has called `messages.create()` (or equivalent); received a response; can read the `content[0].text` field | Exercise | repo contains messages.create or similar patterns → `[~\|artifact]` | https://docs.anthropic.com/en/api/messages | anthropic-api-making-a-basic-completion-request |
| Model selection (which model for which use case) | Can explain when to use Haiku (fast, cheap, simple tasks) vs. Sonnet (balanced) vs. Opus (complex reasoning); has chosen a model with a reason | Qualitative | model specified in code → `[~\|artifact]` | https://docs.anthropic.com/en/docs/about-claude/models | anthropic-api-model-selection-which-model-for-which-use-case |
| Understanding tokens, context windows, and costs | Knows what tokens are; understands the context window limit for their chosen model; has checked cost estimates for their use case | Qualitative | None (ask via gap question) | https://docs.anthropic.com/en/docs/about-claude/models | anthropic-api-understanding-tokens-context-windows-and-costs |

### [A] Core API patterns (unlocks when ROOT ≥ 2 `[✓]` — 5 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|----|-----|
| System prompts and their effect on behavior | Has written a system prompt that meaningfully changes Claude's output format or persona; knows the system prompt is separate from the first user turn | Artifact / Exercise | repo contains system prompt patterns → `[~\|artifact]` | https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts | anthropic-api-system-prompts-and-their-effect-on-behavior |
| Multi-turn conversations (message history management) | Has built a conversation that sends the full message history on each request; understands why context must be managed manually (API is stateless) | Artifact | repo contains conversation history accumulation patterns → `[~\|artifact]` | https://docs.anthropic.com/en/api/messages | anthropic-api-multi-turn-conversations-message-history-management |
| Streaming responses | Has received a streaming response; processes events incrementally (text_delta, etc.); knows the tradeoff: streaming = lower latency, higher complexity | Artifact / Exercise | repo contains streaming/stream patterns → `[~\|artifact]` | https://docs.anthropic.com/en/api/messages-stream | anthropic-api-streaming-responses |
| Stop sequences and max tokens | Has used `stop_sequences` to control where the response ends; has set `max_tokens` explicitly; knows what happens at the limit | Artifact / Qualitative | None | https://docs.anthropic.com/en/api/messages | anthropic-api-stop-sequences-and-max-tokens |
| Handling API errors and rate limits | Handles `APIStatusError`, `RateLimitError`, and timeout gracefully; has implemented exponential backoff or retry logic | Artifact | repo contains error handling for API calls → `[~\|artifact]` | https://docs.anthropic.com/en/api/errors | anthropic-api-handling-api-errors-and-rate-limits |

### [B] Tool use (unlocks when Branch A ≥ 3 `[✓]` — 5 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|----|-----|
| Defining tools (name, description, input schema) | Has defined ≥1 tool with a clear name, a description Claude uses to decide when to call it, and a valid `input_schema` (JSON Schema) | Artifact | repo contains tool definition objects → `[~\|artifact]` | https://docs.anthropic.com/en/docs/build-with-claude/tool-use | anthropic-api-defining-tools-name-description-input-schema |
| Parsing tool_use blocks from responses | Correctly identifies `stop_reason: "tool_use"` in the response; extracts `tool_use` content block name and `input` dict | Artifact | None | https://docs.anthropic.com/en/docs/build-with-claude/tool-use | anthropic-api-parsing-tool-use-blocks-from-responses |
| Executing tools and returning tool_result blocks | Executes the tool logic and returns a `tool_result` content block with the `tool_use_id` correctly set; conversation continues | Artifact | None | https://docs.anthropic.com/en/docs/build-with-claude/tool-use | anthropic-api-executing-tools-and-returning-tool-result-blocks |
| Agentic loops (repeated tool use until task completion) | Has implemented a loop: send message → check stop_reason → execute tool → append result → send again; loop terminates on `end_turn` | Artifact | repo contains agentic loop patterns → `[~\|artifact]` | https://docs.anthropic.com/en/docs/build-with-claude/tool-use | anthropic-api-agentic-loops-repeated-tool-use-until-task-completion |
| Parallel tool use | Claude returns multiple `tool_use` blocks in one response; all are executed and returned in a single `tool_result` list before continuing | Artifact / Qualitative | None | https://docs.anthropic.com/en/docs/build-with-claude/tool-use | anthropic-api-parallel-tool-use |

### [C] Production patterns (unlocks when Branch B ≥ 3 `[✓]` — 4 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|----|-----|
| Prompt caching (cost reduction) | Has enabled prompt caching on a long system prompt or repeated context block; knows `cache_control: {type: "ephemeral"}`; has measured cost reduction | Artifact | repo contains cache_control patterns → `[✓\|artifact]` | https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching | anthropic-api-prompt-caching-cost-reduction |
| Batching requests for throughput | Has used the Batch API for offline/async workloads; knows when batch is better than real-time (latency tolerance vs. cost) | Artifact | repo contains batch API patterns → `[✓\|artifact]` | https://docs.anthropic.com/en/api/creating-message-batches | anthropic-api-batching-requests-for-throughput |
| Evaluating outputs programmatically | Has a structured eval: test cases with expected outputs (or criteria), Claude responses, and a scoring function; can iterate on prompts based on scores | Artifact / Exercise | repo contains eval patterns → `[~\|artifact]` | https://docs.anthropic.com/en/docs/build-with-claude/develop-tests | anthropic-api-evaluating-outputs-programmatically |
| Safety and content policy in production | Has reviewed the usage policies; has a plan for handling refusals (catching API errors vs. checking `stop_reason`); understands what Claude won't do by default | Qualitative | None (ask via gap question) | https://docs.anthropic.com/en/docs/about-claude/safety-and-usage-policies | anthropic-api-safety-and-content-policy-in-production |

---

## Probes

| name | primitive | args |
|------|-----------|------|
| sdk_import         | grep-count | "from anthropic\|import anthropic\|@anthropic-ai/sdk" src/ app/ lib/ scripts/ |
| messages_create    | grep-count | "messages.create\|messages.stream" src/ app/ lib/ scripts/ |
| model_specified    | grep-count | "claude-3\|claude-sonnet\|claude-opus\|claude-haiku" src/ app/ lib/ scripts/ |
| system_prompt      | grep-count | "system=" src/ app/ lib/ scripts/ |
| conversation_hist  | grep-count | "messages.append" src/ app/ lib/ scripts/ |
| streaming          | grep-count | "text_delta\|messages.stream\|stream=True" src/ app/ lib/ scripts/ |
| api_error_handling | grep-count | "RateLimitError\|APIStatusError\|APIError" src/ app/ lib/ scripts/ |
| tool_definitions   | grep-count | "input_schema" src/ app/ lib/ scripts/ |
| agentic_loop       | grep-count | "stop_reason\|tool_use_id" src/ app/ lib/ scripts/ |
| cache_control      | grep-count | "cache_control" src/ app/ lib/ scripts/ |
| batch_api          | grep-count | "batches.create\|message-batches" src/ app/ lib/ scripts/ |

**Notes.** Grep probes are scoped to `src/ app/ lib/ scripts/`, not the repo root:
`grep-count` recurses into dot-dirs, so scanning `.` would descend into `.venv/`
and false-positive `sdk_import` on a merely *installed* SDK. The tradeoff is
precision over recall — a project that keeps API code only at the repo root
won't auto-seed and is caught by the gap questions instead. The `[✓|artifact]`
seeds (`cache_control`, batch API) are strong direct witnesses of the act; the
rest seed `[~|artifact]`. "Evaluating outputs" has no precise code signature and
is left to teach-back.

---

## Detection signals

| Collected evidence | Node → status |
|--------------------|---------------|
| sdk_import > 0 | ROOT: "Authentication and API key management" → `[~\|artifact]` |
| messages_create > 0 | ROOT: "Making a basic completion request" → `[~\|artifact]` |
| model_specified > 0 | ROOT: "Model selection (which model for which use case)" → `[~\|artifact]` |
| system_prompt > 0 | A: "System prompts" → `[~\|artifact]` |
| conversation_hist > 0 | A: "Multi-turn conversations" → `[~\|artifact]` |
| streaming > 0 | A: "Streaming responses" → `[~\|artifact]` |
| api_error_handling > 0 | A: "Handling API errors and rate limits" → `[~\|artifact]` |
| tool_definitions > 0 | B: "Defining tools" → `[~\|artifact]` |
| agentic_loop > 0 | B: "Agentic loops" → `[~\|artifact]` |
| cache_control > 0 | C: "Prompt caching" → `[✓\|artifact]` |
| batch_api > 0 | C: "Batching requests" → `[✓\|artifact]` |

---

## Gap questions

| Branch | Gap | Ask this |
|--------|-----|----------|
| [ROOT] | No API usage evidence | "Have you made a Claude API call directly — not through Claude Code, but via the SDK or HTTP? If so, what were you building?" |
| [ROOT] | No model selection evidence | "Have you chosen between Haiku, Sonnet, and Opus for a specific use case? If so, what was the task and why did you pick that model?" |
| [ROOT] | No token/cost awareness | "Do you know the context window size for the Claude model you're using, and roughly what it costs per 1M tokens?" |
| [A] | No system prompt evidence | "Have you written a system prompt that changed how Claude responds — like giving it a persona or constraining its output format?" |
| [B] | No tool use evidence | "Have you implemented tool use (function calling) with the API — where Claude returns a tool call and you execute it? If so, what did the tool do?" |
| [C] | No production pattern evidence | "Have you implemented prompt caching or the Batch API to reduce costs or improve throughput in a production workload?" |

### Qualitative rubric for answers

- **`[✓]` Demonstrated**: Specific, verifiable detail only someone who has done it would know
- **`[~]` Self-reported**: Affirmative but vague
- **`[ ]` Not yet**: Negative, "not sure," or "heard of it but haven't tried"

### Answer → node mapping

| Answer contains | Node → status |
|-----------------|---------------|
| Specific API call description + what was returned | ROOT: "Basic completion" → `[✓\|reported]` |
| Vague "yes I've used the API" | ROOT: "Authentication" + "Basic completion" → `[~\|reported]` |
| Model choice + rationale | ROOT: "Model selection (which model for which use case)" → `[✓\|reported]` |
| Token/cost specifics (numbers, limits) | ROOT: "Understanding tokens, context windows, and costs" → `[✓\|reported]` |
| System prompt with specific behavior described | A: "System prompts" → `[✓\|reported]` |
| Tool definition or tool_use block described | B: "Defining tools" + "Parsing tool_use" → `[~\|reported]` |
| Full agentic loop described | B: "Agentic loops" → `[✓\|reported]` |
| Prompt caching or batch API described | C: respective node → `[✓\|reported]` |
| Safety/refusal handling described | C: "Safety and content policy" → `[✓\|reported]` |

---

## Unlock thresholds

- Branch A unlocks when ROOT ≥ 2 `[✓]`
- Branch B unlocks when Branch A ≥ 3 `[✓]`
- Branch C unlocks when Branch B ≥ 3 `[✓]`

Both `[✓]` and `[~]` count toward unlock thresholds.

---

## Tier definitions

| Tier | Criterion |
|------|-----------|
| Explorer | ROOT incomplete — hasn't made a direct API call or is just getting started |
| Builder | Has core patterns working: completions, system prompts, multi-turn, streaming |
| Practitioner | Implements tool use end-to-end; agentic loops working; handles errors robustly |
| Expert | Production-deployed: prompt caching, batch processing, eval pipeline, safety handling |

---

## Tree render template

```
API fundamentals
    [?] Authentication and API key management
    [?] Making a basic completion request
    [?] Model selection (which model for which use case)
    [?] Understanding tokens, context windows, and costs

Core API patterns   [if locked: "(unlock: complete 2 API fundamentals)"]
    [?] System prompts and their effect on behavior
    [?] Multi-turn conversations (message history management)
    [?] Streaming responses
    [?] Stop sequences and max tokens
    [?] Handling API errors and rate limits

Tool use   [if locked: "(unlock: complete 3 Core API patterns)"]
    [?] Defining tools (name, description, input schema)
    [?] Parsing tool_use blocks from responses
    [?] Executing tools and returning tool_result blocks
    [?] Agentic loops (repeated tool use until task completion)
    [?] Parallel tool use

Production patterns   [if locked: "(unlock: complete 3 Tool Use skills)"]
    [?] Prompt caching (cost reduction)
    [?] Batching requests for throughput
    [?] Evaluating outputs programmatically
    [?] Safety and content policy in production
```

Replace every `[?]` with: `[✓]`, `[~]`, `[ ]`, `[★]`, or `[·]`.
If a branch is fully locked (`[·]`), collapse it to just the branch header line.

---

## Saved tree file template

When writing to `~/.claude/ramp/graphs/anthropic-api.md`, use this format:

```markdown
---
version: 3
topic: anthropic-api
user: [git config user.name or "unknown"]
email: [git config user.email or "unknown"]
updated: [today's date YYYY-MM-DD]
level: [Explorer / Builder / Practitioner / Expert]
xp: [CURRENT_XP]
---

# Anthropic API Knowledge Graph

*[✓] Demonstrated · [~] Self-reported · [ ] Not yet · [★] Mastery target · [·] Locked*

## [ROOT] API fundamentals
- [STATUS|TYPE] Authentication and API key management
- [STATUS|TYPE] Making a basic completion request
- [STATUS|TYPE] Model selection (which model for which use case)
- [STATUS|TYPE] Understanding tokens, context windows, and costs

## [A] Core API patterns
- [STATUS|TYPE] System prompts and their effect on behavior
- [STATUS|TYPE] Multi-turn conversations (message history management)
- [STATUS|TYPE] Streaming responses
- [STATUS|TYPE] Stop sequences and max tokens
- [STATUS|TYPE] Handling API errors and rate limits

## [B] Tool use
- [STATUS|TYPE] Defining tools (name, description, input schema)
- [STATUS|TYPE] Parsing tool_use blocks from responses
- [STATUS|TYPE] Executing tools and returning tool_result blocks
- [STATUS|TYPE] Agentic loops (repeated tool use until task completion)
- [STATUS|TYPE] Parallel tool use

## [C] Production patterns
- [STATUS|TYPE] Prompt caching (cost reduction)
- [STATUS|TYPE] Batching requests for throughput
- [STATUS|TYPE] Evaluating outputs programmatically
- [STATUS|TYPE] Safety and content policy in production

## Frontier
- [frontier node name] — [criterion one-liner]

## Notes
<!-- Add personal notes here -->
```

**Demonstration evidence trail:** For `[✓]` nodes only, append `— [repo-name], [YYYY-MM-DD]: [brief note] | next: [YYYY-MM-DD] [L1]`.
Spaced repetition levels: L1=1d, L2=3d, L3=7d, L4=21d, L5=60d, L6=permanent.
