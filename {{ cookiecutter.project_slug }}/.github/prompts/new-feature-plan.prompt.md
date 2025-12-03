---
name: new-feature-plan
description: Plan a cross-service feature for the platform or application
agent: planner
model: GPT-5 mini
tools:
  - githubRepo
  - search
argument-hint: "What feature or refactor do you need planned?"
---

You are the planning agent. Read relevant code and instructions. Generate a clear, multi-step plan for the requested feature.

Feature to plan: ${input:feature}

Include:
- Context and assumptions (existing behaviour, constraints, instruction files consulted)
- Affected components (backend, API gateway, worker, frontend, infra, tests) and contract touchpoints
- Ordered steps with small, verifiable changes and the tools/commands to run
- Testing strategy (automated + manual) and risks/rollback considerations
- Recommended follow-up prompts or agents for implementation and review
- Optional supplementary context: ${input:context:Link to spec, ticket, or KPI target}

Remember to cite relevant instruction files, `AGENTS.md`, and model guides (e.g. `CLAUDE.md`, `GEMINI.md`). Leverage MCP helpers via `analysis` server for dependency graphs when needed.
---
name: new-feature-plan
description: Plan a cross-service feature for the platform or application
agent: planner
model: GPT-5 mini
tools:
  - githubRepo
  - search
argument-hint: "What feature or refactor do you need planned?"
---

You are the planning agent. Read relevant code and instructions. Generate a clear, multi-step plan for the requested feature.

Feature to plan: ${input:feature}

Include:
- Context and assumptions (existing behaviour, constraints, instruction files consulted)
- Affected components (backend, API gateway, worker, frontend, infra, tests) and contract touchpoints
- Ordered steps with small, verifiable changes and the tools/commands to run
- Testing strategy (automated + manual) and risks/rollback considerations
- Recommended follow-up prompts or agents for implementation and review
- Optional supplementary context: ${input:context:Link to spec, ticket, or KPI target}

Remember to cite relevant instruction files, `AGENTS.md`, and model guides (e.g. `CLAUDE.md`, `GEMINI.md`). Leverage MCP helpers via `analysis` server for dependency graphs when needed.
