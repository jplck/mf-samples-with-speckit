<!--
Sync Impact Report
Version change: N/A → 1.0.0
Modified principles: Initial issuance (no prior titles)
Added sections: Core Principles, Delivery Constraints, Workflow Expectations, Governance
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md ✅ updated
- .specify/templates/spec-template.md ✅ updated
- .specify/templates/tasks-template.md ✅ updated
Follow-up TODOs: None
-->

# Azure AI Hosted Agents Constitution

## Core Principles

### I. Infrastructure-as-Code Canon
- All Azure assets (AI Project, ACR, storage, monitoring, Bing Custom Search) MUST be provisioned and updated exclusively through the Bicep templates in `infra/` executed by `azd up`/`azd deploy`.
- No manual portal edits are allowed; roll forward by updating Bicep, or roll back via `azd down`.
- Every feature proposal MUST state the exact Bicep modules it touches so reviewers can verify reproducibility.

### II. Containerized Agent Contract
- Each hosted agent lives in `src/agents/<agent-name>/` and requires, at minimum, an `agent.py`, `Dockerfile`, and `requirements.txt` tailored to that agent.
- The only supported build path is `scripts/postdeploy.sh <name>:<path>` invoked by the `build-and-push-container-images` hook in `azure.yaml`; bypassing this script is non-compliant.
- Adding or renaming an agent demands a README update plus a new hook argument so that `*_IMAGE` variables are recorded in the root `.env` file.

### III. Environment-Driven Configuration
- The `.azure/<env>/.env` file copied to repo root is the single source of truth for runtime configuration; code MUST read config via helpers such as `get_env` or `config/settings.py`.
- Secrets or endpoints MUST never be hard-coded in Python or Dockerfiles; they belong in the `.env` emitted by `azd` or in Azure Key Vault references consumed by Bicep.
- Any new setting defaults MUST be explicitly justified in specs, and `deploy_agents.py` MUST fail fast when required keys are missing.

### IV. Automated Agent Provisioning & Tools
- Hosted agents are registered only through `src/deploy_agents.py`, which discovers `*_IMAGE` variables, supplies `AZURE_*` environment values, and wires the Bing Custom Search tool via the project connection.
- Manual creation or edits inside Azure AI Studio are prohibited; changes must be encoded in code or scripts so rerunning `python deploy_agents.py` reproduces the state.
- Tooling additions (e.g., more connections) MUST be defined as code-first inputs passed into the deployment script, keeping parity between local and CI runs.

### V. Spec-First, Story-Complete Delivery
- Every feature flows through Speckit: create a spec (`.specify/templates/spec-template.md`), an implementation plan, and story-scoped tasks before touching code.
- User stories MUST remain independently testable; task files have to show how each story can be demoed on its own (e.g., via `curl` against the orchestrator endpoint).
- Tests, telemetry, and docs are part of the definition of done; skipping them requires an explicit exception recorded under "Complexity Tracking" in the plan template.

## Delivery Constraints

- `scripts/postdeploy.sh` is the canonical orchestrator for container builds, pushes, and agent registration. Any change to build arguments, registry, or env propagation MUST keep the script idempotent and bash-compatible.
- File/variable naming follows the pattern `<AGENT_NAME>_IMAGE=...` where `AGENT_NAME` is uppercase with underscores. Downstream automation relies on this contract and will reject deviations.
- README entries for each agent (order-orchestrator, order, product-search) MUST stay accurate; shipping a new capability without README coverage blocks release.
- Connections (e.g., Bing Custom Search) are managed through Azure AI Project connections referenced by environment variables. Code MUST look up the connection via `client.connections.get(os.environ[...])` rather than storing IDs in code.

## Workflow Expectations

1. Run `specify init .` once per repo clone, then follow `/speckit.spec`, `/speckit.plan`, and `/speckit.tasks` to capture intent, design, and execution.
2. Constitution Check inside the plan must, at minimum, confirm: (a) IaC-only changes, (b) compliance with the containerized agent contract, (c) env variable coverage, (d) deployment automation impact, and (e) independent story slices.
3. Before merging, demonstrate the change by running `azd up` or `azd deploy` plus `python src/deploy_agents.py` (if images already built) and attach the relevant `curl` or workflow traces.
4. Keep docs, infrastructure, and runtime assets in lockstep: a PR that alters agents without updating README, infra, or scripts is non-compliant.

## Governance

- This constitution supersedes prior informal practices. Reviewers MUST block changes that violate any principle unless an approved exception is documented in the plan's Complexity Tracking table.
- Amendments require: (1) an ADR or plan section describing the need, (2) updates to this file plus any affected templates, and (3) evidence that `azd` automation stays reproducible.
- Versioning follows SemVer: MAJOR for principle removals/overhauls, MINOR for new sections or materially stronger requirements, PATCH for clarifications. Each amendment updates `LAST_AMENDED_DATE`.
- Compliance reviews occur during every PR: reviewers verify README alignment, IaC-only resource management, and that Speckit artifacts reference this constitution's gates.

**Version**: 1.0.0 | **Ratified**: 2025-11-28 | **Last Amended**: 2025-11-28
