---
topic: claude-code
version: 2
sources: [getting-started, build, configuration, deployment, administration]
source_url: https://code.claude.com/docs/en/overview
description: Complete Claude Code curriculum — aggregates all sub-topics (getting-started, build, configuration, deployment, administration) into one comprehensive learning path.
---

# Claude Code — Meta Topic

This is the master topic for Claude Code. It sources five focused sub-topic schemas and presents them as a single unified knowledge graph and learning path.

**Sub-topics sourced:**
- `getting-started` — Foundations: what Claude Code is, tool loop, memory, workflows, best practices (12 nodes)
- `build` — Building: agents, skills, plugins, hooks, headless, MCP (32 nodes)
- `configuration` — Configuration: settings, permissions, model config, keybindings (13 nodes)
- `deployment` — Deployment: Bedrock, Vertex, Foundry, network, LLM gateway, devcontainer (11 nodes)
- `administration` — Administration: setup, auth, security, data, costs, analytics (13 nodes)

**Total: 81 nodes across 5 sub-topics.**

When `/ramp:up` loads this topic, it concatenates all five sourced schemas. The engine sees one combined schema document with all node definitions, detection signals, gap questions, and mastery criteria.

---

## Usage

```
/ramp:up                    → claude-code (this meta-topic, full curriculum)
/ramp:up getting-started    → focused on foundations only
/ramp:up build              → focused on agents, skills, hooks, MCP
/ramp:up configuration      → focused on settings and permissions
/ramp:up deployment         → focused on cloud providers and CI/CD
/ramp:up administration     → focused on org management and compliance
```

## Tree file behavior

Running `/ramp:up` (claude-code topic) saves to `~/.claude/knowledge-graphs/claude-code.md` — a comprehensive tree containing all nodes from all sub-topics. Each sub-topic also has its own tree file for focused use.

## Merge priority for composite trees

When loading tree files for a composite session:
1. Load `~/.claude/knowledge-graphs/claude-code.md` as the personal tree
2. Cross-reference nodes against all sourced sub-topic trees for any `[✓]` evidence
3. Merge rules: never downgrade `[✓]`; sub-topic `[✓]` upgrades composite `[~]` for same node

## Saved tree file template

When writing `~/.claude/knowledge-graphs/claude-code.md` from a composite session, use this structure — all nodes from all sub-topics in sequence:

