---
topic: getting-started
version: 1
source_url: https://code.claude.com/docs/en/overview
description: Claude Code fundamentals — what it is, how it works, core workflows, memory system, and best practices for effective use.
---

# Getting Started Knowledge Tree Schema

This file defines the curriculum for the `getting-started` topic. Covers the foundational Claude Code docs: overview, quickstart, how it works, features, memory, common workflows, and best practices.

---

## Node definitions

12 nodes across 3 branches.

### [ROOT] Core foundations (always unlocked — 5 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|-----------|
| What Claude Code does and when to use it | Can articulate what Claude Code is (an agentic CLI, not a chat UI), the tool loop model, and at least two scenarios where it's the right tool vs. the wrong one | Qualitative | None | https://code.claude.com/docs/en/overview |
| Installation and first run | Has installed Claude Code, run `claude` at least once, and knows the difference between interactive and headless invocation | Historical / Exercise | git history or sessions exist → `[~\|historical]` | https://code.claude.com/docs/en/quickstart |
| How Claude Code uses computers (tool loop) | Can explain the tool loop: Claude proposes tool calls → user approves → output fed back → Claude continues; knows which tools exist (Bash, Read, Write, Edit, Glob, Grep, Agent) | Qualitative | None | https://code.claude.com/docs/en/how-claude-code-works |
| Core feature surface (interactive vs. headless, key tools) | Can describe the main capability surface: interactive mode, headless mode, slash commands, MCP servers, hooks, agents; knows where each fits | Qualitative | headless invocations > 0 → `[~\|historical]` | https://code.claude.com/docs/en/features-overview |
| Memory types and scope hierarchy | Can name all four memory types (CLAUDE.md, settings.json, auto-memory, session context) and explain how they differ in persistence and scope | Exercise / Qualitative | CLAUDE.md exists → `[~\|artifact]`; settings.json exists → `[~\|artifact]` | https://code.claude.com/docs/en/memory |

### [A] Working effectively (4 nodes, unlocks when ROOT ≥ 3 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|-----------|
| Common workflow patterns | Has used Claude Code for ≥2 of: code changes, debugging, test writing, commit messages, PR descriptions; can describe what happened | Historical / Exercise | git history exists + sessions > 5 → `[~\|historical]` | https://code.claude.com/docs/en/common-workflows |
| When to interrupt vs. let it run | Has deliberately stopped Claude mid-task (Ctrl+C or Esc) AND deliberately let it run uninterrupted for a multi-step task; can explain the heuristic for choosing | Exercise / Qualitative | sessions > 10 → `[~\|historical]` | https://code.claude.com/docs/en/how-claude-code-works |
| Reading and verifying Claude's output | After a non-trivial change, explicitly reviewed the diff, ran a test or linter, and caught or confirmed Claude's work; can describe what "trust but verify" means operationally | Exercise / Historical | max files in recent commit > 0 → `[~\|historical]` | https://code.claude.com/docs/en/best-practices |
| Writing effective prompts for code tasks | Has crafted a prompt that includes: what to change, why, and a constraint or acceptance criterion; can explain why context-rich prompts outperform vague ones | Qualitative | None | https://code.claude.com/docs/en/best-practices |

### [B] Best practices (3 nodes, unlocks when Branch A ≥ 2 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|-----------|
| CLAUDE.md as living project memory | Has written or meaningfully updated a CLAUDE.md; can describe what belongs there (build commands, conventions, architecture notes) vs. what doesn't | Artifact | CLAUDE.md line count > 20 → `[✓\|artifact]` | https://code.claude.com/docs/en/memory |
| Iterative refinement and course corrections | Has pushed back on a Claude response mid-task, requested a change, and iterated; understands that Claude responds to correction — it's not one-shot | Exercise / Historical | sessions > 5 → `[~\|historical]` | https://code.claude.com/docs/en/best-practices |
| Recognizing and avoiding common pitfalls | Can name at least two failure modes: over-trusting output without review, giving too little context, not using plan mode for risky changes | Qualitative | None | https://code.claude.com/docs/en/best-practices |

---

## Detection signals

| Collected evidence | Node → status |
|--------------------|---------------|
| git history exists OR sessions > 0 | ROOT: "Installation and first run" → `[✓\|historical]` |
| sessions > 5 | A: "Common workflow patterns" → `[~\|historical]` |
| sessions > 10 | A: "When to interrupt vs. let it run" → `[~\|historical]` |
| sessions > 10 | A: "Iterative refinement" → `[~\|historical]` |
| CLAUDE.md line count > 20 | B: "CLAUDE.md as living project memory" → `[✓\|artifact]` |
| headless invocations > 0 | ROOT: "Core feature surface" → `[~\|historical]` |
| max files in recent commit ≥ 3 | A: "Reading and verifying Claude's output" → `[~\|historical]` |

---

## Gap questions

