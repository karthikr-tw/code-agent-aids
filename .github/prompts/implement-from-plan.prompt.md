---
name: implement-from-plan
description: Implement a previously generated plan
agent: implement
model: GPT-5 mini
tools:
  - githubRepo
  - runCommands
  - edit
argument-hint: "Reference the plan or task you want implemented."
---

Take the plan from prior messages and apply it carefully:
- Restate scope, constraints, and applicable instruction files before editing.
- Make small, incremental edits and keep diffs reviewable.
- Propose terminal commands explicitly, request approval, and report outcomes (tests, linters, builds).
- Update tests, documentation, and shared contracts in lockstep with code changes.
- Summarize remaining risks, follow-up work, and verification steps for reviewers.
- Optional explicit plan reference: ${input:plan_url:Link to plan or ticket}
- If new MCP tooling is required, note the server to attach (e.g. `analysis`, `design-a11y`).
