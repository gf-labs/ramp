# Claude Code Docs Map

Generated: 2026-03-05 | Source: https://code.claude.com/docs/en/

This file maps every Claude Code documentation page to its topic schema and the nodes it informs.
Purpose: human-readable reference now; machine-parseable foundation for a future `/sup:sync` command.

---

## Getting Started (`topics/getting-started.md`)

| URL | Nodes informed |
|-----|---------------|
| https://code.claude.com/docs/en/overview | What Claude Code does and when to use it |
| https://code.claude.com/docs/en/quickstart | Installation and first run |
| https://code.claude.com/docs/en/how-claude-code-works | How Claude Code uses computers (tool loop); When to interrupt vs. let it run |
| https://code.claude.com/docs/en/features-overview | Core feature surface (interactive vs. headless, key tools) |
| https://code.claude.com/docs/en/memory | Memory types and scope hierarchy; CLAUDE.md as living project memory |
| https://code.claude.com/docs/en/common-workflows | Common workflow patterns |
| https://code.claude.com/docs/en/best-practices | Writing effective prompts for code tasks; Reading and verifying Claude's output; Iterative refinement and course corrections; Recognizing and avoiding common pitfalls |

---

## Build with Claude Code (`topics/build.md`)

| URL | Nodes informed |
|-----|---------------|
| https://code.claude.com/docs/en/sub-agents | Subagent basics: spawning and tool access; Foreground vs. background subagents; Custom subagent definitions (.claude/agents/) |
| https://code.claude.com/docs/en/agent-teams | Agent teams: orchestration patterns; Worktrees for parallel development |
| https://code.claude.com/docs/en/plugins | Plugin manifest (plugin.json) |
| https://code.claude.com/docs/en/discover-plugins | Plugin discovery and installation |
| https://code.claude.com/docs/en/skills | Skills (slash commands): creation and syntax; Skill mechanics: $ARGUMENTS, !bash, @file; Skill and command composition |
| https://code.claude.com/docs/en/output-styles | Output styles: controlling response format |
| https://code.claude.com/docs/en/hooks-guide | Hooks guide: design patterns and gotchas; Scoped hooks (in skill or agent frontmatter) |
| https://code.claude.com/docs/en/hooks | PreToolUse hooks (validation, blocking); PostToolUse hooks (linting, reactions); Stop and Notification hooks (session alerts); Hook handler scripts (stdin, exit codes, response) |
| https://code.claude.com/docs/en/headless | Headless mode (-p flag, non-interactive); Piped input and CI integration |
| https://code.claude.com/docs/en/mcp | MCP: configure and use servers; MCP project config (.mcp.json) |
| https://code.claude.com/docs/en/troubleshooting | Troubleshooting: diagnose and recover |

---

## Configuration (`topics/configuration.md`)

| URL | Nodes informed |
|-----|---------------|
| https://code.claude.com/docs/en/settings | Settings scope hierarchy: global, project, local; Settings file format and key options; Server-managed settings (policy enforcement); Plan mode as default |
| https://code.claude.com/docs/en/permissions | Permissions: allow/deny rules and glob patterns; Permission precedence and scoping |
| https://code.claude.com/docs/en/sandboxing | Sandboxing configuration |
| https://code.claude.com/docs/en/terminal-config | Terminal configuration; Interactive mode features |
| https://code.claude.com/docs/en/model-config | Model selection and budget configuration |
| https://code.claude.com/docs/en/fast-mode | Fast mode |
| https://code.claude.com/docs/en/statusline | Status line customization |
| https://code.claude.com/docs/en/keybindings | Keybindings customization |

---

## Deployment (`topics/deployment.md`)

| URL | Nodes informed |
|-----|---------------|
| https://code.claude.com/docs/en/third-party-integrations | Third-party integrations overview; Choosing a deployment model |
| https://code.claude.com/docs/en/amazon-bedrock | Amazon Bedrock setup; Environment variable management for Claude Code |
| https://code.claude.com/docs/en/google-vertex-ai | Google Vertex AI setup |
| https://code.claude.com/docs/en/microsoft-foundry | Microsoft Azure AI Foundry setup |
| https://code.claude.com/docs/en/network-config | Network configuration (proxies, certificates) |
| https://code.claude.com/docs/en/llm-gateway | LLM gateway patterns |
| https://code.claude.com/docs/en/devcontainer | Dev container configuration |

---

## Administration (`topics/administration.md`)

| URL | Nodes informed |
|-----|---------------|
| https://code.claude.com/docs/en/setup | Organization setup and provisioning |
| https://code.claude.com/docs/en/authentication | Authentication methods; Authentication for enterprise deployments |
| https://code.claude.com/docs/en/security | Security configuration; Audit logging and security monitoring |
| https://code.claude.com/docs/en/server-managed-settings | Server-managed settings and policy enforcement |
| https://code.claude.com/docs/en/data-usage | Data usage and privacy policies |
| https://code.claude.com/docs/en/zero-data-retention | Zero data retention (ZDR) configuration |
| https://code.claude.com/docs/en/monitoring-usage | Usage monitoring (per user, per team) |
| https://code.claude.com/docs/en/costs | Cost management and budgeting; Token and session limits; Chargeback and cost allocation |
| https://code.claude.com/docs/en/analytics | Analytics and reporting |
| https://code.claude.com/docs/en/plugin-marketplaces | Plugin marketplace administration |

---

## Resources (informational — no schema nodes)

| URL | Notes |
|-----|-------|
| https://code.claude.com/docs/en/legal-and-compliance | Legal reference; relevant to administration topic context |

---

## Existing specialized topics

These topics are independently maintained (not sourced by `claude-code` meta-topic):

| Topic file | Source domain | Doc base |
|-----------|--------------|---------|
| `topics/best-practices.md` | CLAUDE.md design, config hygiene | https://docs.anthropic.com/en/docs/claude-code/ |
| `topics/mcp-development.md` | Building MCP servers | https://modelcontextprotocol.io/ |
| `topics/anthropic-api.md` | Claude API usage | https://docs.anthropic.com/en/api/ |

---

## Future: `/sup:sync` command

A future command will:
1. Fetch each URL above
2. Parse page content (headings, key features, config keys)
3. Diff against current node definitions in the relevant schema
4. Propose additions, removals, or mastery criterion updates
5. Write updated schemas after user approval

Design constraint: the URL → node mapping in this file is the source of truth for which pages inform which nodes. The sync command reads this file first.