| Branch | Gap | Ask this |
|--------|-----|----------|
| [ROOT] | No tool loop evidence | "Explain the tool loop model in your own words — what happens between when you type a prompt and when Claude writes code?" |
| [ROOT] | No feature surface evidence | "Which Claude Code features have you used beyond basic edits — headless mode, hooks, MCP, agents? Walk me through one." |
| [ROOT] | No memory types evidence | "Name the four ways Claude Code persists information across sessions. What goes in each one?" |
| [A] | No workflow pattern evidence | "Walk me through the last time you used Claude Code for something beyond a simple edit. What did you ask it to do and what happened?" |
| [A] | No interrupt/let-run evidence | "Have you ever stopped Claude mid-task? What triggered it? Have you ever let it run 10+ tool calls uninterrupted?" |
| [A] | No verification evidence | "After Claude makes a non-trivial change, what do you do before accepting it? Be specific — what are you looking for?" |
| [B] | No CLAUDE.md evidence | "What's in your CLAUDE.md right now? Walk me through why each section is there." |
| [B] | No pitfall evidence | "What's the most common mistake developers make when using Claude Code? Name two." |

### Qualitative rubric

- **`[✓]` Demonstrated**: Contains at least one specific, verifiable detail — a concrete scenario, an observed behavior, a tradeoff navigated, or a clear causal explanation of *why* not just *what*.
- **`[~]` Self-reported**: Affirmative but vague. "Yes I've used it" without specifics.
- **`[ ]` Not yet**: Negative, "not sure," or "heard of it but haven't tried."

### Answer → node mapping

| Answer contains | Node → status |
|-----------------|---------------|
| Specific description of tool loop (propose → approve → feedback → continue) | ROOT: "How Claude Code uses computers" → `[✓\|reported]` |
| Vague "yes Claude proposes things and I approve" | ROOT: "How Claude Code uses computers" → `[~\|reported]` |
| Specific use of headless/hooks/agents/MCP | ROOT: "Core feature surface" → `[✓\|reported]` |
| Specific workflow (debugging, PR, multi-file change) with detail | A: "Common workflow patterns" → `[✓\|reported]` |
| Mentions Ctrl+C or deliberate interruption with reason | A: "When to interrupt vs. let it run" → `[✓\|reported]` |
| Mentions reviewing diff or running tests after Claude's changes | A: "Reading and verifying" → `[✓\|reported]` |
| Mentions context-rich prompts or acceptance criteria | A: "Writing effective prompts" → `[✓\|reported]` |
| Describes CLAUDE.md contents specifically | B: "CLAUDE.md as living project memory" → `[✓\|reported]` |
| Names specific pitfalls (over-trust, vague prompts, no plan mode) | B: "Recognizing common pitfalls" → `[✓\|reported]` |

---

## Unlock thresholds

- Branch A unlocks when ROOT ≥ 3 `[✓]`
- Branch B unlocks when Branch A ≥ 2 `[✓]`

Both `[✓]` and `[~]` count toward unlock thresholds.

---

## Tier definitions

| Tier | Criterion |
|------|-----------|
| Explorer | ROOT incomplete |
| Builder | ROOT complete, Branch A in progress |
| Practitioner | Branch A complete, Branch B active |
| Expert | All branches complete |

---

## Tree render template

```
[ROOT] Core Foundations
    [?] What Claude Code does and when to use it
    [?] Installation and first run
    [?] How Claude Code uses computers (tool loop)
    [?] Core feature surface (interactive vs. headless, key tools)
    [?] Memory types and scope hierarchy

[A] Working Effectively   [if locked: "(unlock: complete 3 Core Foundations)"]
    [?] Common workflow patterns
    [?] When to interrupt vs. let it run
    [?] Reading and verifying Claude's output
    [?] Writing effective prompts for code tasks

[B] Best Practices   [if locked: "(unlock: complete 2 Working Effectively skills)"]
    [?] CLAUDE.md as living project memory
    [?] Iterative refinement and course corrections
    [?] Recognizing and avoiding common pitfalls
```

---

## Saved tree file template

```markdown
---
version: 3
topic: getting-started
user: [git config user.name or "unknown"]
email: [git config user.email or "unknown"]
updated: [today's date YYYY-MM-DD]
level: [Explorer / Builder / Practitioner / Expert]
xp: [CURRENT_XP]
---

# Getting Started Knowledge Tree

*[✓] Demonstrated · [~] Self-reported · [ ] Not yet · [★] Mastery target · [·] Locked*

## [ROOT] Core Foundations
- [STATUS|TYPE] What Claude Code does and when to use it
- [STATUS|TYPE] Installation and first run
- [STATUS|TYPE] How Claude Code uses computers (tool loop)
- [STATUS|TYPE] Core feature surface (interactive vs. headless, key tools)
- [STATUS|TYPE] Memory types and scope hierarchy

## [A] Working Effectively
- [STATUS|TYPE] Common workflow patterns
- [STATUS|TYPE] When to interrupt vs. let it run
- [STATUS|TYPE] Reading and verifying Claude's output
- [STATUS|TYPE] Writing effective prompts for code tasks

## [B] Best Practices
- [STATUS|TYPE] CLAUDE.md as living project memory
- [STATUS|TYPE] Iterative refinement and course corrections
- [STATUS|TYPE] Recognizing and avoiding common pitfalls

## Frontier
- [frontier node name] — [criterion one-liner]

## Notes
<!-- Add personal notes here -->
```
