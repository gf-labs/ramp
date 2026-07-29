# Claude Code Docs Map

Generated: 2026-03-05 · Last verified against schemas: 2026-06-26 | Source: https://code.claude.com/docs/en/

This file maps documentation pages to their topic schema and the nodes they inform — the
Claude Code docs below, plus standalone topics like `git` (Pro Git book) that carry their own
source base. Purpose: human-readable reference now; machine-parseable foundation for a future
`/ramp:sync` command.

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
| https://docs.anthropic.com/en/docs/claude-code/plugins | Skills distribution via plugins and managed_settings.json |
| https://code.claude.com/docs/en/discover-plugins | Plugin discovery and installation |
| https://code.claude.com/docs/en/skills | Skills (slash commands): creation and syntax; Skill mechanics: $ARGUMENTS, !bash, @file; Skill and command composition; argument-hint frontmatter for documenting expected arguments |
| https://docs.anthropic.com/en/docs/claude-code/skills | context: fork for skill isolation |
| https://docs.anthropic.com/en/docs/claude-code/memory | .claude/rules/ with YAML paths: glob patterns for conditional rule loading |
| https://code.claude.com/docs/en/output-styles | Output styles: controlling response format |
| https://code.claude.com/docs/en/hooks-guide | Hooks guide: design patterns and gotchas; Scoped hooks (in skill or agent frontmatter) |
| https://code.claude.com/docs/en/hooks | PreToolUse hooks (validation, blocking); PostToolUse hooks (linting, reactions); Stop and Notification hooks (session alerts); Hook handler scripts (stdin, exit codes, response) |
| https://code.claude.com/docs/en/headless | Headless mode (-p flag, non-interactive); Piped input and CI integration; --output-format json and --json-schema for structured headless output |
| https://docs.anthropic.com/en/docs/claude-code/built-in-tools | Built-in tool selection for codebase tasks |
| https://code.claude.com/docs/en/mcp | MCP: configure and use servers; MCP project config (.mcp.json) |
| https://code.claude.com/docs/en/troubleshooting | Troubleshooting: diagnose and recover |
| https://docs.anthropic.com/en/docs/claude-code/sub-agents | Skills as custom subagent delegation targets; Iterative refinement: sequential subagent pattern for test-driven iteration |
| https://docs.anthropic.com/en/docs/build-with-claude/agents | Interview pattern: structured questions for ambiguous analysis tasks |
| *(empirically verified — no canonical doc page)* | Skill command execution contexts (!bash vs Bash tool) |

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
| [`design-notes.md`](design-notes.md) | Repo doc — architecture rationale (kernel, evidence model, schema-declared probes); no external source |

---

## Git (`topics/git.md`) — Pro Git book

Standalone topic (not part of the `claude-code` composite). Source base: https://git-scm.com/book/en/v2 · 27 nodes across 6 branches · id-native with schema-declared `## Probes`. Full URL→node map so the future freshness job can diff it against live docs.

| URL | Nodes informed |
|-----|---------------|
| https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F | What Git is: snapshots, not diffs; The three states: working tree, index, commit |
| https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository | Repository setup: init and clone |
| https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository | Recording changes: add, commit, status, diff |
| https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History | Viewing history with log |
| https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell | Branches as movable pointers (and HEAD) |
| https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging | Basic branch-and-merge workflow; Fast-forward vs. merge commits; Resolving merge conflicts |
| https://git-scm.com/book/en/v2/Git-Branching-Branch-Management | Branch management and workflows |
| https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes | Remotes: fetch, pull, push |
| https://git-scm.com/book/en/v2/Git-Branching-Remote-Branches | Remote-tracking branches |
| https://git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project | Collaboration: pull requests and shared branches |
| https://git-scm.com/book/en/v2/Git-Branching-Rebasing | Rebase vs. merge for integration |
| https://git-scm.com/book/en/v2/Git-Tools-Reset-Demystified | reset: --soft, --mixed, --hard |
| https://git-scm.com/book/en/v2/Git-Basics-Undoing-Things | revert vs. reset |
| https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History | Interactive rebase: squash, reword, reorder |
| https://git-scm.com/book/en/v2/Git-Internals-Maintenance-and-Data-Recovery | The reflog and recovering lost work |
| https://git-scm.com/book/en/v2/Distributed-Git-Maintaining-a-Project | cherry-pick |
| https://git-scm.com/book/en/v2/Git-Tools-Stashing-and-Cleaning | Stashing work in progress |
| https://git-scm.com/docs/git-worktree | Worktrees for parallel work |
| https://git-scm.com/book/en/v2/Git-Tools-Debugging-with-Git | Bisect to find a regression |
| https://git-scm.com/book/en/v2/Git-Basics-Tagging | Tags and annotated releases |
| https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks | Client-side hooks |
| https://git-scm.com/book/en/v2/Git-Internals-Git-Objects | Git objects: blobs, trees, commits |
| https://git-scm.com/book/en/v2/Git-Internals-Git-References | Refs and HEAD |
| https://git-scm.com/book/en/v2/Git-Internals-Plumbing-and-Porcelain | The commit DAG; plumbing vs. porcelain |

