---
name: refactor-service
description: Refactor a selected service while respecting path instructions
agent: implement
model: GPT-5 mini
tools:
  - githubRepo
  - edit
argument-hint: "Which service needs refactoring and why?"
---

Refactor the chosen service to improve clarity and maintainability while keeping behavior stable.

Service: ${input:service}

Follow relevant `.instructions.md` rules and nested `AGENTS.md` guidance.

Provide:
- Summary of current issues, invariants to preserve, and risks.
- Step-by-step refactor plan (pure refactors first, behaviour changes last).
- Proposed code edits referencing files/symbols.
- Tests/commands to run (unit, integration, lint) and expected outcomes.
- Notes for reviewers (migration steps, manual QA, follow-up work).
- Optional service path override: ${input:path:Relative path to service or module}
- Flag whether MCP audits should be run: ${input:run_mcp:yes/no}
