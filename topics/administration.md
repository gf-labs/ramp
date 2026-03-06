---
topic: administration
version: 1
source_url: https://code.claude.com/docs/en/setup
description: Claude Code administration — org setup, authentication, security, data policies, monitoring, costs, analytics, and plugin marketplace management.
---

# Administration Knowledge Tree Schema

This file defines the curriculum for the `administration` topic. Covers the Administration docs section: setup, authentication, security, server-managed-settings, data-usage, zero-data-retention, monitoring-usage, costs, analytics, plugin-marketplaces.

---

## Node definitions

13 nodes across 3 branches.

### [ROOT] Setup and authentication (4 nodes, always unlocked)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|-----------|
| Organization setup and provisioning | Has set up Claude Code for a team or org; knows the provisioning flow (workspace creation, member invitation, license assignment) | Historical / Qualitative | None | https://code.claude.com/docs/en/setup |
| Authentication methods | Can describe the supported auth methods (API key, SSO/SAML, OAuth); knows when each is appropriate and how to configure them | Qualitative | None | https://code.claude.com/docs/en/authentication |
| Security configuration | Has reviewed or configured security settings: IP allowlisting, session timeouts, audit log retention; can describe the security model | Qualitative | None | https://code.claude.com/docs/en/security |
| Plugin marketplace administration | Has managed plugins at the org level: approved/blocked plugins, set org-wide defaults, or published to an internal marketplace | Historical / Qualitative | None | https://code.claude.com/docs/en/plugin-marketplaces |

### [A] Data and compliance (4 nodes, unlocks when ROOT ≥ 1 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|-----------|
| Data usage and privacy policies | Can explain what data Claude Code sends to Anthropic (prompts, tool outputs, session metadata); knows what is and isn't retained; can brief a security team on the data flow | Qualitative | None | https://code.claude.com/docs/en/data-usage |
| Zero data retention (ZDR) configuration | Knows what ZDR mode does (prompts/responses not retained for training or review); has configured it or can explain the setup steps and eligibility requirements | Qualitative | None | https://code.claude.com/docs/en/zero-data-retention |
| Server-managed settings and policy enforcement | Has configured or observed server-managed settings: settings that administrators push down and users cannot override; knows how to structure a policy file | Qualitative | None | https://code.claude.com/docs/en/server-managed-settings |
| Audit logging and security monitoring | Has accessed or configured audit logs for Claude Code activity; knows what events are logged (tool calls, model invocations, session starts) and how to export them | Historical / Qualitative | None | https://code.claude.com/docs/en/security |

### [B] Cost and usage management (5 nodes, unlocks when Branch A ≥ 2 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url |
|------|-------------------|------|-------------------|-----------|
| Usage monitoring (per user, per team) | Has accessed the usage dashboard; can read token consumption by user or team; knows how to set up alerts for threshold breaches | Historical / Qualitative | None | https://code.claude.com/docs/en/monitoring-usage |
| Cost management and budgeting | Has set or reviewed a budget for Claude Code usage; knows the cost model (per-token pricing by model); can project costs for a team | Qualitative | None | https://code.claude.com/docs/en/costs |
| Token and session limits | Has configured or can describe `maxTokens`, session token budgets, or per-user limits; knows how hitting a limit affects Claude's behavior | Qualitative | `maxTokens` in settings → `[~\|artifact]` | https://code.claude.com/docs/en/costs |
| Analytics and reporting | Has used the analytics dashboard or API to generate a usage report; knows which metrics are available (sessions, tokens, tools used, models) | Historical / Qualitative | None | https://code.claude.com/docs/en/analytics |
| Chargeback and cost allocation | Has set up or can describe cost allocation by team, project, or cost center using tags or org structure; knows how to export cost data | Qualitative | None | https://code.claude.com/docs/en/costs |

---

## Detection signals

| Collected evidence | Node → status |
|--------------------|---------------|
| `maxTokens` in settings | B: "Token and session limits" → `[~\|artifact]` |

*Note: Most administration nodes require organizational context and cannot be auto-detected from local filesystem signals. Gap questions are the primary assessment path for this topic.*

---

## Gap questions