---

## Bash (`topics/bash.md`) — GNU Bash Reference Manual

Standalone topic (not part of the `claude-code` composite). Source base: https://www.gnu.org/software/bash/manual/ · 29 nodes across 6 branches · id-native with schema-declared `## Probes`. Scoped to writing correct, robust scripts (interactive-shell customization, job control, and completion programming are out of scope). Full URL→node map so the future freshness job can diff it against live docs.

| URL | Nodes informed |
|-----|---------------|
| https://www.gnu.org/software/bash/manual/html_node/What-is-Bash_003f.html | What Bash is: shell and scripting language |
| https://www.gnu.org/software/bash/manual/html_node/Shell-Scripts.html | Writing and running a script: shebang, chmod, invocation |
| https://www.gnu.org/software/bash/manual/html_node/Shell-Parameters.html | Variables and assignment |
| https://www.gnu.org/software/bash/manual/html_node/Quoting.html | Quoting: single, double, and why it matters |
| https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html | Exit status and command success; Error handling patterns |
| https://www.gnu.org/software/bash/manual/html_node/Bash-Conditional-Expressions.html | Conditionals: if, test, and [[ ]] |
| https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html | Case statements |
| https://www.gnu.org/software/bash/manual/html_node/Looping-Constructs.html | Loops: for, while, until |
| https://www.gnu.org/software/bash/manual/html_node/Lists.html | Lists and short-circuits: &&, \|\|, ; |
| https://www.gnu.org/software/bash/manual/html_node/Shell-Arithmetic.html | Integer arithmetic: (( )) and $(( )) |
| https://www.gnu.org/software/bash/manual/html_node/Shell-Functions.html | Defining and calling functions; Local variables and scope |
| https://www.gnu.org/software/bash/manual/html_node/Positional-Parameters.html | Positional parameters and "$@" vs "$*" |
| https://www.gnu.org/software/bash/manual/html_node/Special-Parameters.html | Special parameters and function exit status |
| https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html | Reading input with read; Traps and cleanup: trap ... EXIT |
| https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html | Strict mode: set -e, -u, -o pipefail |
| https://www.gnu.org/software/bash/manual/html_node/Word-Splitting.html | Quoting pitfalls and word splitting |
| https://www.shellcheck.net/ | Linting with ShellCheck |
| https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html | Parameter expansion |
| https://www.gnu.org/software/bash/manual/html_node/Command-Substitution.html | Command substitution: $(...) |
| https://www.gnu.org/software/bash/manual/html_node/Redirections.html | Redirection: stdout, stderr, and /dev/null; Here-documents and here-strings |
| https://www.gnu.org/software/bash/manual/html_node/Pipelines.html | Pipes and pipelines |
| https://www.gnu.org/software/bash/manual/html_node/Arrays.html | Arrays: indexed and associative |
| https://www.gnu.org/software/bash/manual/html_node/Filename-Expansion.html | Globbing and brace expansion |
| https://www.gnu.org/software/bash/manual/html_node/Process-Substitution.html | Process substitution: <(...) |
| https://www.gnu.org/software/bash/manual/html_node/Shell-Expansions.html | Expansion order and the expansion pipeline |

---

## Python (`topics/python.md`) — official Python Tutorial and Language Reference

Standalone topic (not part of the `claude-code` composite). Source base: https://docs.python.org/3/tutorial/ · 31 nodes across 6 branches · id-native with schema-declared `## Probes`. Scoped to core-language fluency (async/concurrency, descriptors/metaclasses, stdlib-module fluency, typing beyond annotations, and packaging are out of scope). Full URL→node map so the future freshness job can diff it against live docs.