```markdown
---
version: 3
topic: claude-code
user: [git config user.name or "unknown"]
email: [git config user.email or "unknown"]
updated: [today's date YYYY-MM-DD]
level: [Explorer / Builder / Practitioner / Expert]
xp: [CURRENT_XP]
sources: [getting-started, build, configuration, deployment, administration]
---

# Claude Code Knowledge Graph

*[✓] Demonstrated · [~] Self-reported · [ ] Not yet · [★] Mastery target · [·] Locked*

## [Getting Started · ROOT] Core Foundations
- [STATUS|TYPE] What Claude Code does and when to use it
- [STATUS|TYPE] Installation and first run
- [STATUS|TYPE] How Claude Code uses computers (tool loop)
- [STATUS|TYPE] Core feature surface (interactive vs. headless, key tools)
- [STATUS|TYPE] Memory types and scope hierarchy

## [Getting Started · A] Working Effectively
- [STATUS|TYPE] Common workflow patterns
- [STATUS|TYPE] When to interrupt vs. let it run
- [STATUS|TYPE] Reading and verifying Claude's output
- [STATUS|TYPE] Writing effective prompts for code tasks

## [Getting Started · B] Best Practices
- [STATUS|TYPE] CLAUDE.md as living project memory
- [STATUS|TYPE] Iterative refinement and course corrections
- [STATUS|TYPE] Recognizing and avoiding common pitfalls

## [Build · ROOT] Agents and Orchestration
- [STATUS|TYPE] Subagent basics: spawning and tool access
- [STATUS|TYPE] Foreground vs. background subagents
- [STATUS|TYPE] Agent teams: orchestration patterns
- [STATUS|TYPE] Custom subagent definitions (.claude/agents/)
- [STATUS|TYPE] Worktrees for parallel development

## [Build · A] Skills and Plugins
- [STATUS|TYPE] Skills (slash commands): creation and syntax
- [STATUS|TYPE] Skill mechanics: $ARGUMENTS, !bash, @file
- [STATUS|TYPE] Skill and command composition
- [STATUS|TYPE] Output styles: controlling response format
- [STATUS|TYPE] Plugin discovery and installation
- [STATUS|TYPE] Plugin manifest (plugin.json)
- [STATUS|TYPE] context: fork for skill isolation
- [STATUS|TYPE] argument-hint frontmatter for documenting expected arguments
- [STATUS|TYPE] .claude/rules/ with YAML paths: glob patterns for conditional rule loading
- [STATUS|TYPE] Skill command execution contexts (!bash vs Bash tool)

## [Build · B] Hooks System
- [STATUS|TYPE] PreToolUse hooks (validation, blocking)
- [STATUS|TYPE] PostToolUse hooks (linting, reactions)
- [STATUS|TYPE] Stop and Notification hooks (session alerts)
- [STATUS|TYPE] Hook handler scripts (stdin, exit codes, response)
- [STATUS|TYPE] Scoped hooks (in skill or agent frontmatter)
- [STATUS|TYPE] Hooks guide: design patterns and gotchas

## [Build · C] Headless and MCP
- [STATUS|TYPE] Headless mode (-p flag, non-interactive)
- [STATUS|TYPE] Piped input and CI integration
- [STATUS|TYPE] --output-format json and --json-schema for structured headless output
- [STATUS|TYPE] Built-in tool selection for codebase tasks
- [STATUS|TYPE] MCP: configure and use servers
- [STATUS|TYPE] MCP project config (.mcp.json)
- [STATUS|TYPE] Troubleshooting: diagnose and recover

## [Build · D] Skills Distribution and Enterprise
- [STATUS|TYPE] Skills distribution via plugins and managed_settings.json
- [STATUS|TYPE] Skills as custom subagent delegation targets

## [Build · E] Iterative Refinement Workflows
- [STATUS|TYPE] Iterative refinement: sequential subagent pattern for test-driven iteration
- [STATUS|TYPE] Interview pattern: structured questions for ambiguous analysis tasks

## [Configuration · ROOT] Settings Fundamentals
- [STATUS|TYPE] Settings scope hierarchy: global, project, local
- [STATUS|TYPE] Settings file format and key options
- [STATUS|TYPE] Model selection and budget configuration
- [STATUS|TYPE] Server-managed settings (policy enforcement)

## [Configuration · A] Permissions and Security
- [STATUS|TYPE] Permissions: allow/deny rules and glob patterns
- [STATUS|TYPE] Permission precedence and scoping
- [STATUS|TYPE] Sandboxing configuration
- [STATUS|TYPE] Fast mode
- [STATUS|TYPE] Plan mode as default

## [Configuration · B] Interface Customization
- [STATUS|TYPE] Terminal configuration
- [STATUS|TYPE] Status line customization
- [STATUS|TYPE] Keybindings customization
- [STATUS|TYPE] Interactive mode features

## [Deployment · ROOT] Cloud Provider Integration
- [STATUS|TYPE] Third-party integrations overview
- [STATUS|TYPE] Amazon Bedrock setup
- [STATUS|TYPE] Google Vertex AI setup
- [STATUS|TYPE] Microsoft Azure AI Foundry setup

## [Deployment · A] Network and Infrastructure
- [STATUS|TYPE] Network configuration (proxies, certificates)
- [STATUS|TYPE] LLM gateway patterns
- [STATUS|TYPE] Dev container configuration
- [STATUS|TYPE] Authentication for enterprise deployments

## [Deployment · B] Deployment Patterns
- [STATUS|TYPE] Choosing a deployment model
- [STATUS|TYPE] Environment variable management for Claude Code
- [STATUS|TYPE] Headless Claude in CI/CD pipelines

## [Administration · ROOT] Setup and Authentication
- [STATUS|TYPE] Organization setup and provisioning
- [STATUS|TYPE] Authentication methods
- [STATUS|TYPE] Security configuration
- [STATUS|TYPE] Plugin marketplace administration

## [Administration · A] Data and Compliance
- [STATUS|TYPE] Data usage and privacy policies
- [STATUS|TYPE] Zero data retention (ZDR) configuration
- [STATUS|TYPE] Server-managed settings and policy enforcement
- [STATUS|TYPE] Audit logging and security monitoring

## [Administration · B] Cost and Usage Management
- [STATUS|TYPE] Usage monitoring (per user, per team)
- [STATUS|TYPE] Cost management and budgeting
- [STATUS|TYPE] Token and session limits
- [STATUS|TYPE] Analytics and reporting
- [STATUS|TYPE] Chargeback and cost allocation

## Frontier
- [frontier node name] — [criterion one-liner]

## Notes
<!-- Add personal notes here -->
```
