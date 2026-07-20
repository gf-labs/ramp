---
topic: deployment
node_count: 11
version: 1
source_url: https://code.claude.com/docs/en/third-party-integrations
description: Deploying Claude Code in enterprise environments — cloud providers (Bedrock, Vertex, Foundry), network configuration, LLM gateways, and dev containers.
goal: ramp them up on deploying Claude Code in the enterprise — routing through cloud providers (Bedrock, Vertex, Azure Foundry), then network config (proxies, gateways, dev containers, auth), and choosing and operating a deployment model in CI/CD
---

# Deployment Knowledge Graph Schema

This file defines the curriculum for the `deployment` topic. Covers the Deployment docs section: third-party-integrations, amazon-bedrock, google-vertex-ai, microsoft-foundry, network-config, llm-gateway, devcontainer.

---

## Node definitions

11 nodes across 3 branches.

### [ROOT] Cloud provider integration (always unlocked — 4 nodes)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|-----------|-----|
| Third-party integrations overview | Can describe why organizations use Claude Code through a cloud provider (data residency, compliance, billing consolidation, enterprise contracts); knows the three supported providers | Qualitative | None | https://code.claude.com/docs/en/third-party-integrations | deployment-third-party-integrations-overview |
| Amazon Bedrock setup | Has configured Claude Code to use AWS Bedrock as the model backend; knows the required env vars (`ANTHROPIC_BEDROCK_BASE_URL`, AWS credentials) and region selection | Artifact / Historical | AWS credentials or Bedrock env vars in environment → `[~\|historical]` | https://code.claude.com/docs/en/amazon-bedrock | deployment-amazon-bedrock-setup |
| Google Vertex AI setup | Has configured Claude Code to use Google Vertex AI; knows the required env vars (`ANTHROPIC_VERTEX_PROJECT_ID`, `CLOUD_ML_REGION`, GCP credentials) | Artifact / Historical | GCP credentials or Vertex env vars in environment → `[~\|historical]` | https://code.claude.com/docs/en/google-vertex-ai | deployment-google-vertex-ai-setup |
| Microsoft Azure AI Foundry setup | Has configured Claude Code to use Azure AI Foundry; knows the required env vars and endpoint format | Artifact / Historical | Azure credentials in environment → `[~\|historical]` | https://code.claude.com/docs/en/microsoft-foundry | deployment-microsoft-azure-ai-foundry-setup |

### [A] Network and infrastructure (4 nodes, unlocks when ROOT ≥ 1 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|-----------|-----|
| Network configuration (proxies, certificates) | Has configured Claude Code to work through a corporate proxy or with a custom TLS certificate; knows `HTTPS_PROXY`, `SSL_CERT_FILE`, and other relevant env vars | Historical / Qualitative | Proxy or cert env vars in environment → `[~\|historical]` | https://code.claude.com/docs/en/network-config | deployment-network-configuration-proxies-certificates |
| LLM gateway patterns | Knows what an LLM gateway is (a proxy between Claude Code and the model API for logging, rate limiting, cost control); has configured or observed one; understands `ANTHROPIC_BASE_URL` | Qualitative | `ANTHROPIC_BASE_URL` in environment → `[~\|historical]` | https://code.claude.com/docs/en/llm-gateway | deployment-llm-gateway-patterns |
| Dev container configuration | Has used Claude Code inside a dev container (`devcontainer.json`); knows how to configure the Claude Code extension or CLI in a containerized environment | Artifact / Historical | `devcontainer.json` in repo → `[~\|artifact]` | https://code.claude.com/docs/en/devcontainer | deployment-dev-container-configuration |
| Authentication for enterprise deployments | Can describe the auth flow for each cloud provider (IAM roles, service accounts, managed identity); knows the difference between API key auth and federated identity | Qualitative | None | https://code.claude.com/docs/en/authentication | deployment-authentication-for-enterprise-deployments |

### [B] Deployment patterns (3 nodes, unlocks when Branch A ≥ 2 `[✓]`)