| Branch | Gap | Ask this |
|--------|-----|----------|
| [ROOT] | No setup evidence | "Have you set up Claude Code for a team or org? Walk me through the provisioning steps you went through — workspace, licenses, members." |
| [ROOT] | No auth evidence | "What authentication method does your org use for Claude Code — API key, SSO/SAML, or OAuth? How is it configured?" |
| [ROOT] | No security evidence | "What security controls have you configured or reviewed for Claude Code? IP allowlisting, session timeouts, audit logs?" |
| [A] | No data usage evidence | "What data does Claude Code send to Anthropic during a session? Walk me through the data flow as if briefing a security team." |
| [A] | No ZDR evidence | "Has your org enabled zero data retention? What does it prevent Anthropic from doing with your data and what are the eligibility requirements?" |
| [A] | No server-managed evidence | "Have you used server-managed settings to push Claude Code configuration to users? What did you enforce and why?" |
| [B] | No usage monitoring evidence | "Have you looked at usage data for your team — who's using Claude Code, how much, which models? How did you access that?" |
| [B] | No cost evidence | "How do you track and control Claude Code costs for your org? Token limits, budgets, per-user caps?" |
| [B] | No analytics evidence | "Have you pulled analytics data from Claude Code — sessions, tokens, model distribution? What did you do with it?" |

### Qualitative rubric

- **`[✓]` Demonstrated**: Contains a specific config detail, dashboard name, policy decision, or outcome from actual administrative work.
- **`[~]` Self-reported**: Knows the area exists but no hands-on specifics.
- **`[ ]` Not yet**: No admin responsibility or exposure.

### Answer → node mapping

| Answer contains | Node → status |
|-----------------|---------------|
| Specific provisioning steps (workspace, license, member invite) | ROOT: "Organization setup and provisioning" → `[✓\|reported]` |
| Specific auth method (SSO, SAML, OAuth) with config details | ROOT: "Authentication methods" → `[✓\|reported]` |
| Specific security control (IP allowlist, timeout, audit log) | ROOT: "Security configuration" → `[✓\|reported]` |
| Description of data retention model with specifics | A: "Data usage and privacy policies" → `[✓\|reported]` |
| ZDR eligibility or config details | A: "Zero data retention" → `[✓\|reported]` |
| Server-managed policy config details | A: "Server-managed settings" → `[✓\|reported]` |
| Dashboard usage or API export description | B: "Usage monitoring" → `[✓\|reported]` or "Analytics and reporting" → `[✓\|reported]` |
| Token limit or budget configuration detail | B: "Cost management" → `[✓\|reported]` or "Token and session limits" → `[✓\|reported]` |
| Cost allocation or chargeback setup | B: "Chargeback and cost allocation" → `[✓\|reported]` |

---

## Unlock thresholds

- Branch A unlocks when ROOT ≥ 1 `[✓]`
- Branch B unlocks when Branch A ≥ 2 `[✓]`

Both `[✓]` and `[~]` count toward unlock thresholds.

---

## Tier definitions

| Tier | Criterion |
|------|-----------|
| Explorer | No hands-on admin experience; theory only |
| Builder | Has done basic setup and auth; data policies understood |
| Practitioner | Running monitoring and cost management; security configured |
| Expert | Full org deployment with compliance controls, analytics, and chargeback |

---

## Tree render template

```
[ROOT] Setup and Authentication
    [?] Organization setup and provisioning
    [?] Authentication methods
    [?] Security configuration
    [?] Plugin marketplace administration

[A] Data and Compliance   [if locked: "(unlock: complete 1 Setup & Authentication skill)"]
    [?] Data usage and privacy policies
    [?] Zero data retention (ZDR) configuration
    [?] Server-managed settings and policy enforcement
    [?] Audit logging and security monitoring

[B] Cost and Usage Management   [if locked: "(unlock: complete 2 Data & Compliance skills)"]
    [?] Usage monitoring (per user, per team)
    [?] Cost management and budgeting
    [?] Token and session limits
    [?] Analytics and reporting
    [?] Chargeback and cost allocation
```

---

## Saved tree file template

```markdown
---
version: 3
topic: administration
user: [git config user.name or "unknown"]
email: [git config user.email or "unknown"]
updated: [today's date YYYY-MM-DD]
level: [Explorer / Builder / Practitioner / Expert]
xp: [CURRENT_XP]
---

# Administration Knowledge Tree

*[✓] Demonstrated · [~] Self-reported · [ ] Not yet · [★] Mastery target · [·] Locked*

## [ROOT] Setup and Authentication
- [STATUS|TYPE] Organization setup and provisioning
- [STATUS|TYPE] Authentication methods
- [STATUS|TYPE] Security configuration
- [STATUS|TYPE] Plugin marketplace administration

## [A] Data and Compliance
- [STATUS|TYPE] Data usage and privacy policies
- [STATUS|TYPE] Zero data retention (ZDR) configuration
- [STATUS|TYPE] Server-managed settings and policy enforcement
- [STATUS|TYPE] Audit logging and security monitoring

## [B] Cost and Usage Management
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
