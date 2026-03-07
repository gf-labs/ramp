---
topic: anthropic-api
version: 1
source_url: https://docs.anthropic.com/en/api/
description: Using the Claude API and Anthropic SDK to build custom applications, pipelines, and agentic systems — from basic completions through production tool-use loops.
---

# Anthropic API Knowledge Tree Schema

This topic covers **building with the Claude API** — making completion requests, handling tool use, managing multi-turn conversations, and deploying production pipelines. A developer who completes this tree can build a reliable Claude-powered application from scratch.

---

## Node definitions

18 nodes across 4 branches.

### [ROOT] API fundamentals (always unlocked — 4 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|----|
| Authentication and API key management | Has made an authenticated API request; stores key via env var (not hardcoded); knows the `ANTHROPIC_API_KEY` convention | Artifact / Exercise | `from anthropic` or `@anthropic-ai` import in repo → `[~\|artifact]` | https://docs.anthropic.com/en/api/getting-started |
| Making a basic completion request | Has called `messages.create()` (or equivalent); received a response; can read the `content[0].text` field | Exercise | repo contains messages.create or similar patterns → `[~\|artifact]` | https://docs.anthropic.com/en/api/messages |
| Model selection (which model for which use case) | Can explain when to use Haiku (fast, cheap, simple tasks) vs. Sonnet (balanced) vs. Opus (complex reasoning); has chosen a model with a reason | Qualitative | model specified in code → `[~\|artifact]` | https://docs.anthropic.com/en/docs/about-claude/models |
| Understanding tokens, context windows, and costs | Knows what tokens are; understands the context window limit for their chosen model; has checked cost estimates for their use case | Qualitative | None (ask via gap question) | https://docs.anthropic.com/en/docs/about-claude/models |

### [A] Core API patterns (unlocks when ROOT ≥ 2 `[✓]` — 5 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|----|
| System prompts and their effect on behavior | Has written a system prompt that meaningfully changes Claude's output format or persona; knows the system prompt is separate from the first user turn | Artifact / Exercise | repo contains system prompt patterns → `[~\|artifact]` | https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts |
| Multi-turn conversations (message history management) | Has built a conversation that sends the full message history on each request; understands why context must be managed manually (API is stateless) | Artifact | repo contains conversation history accumulation patterns → `[~\|artifact]` | https://docs.anthropic.com/en/api/messages |
| Streaming responses | Has received a streaming response; processes events incrementally (text_delta, etc.); knows the tradeoff: streaming = lower latency, higher complexity | Artifact / Exercise | repo contains streaming/stream patterns → `[~\|artifact]` | https://docs.anthropic.com/en/api/messages-stream |
| Stop sequences and max tokens | Has used `stop_sequences` to control where the response ends; has set `max_tokens` explicitly; knows what happens at the limit | Artifact / Qualitative | None | https://docs.anthropic.com/en/api/messages |
| Handling API errors and rate limits | Handles `APIStatusError`, `RateLimitError`, and timeout gracefully; has implemented exponential backoff or retry logic | Artifact | repo contains error handling for API calls → `[~\|artifact]` | https://docs.anthropic.com/en/api/errors |

### [B] Tool use (unlocks when Branch A ≥ 3 `[✓]` — 5 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|----|
| Defining tools (name, description, input schema) | Has defined ≥1 tool with a clear name, a description Claude uses to decide when to call it, and a valid `input_schema` (JSON Schema) | Artifact | repo contains tool definition objects → `[~\|artifact]` | https://docs.anthropic.com/en/docs/build-with-claude/tool-use |
| Parsing tool_use blocks from responses | Correctly identifies `stop_reason: "tool_use"` in the response; extracts `tool_use` content block name and `input` dict | Artifact | None | https://docs.anthropic.com/en/docs/build-with-claude/tool-use |
| Executing tools and returning tool_result blocks | Executes the tool logic and returns a `tool_result` content block with the `tool_use_id` correctly set; conversation continues | Artifact | None | https://docs.anthropic.com/en/docs/build-with-claude/tool-use |
| Agentic loops (repeated tool use until task completion) | Has implemented a loop: send message → check stop_reason → execute tool → append result → send again; loop terminates on `end_turn` | Artifact | repo contains agentic loop patterns → `[~\|artifact]` | https://docs.anthropic.com/en/docs/build-with-claude/tool-use |
| Parallel tool use | Claude returns multiple `tool_use` blocks in one response; all are executed and returned in a single `tool_result` list before continuing | Artifact / Qualitative | None | https://docs.anthropic.com/en/docs/build-with-claude/tool-use |