| Node | Mastery criterion | Type | Auto-detect signal | source_url | id |
|------|-------------------|------|-------------------|-----------|-----|
| Choosing a deployment model | Can compare direct Anthropic API vs. Bedrock vs. Vertex vs. gateway for a given org's requirements (data residency, compliance, cost, latency); knows the key tradeoffs | Qualitative | None | https://code.claude.com/docs/en/third-party-integrations | deployment-choosing-a-deployment-model |
| Environment variable management for Claude Code | Has a strategy for managing Claude Code env vars across local dev, CI, and production (dotenv, secret manager, shell profile); knows which vars are required vs. optional | Historical / Qualitative | None | https://code.claude.com/docs/en/amazon-bedrock | deployment-environment-variable-management-for-claude-code |
| Headless Claude in CI/CD pipelines | Has integrated `claude -p` or the Claude Code SDK into a CI pipeline; knows how to authenticate non-interactively and handle rate limits | Historical / Exercise | CI workflow with claude command → `[✓\|artifact]` | https://code.claude.com/docs/en/headless | deployment-headless-claude-in-ci-cd-pipelines |

---

## Probes

| name | primitive | args |
|------|-----------|------|

*(none — deployment's detection signals are environment-variable based; the vocabulary has no `env-exists`/`env-value` primitive yet, so this schema declares no probes in this slice.)*

---

## Detection signals

| Collected evidence | Node → status |
|--------------------|---------------|
| AWS credentials or `ANTHROPIC_BEDROCK_BASE_URL` in environment | ROOT: "Amazon Bedrock setup" → `[~\|historical]` |
| GCP credentials or `ANTHROPIC_VERTEX_PROJECT_ID` in environment | ROOT: "Google Vertex AI setup" → `[~\|historical]` |
| Azure credentials in environment | ROOT: "Microsoft Azure AI Foundry setup" → `[~\|historical]` |
| `HTTPS_PROXY` or `SSL_CERT_FILE` in environment | A: "Network configuration" → `[~\|historical]` |
| `ANTHROPIC_BASE_URL` pointing to non-Anthropic host | A: "LLM gateway patterns" → `[~\|historical]` |
| `devcontainer.json` in repo | A: "Dev container configuration" → `[~\|artifact]` |
| CI workflow file with `claude` command | B: "Headless Claude in CI/CD pipelines" → `[✓\|artifact]` |

---

## Gap questions

| Branch | Gap | Ask this |
|--------|-----|----------|
| [ROOT] | No cloud provider evidence | "Does your org route Claude Code through a cloud provider like Bedrock or Vertex? If so, which one, and why did the org choose that path?" |
| [ROOT] | Bedrock setup | "Have you pointed Claude Code at AWS Bedrock as the model backend? Which env vars and region did you set?" |
| [ROOT] | Vertex setup | "Have you run Claude Code through Google Vertex AI? What project and region env vars did that require?" |
| [ROOT] | Azure Foundry setup | "Have you configured Claude Code against Azure AI Foundry? What endpoint and env vars did it need?" |
| [A] | No network config evidence | "Have you had to configure a proxy or custom certificate to get Claude Code working in a corporate network? Walk me through what you changed." |
| [A] | No gateway evidence | "Is there an LLM gateway between your Claude Code and Anthropic's API? What does it do and how did you configure `ANTHROPIC_BASE_URL`?" |
| [A] | No devcontainer evidence | "Have you used Claude Code inside a dev container? What was in the `devcontainer.json` to make it work?" |
| [A] | Enterprise auth | "For an enterprise cloud deployment, how does auth actually work — IAM roles, service accounts, managed identity? How's that different from a plain API key?" |
| [B] | No deployment model evidence | "Walk me through how you'd choose between Anthropic API directly vs. Bedrock vs. Vertex for an enterprise deployment. What are the key decision factors?" |
| [B] | Env var management | "How do you manage Claude Code's env vars across local dev, CI, and prod — dotenv, a secret manager, shell profile? Which vars are required vs. optional?" |
| [B] | Headless in CI | "Have you wired `claude -p` or the SDK into a CI pipeline? How do you authenticate non-interactively and handle rate limits?" |

### Qualitative rubric

- **`[✓]` Demonstrated**: Contains a specific env var name, provider-specific config detail, credential type, or observed behavior from actual deployment work.
- **`[~]` Self-reported**: Knows the feature area but no implementation-level specifics.
- **`[ ]` Not yet**: No exposure or pure theory.

### Answer → node mapping

| Answer contains | Node → status |
|-----------------|---------------|
| Names all three cloud providers with their use cases | ROOT: "Third-party integrations overview" → `[✓\|reported]` |
| Specific Bedrock env var or region config | ROOT: "Amazon Bedrock setup" → `[✓\|reported]` |
| Specific Vertex env var or project/region config | ROOT: "Google Vertex AI setup" → `[✓\|reported]` |
| Specific Azure endpoint or credential config | ROOT: "Microsoft Azure AI Foundry setup" → `[✓\|reported]` |
| Proxy env var or cert file path | A: "Network configuration" → `[✓\|reported]` |
| `ANTHROPIC_BASE_URL` pointing to gateway | A: "LLM gateway patterns" → `[✓\|reported]` |
| devcontainer.json config detail | A: "Dev container configuration" → `[✓\|reported]` |
| Describes provider auth flow (IAM role / service account / managed identity) vs. API-key auth | A: "Authentication for enterprise deployments" → `[✓\|reported]` |
| Comparison of providers with specific tradeoffs | B: "Choosing a deployment model" → `[✓\|reported]` |
| Describes an env-var strategy across dev/CI/prod and which vars are required | B: "Environment variable management for Claude Code" → `[✓\|reported]` |
| CI pipeline with `claude -p` or SDK | B: "Headless Claude in CI/CD pipelines" → `[✓\|reported]` |

---

## Unlock thresholds

- Branch A unlocks when ROOT ≥ 1 `[✓]`
- Branch B unlocks when Branch A ≥ 2 `[✓]`

Both `[✓]` and `[~]` count toward unlock thresholds.

---

## Tier definitions

| Tier | Criterion |
|------|-----------|
| Explorer | ROOT incomplete or theory-only |
| Builder | Has configured at least one provider; network basics understood |
| Practitioner | Running in CI; understands auth patterns across providers |
| Expert | Can design and defend an enterprise deployment architecture |

---

## Tree render template

```
Cloud Provider Integration
    [?] Third-party integrations overview
    [?] Amazon Bedrock setup
    [?] Google Vertex AI setup
    [?] Microsoft Azure AI Foundry setup

Network and Infrastructure   [if locked: "(unlock: complete 1 Cloud Provider skill)"]
    [?] Network configuration (proxies, certificates)
    [?] LLM gateway patterns
    [?] Dev container configuration
    [?] Authentication for enterprise deployments

Deployment Patterns   [if locked: "(unlock: complete 2 Network & Infrastructure skills)"]
    [?] Choosing a deployment model
    [?] Environment variable management for Claude Code
    [?] Headless Claude in CI/CD pipelines
```

---

## Saved tree file template

```markdown
---
version: 3
topic: deployment
user: [git config user.name or "unknown"]
email: [git config user.email or "unknown"]
updated: [today's date YYYY-MM-DD]
level: [Explorer / Builder / Practitioner / Expert]
xp: [CURRENT_XP]
---

# Deployment Knowledge Graph

*[✓] Demonstrated · [~] Self-reported · [ ] Not yet · [★] Mastery target · [·] Locked*

## [ROOT] Cloud Provider Integration
- [STATUS|TYPE] Third-party integrations overview
- [STATUS|TYPE] Amazon Bedrock setup
- [STATUS|TYPE] Google Vertex AI setup
- [STATUS|TYPE] Microsoft Azure AI Foundry setup

## [A] Network and Infrastructure
- [STATUS|TYPE] Network configuration (proxies, certificates)
- [STATUS|TYPE] LLM gateway patterns
- [STATUS|TYPE] Dev container configuration
- [STATUS|TYPE] Authentication for enterprise deployments

## [B] Deployment Patterns
- [STATUS|TYPE] Choosing a deployment model
- [STATUS|TYPE] Environment variable management for Claude Code
- [STATUS|TYPE] Headless Claude in CI/CD pipelines

## Frontier
- [frontier node name] — [criterion one-liner]

## Notes
<!-- Add personal notes here -->
```
