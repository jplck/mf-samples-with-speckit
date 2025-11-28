# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.10+ (agents + deployment tooling)  
**Primary Dependencies**: agentframework, LangGraph, azure-ai-projects, azure-identity, Bing Custom Search tooling  
**Storage**: Azure resources only (no local DB); declare additional stores explicitly  
**Testing**: pytest + curl-style workflow verification (document commands)  
**Target Platform**: Azure AI Hosted Agents (Linux containers)
**Project Type**: Multi-agent service (`src/agents/<name>/`)  
**Performance Goals**: Low-latency orchestration suitable for chat-style requests (state any stricter targets)  
**Constraints**: Must run under `azd up/deploy`, container CPU<=1, RAM<=2Gi unless justified  
**Scale/Scope**: Define number of agents/components touched + user load expectations

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

1. **IaC Only** – Describe the exact Bicep modules impacted; manual portal edits are forbidden.
2. **Container Contract** – List every agent path touched and confirm each has `agent.py`, `Dockerfile`, `requirements.txt`, and a README update plan.
3. **Env Coverage** – Enumerate required environment variables (new or existing) and how `.env`/`settings.py` will validate them.
4. **Automation Impact** – Explain changes to `scripts/postdeploy.sh`, `deploy_agents.py`, or `azure.yaml` hooks and how idempotency is preserved.
5. **Story Independence** – Show how each user story remains independently deployable/testable (include curl or workflow verification notes).

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan output)
├── research.md          # Phase 0 (/speckit.plan output)
├── data-model.md        # Phase 1 (/speckit.plan output)
├── quickstart.md        # Phase 1 (/speckit.plan output)
├── contracts/           # Interfaces, prompts, workflows
└── tasks.md             # Phase 2 (/speckit.tasks output)
```

### Source Code (repository root)

```text
infra/                   # Bicep modules invoked by azd
scripts/
  postdeploy.sh          # Build + push + agent registration orchestrator
src/
  deploy_agents.py       # Discovers *_IMAGE vars, wires Bing search
  agents/
    order/
    order-orchestrator/
    product-search/
  config/settings.py
  workflows/
tests/ (add per feature when needed)
README.md                # Must describe any new agent or workflow
```

**Structure Decision**: Reference the exact folders/files touched (e.g., `src/agents/order`, `infra/core/ai`). Add new directories to this tree when planning.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