### [C] Production patterns (unlocks when Branch B ≥ 3 `[✓]` — 4 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|----|
| Prompt caching (cost reduction) | Has enabled prompt caching on a long system prompt or repeated context block; knows `cache_control: {type: "ephemeral"}`; has measured cost reduction | Artifact | repo contains cache_control patterns → `[✓\|artifact]` | https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching |
| Batching requests for throughput | Has used the Batch API for offline/async workloads; knows when batch is better than real-time (latency tolerance vs. cost) | Artifact | repo contains batch API patterns → `[✓\|artifact]` | https://docs.anthropic.com/en/api/creating-message-batches |
| Evaluating outputs programmatically | Has a structured eval: test cases with expected outputs (or criteria), Claude responses, and a scoring function; can iterate on prompts based on scores | Artifact / Exercise | repo contains eval patterns → `[~\|artifact]` | https://docs.anthropic.com/en/docs/build-with-claude/develop-tests |
| Safety and content policy in production | Has reviewed the usage policies; has a plan for handling refusals (catching API errors vs. checking `stop_reason`); understands what Claude won't do by default | Qualitative | None (ask via gap question) | https://docs.anthropic.com/en/docs/about-claude/safety-and-usage-policies |

---

## Detection signals

| Collected evidence | Node → status |
|--------------------|---------------|
| `from anthropic` or `@anthropic-ai/sdk` import in repo | ROOT: "Authentication" + "Basic completion" → `[~\|artifact]` |
| model specified in API calls | ROOT: "Model selection" → `[~\|artifact]` |
| system prompt patterns in code | A: "System prompts" → `[~\|artifact]` |
| message history accumulation patterns | A: "Multi-turn conversations" → `[~\|artifact]` |
| streaming/stream patterns in code | A: "Streaming responses" → `[~\|artifact]` |
| error handling for API calls | A: "Handling errors and rate limits" → `[~\|artifact]` |
| tool definition objects in code | B: "Defining tools" → `[~\|artifact]` |
| agentic loop patterns in code | B: "Agentic loops" → `[~\|artifact]` |
| cache_control patterns in code | C: "Prompt caching" → `[✓\|artifact]` |
| batch API patterns in code | C: "Batching requests" → `[✓\|artifact]` |
| eval/scoring patterns in code | C: "Evaluating outputs" → `[~\|artifact]` |

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
| Model choice + rationale | ROOT: "Model selection" → `[✓\|reported]` |
| Token/cost specifics (numbers, limits) | ROOT: "Tokens and context" → `[✓\|reported]` |
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
[ROOT] API fundamentals
    [?] Authentication and API key management
    [?] Making a basic completion request
    [?] Model selection (which model for which use case)
    [?] Understanding tokens, context windows, and costs

[A] Core API patterns   [if locked: "(unlock: complete 2 API fundamentals)"]
    [?] System prompts and their effect on behavior
    [?] Multi-turn conversations (message history management)
    [?] Streaming responses
    [?] Stop sequences and max tokens
    [?] Handling API errors and rate limits

[B] Tool use   [if locked: "(unlock: complete 3 Core API patterns)"]
    [?] Defining tools (name, description, input schema)
    [?] Parsing tool_use blocks from responses
    [?] Executing tools and returning tool_result blocks
    [?] Agentic loops (repeated tool use until task completion)
    [?] Parallel tool use

[C] Production patterns   [if locked: "(unlock: complete 3 Tool Use skills)"]
    [?] Prompt caching (cost reduction)
    [?] Batching requests for throughput
    [?] Evaluating outputs programmatically
    [?] Safety and content policy in production
```

Replace every `[?]` with: `[✓]`, `[~]`, `[ ]`, `[★]`, or `[·]`.
If a branch is fully locked (`[·]`), collapse it to just the branch header line.

---

## Saved tree file template

When writing to `~/.claude/knowledge-graphs/anthropic-api.md`, use this format:

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

# Anthropic API Knowledge Tree

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