| URL | Nodes informed |
|-----|---------------|
| https://docs.python.org/3/reference/datamodel.html#objects-values-and-types | Objects, types, and names as bindings |
| https://docs.python.org/3/library/copy.html | Mutability and copying |
| https://docs.python.org/3/tutorial/introduction.html#numbers | Numbers and arithmetic |
| https://docs.python.org/3/tutorial/introduction.html#text | Strings and f-strings |
| https://docs.python.org/3/library/stdtypes.html#truth-value-testing | Truthiness, None, and identity vs. equality |
| https://docs.python.org/3/tutorial/controlflow.html#if-statements | Conditionals and guard clauses |
| https://docs.python.org/3/tutorial/controlflow.html#for-statements | for loops and the iteration protocol |
| https://docs.python.org/3/tutorial/controlflow.html#else-clauses-on-loops | while, break, continue, and loop else |
| https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions | Comprehensions |
| https://docs.python.org/3/tutorial/controlflow.html#match-statements | Structural pattern matching with match |
| https://docs.python.org/3/tutorial/controlflow.html#defining-functions | Defining functions; functions as objects |
| https://docs.python.org/3/tutorial/controlflow.html#default-argument-values | Parameters and default values |
| https://docs.python.org/3/tutorial/controlflow.html#arbitrary-argument-lists | *args, **kwargs, and unpacking calls |
| https://docs.python.org/3/tutorial/classes.html#python-scopes-and-namespaces | Scopes: LEGB, closures, and nonlocal |
| https://docs.python.org/3/tutorial/controlflow.html#lambda-expressions | lambda and higher-order functions |
| https://docs.python.org/3/tutorial/controlflow.html#documentation-strings | Docstrings and annotations |
| https://docs.python.org/3/tutorial/datastructures.html#more-on-lists | Lists in practice |
| https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences | Tuples and unpacking |
| https://docs.python.org/3/tutorial/datastructures.html#dictionaries | Dictionaries in practice |
| https://docs.python.org/3/tutorial/datastructures.html#sets | Sets and set operations |
| https://docs.python.org/3/tutorial/classes.html#a-first-look-at-classes | Classes, instances, and __init__ |
| https://docs.python.org/3/tutorial/classes.html#method-objects | Methods and properties |
| https://docs.python.org/3/tutorial/classes.html#inheritance | Inheritance and super() |
| https://docs.python.org/3/reference/datamodel.html#special-method-names | Dunder methods and the object protocol |
| https://docs.python.org/3/tutorial/classes.html#iterators | Iterators from the object side |
| https://docs.python.org/3/tutorial/errors.html#handling-exceptions | Handling exceptions |
| https://docs.python.org/3/tutorial/errors.html#raising-exceptions | Raising and designing exceptions |
| https://docs.python.org/3/reference/compound_stmts.html#the-with-statement | Context managers and with |
| https://docs.python.org/3/tutorial/classes.html#generators | Generators and yield |
| https://docs.python.org/3/glossary.html#term-decorator | Decorators |
| https://docs.python.org/3/tutorial/modules.html | Modules, imports, and the __main__ guard |

---

## Existing specialized topics

These topics are independently maintained (not sourced by `claude-code` meta-topic):

| Topic file | Source domain | Doc base |
|-----------|--------------|---------|
| `topics/git.md` | Git version control (full URL→node map above) | https://git-scm.com/book/en/v2 |
| `topics/bash.md` | Bash scripting (full URL→node map above) | https://www.gnu.org/software/bash/manual/ |
| `topics/python.md` | Python language fundamentals (full URL→node map above) | https://docs.python.org/3/ |
| `topics/best-practices.md` | CLAUDE.md design, config hygiene | https://docs.anthropic.com/en/docs/claude-code/ |
| `topics/mcp-development.md` | Building MCP servers | https://modelcontextprotocol.io/ |
| `topics/anthropic-api.md` | Claude API usage | https://docs.anthropic.com/en/api/ |
| `topics/claude-code-internals.md` | Empirically-verified Claude Code behaviors not in official docs | *(none — verified by experiment)* |

---

## Future: `/ramp:sync` command

A future command will:
1. Fetch each URL above
2. Parse page content (headings, key features, config keys)
3. Diff against current node definitions in the relevant schema
4. Propose additions, removals, or mastery criterion updates
5. Write updated schemas after user approval

Design constraint: the URL → node mapping in this file is the source of truth for which pages inform which nodes. The sync command reads this file first.
