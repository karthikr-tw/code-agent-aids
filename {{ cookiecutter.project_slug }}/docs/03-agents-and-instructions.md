# Agents, Instructions & Prompts

This document explains the purpose and interplay of the major instruction files and agents in this repository.

Key concepts
- Global instructions: `.github/copilot-instructions.md` defines repository-wide policies for Copilot agents.
- Path-scoped instructions: `.github/instructions/*.instructions.md` contain scoped rules that augment or override the global policy for a given path or domain.
- Agents: files under `.github/agents/*.agent.md` describe the role, tool access, handoffs and operational constraints for each agent (planner, implement, review, tests, docs, requirement-parser, etc.).
- Prompts: `.github/prompts/*.prompt.md` are reusable prompt templates for common workflows (plan, implement, refactor, review, tests).

Agent behaviour and handoffs
- Agents have focused roles. For example:
  - `planner` produces ordered, small-step plans.
  - `implement` performs code edits in small, reviewable commits.
  - `review` validates diffs and enforces instruction files.
  - `tests` improves or writes tests only.
  - `docs` writes or updates documentation.
  - `requirement-parser` ingests `COPILOT_REQUIREMENTS.md` and generates or updates instruction layout files (now includes prompts scope).

Handoffs
- Handoffs listed in agent frontmatter represent recommended downstream actions (e.g., planner -> implement). Handoffs should always include a prompt and indicate whether messages are sent automatically.

Prompt lifecycle
- Prompts templates are authored in `.github/prompts/*.prompt.md` and referenced from agent frontmatter or instruction files.
- If a requirement maps to a new reusable workflow, the `requirement-parser` may propose a prompt; implementers should review and accept/modify it prior to automated use.

Auditing & REVIEW markers
- When the `requirement-parser` or other agents encounter ambiguous requirements, they must insert REVIEW NEEDED markers in generated content:

  <!-- REVIEW NEEDED: Documentation requires expert validation [AGENT: requirement-parser] [DATE: YYYY-MM-DD] [reason: ambiguous requirement mapping] -->

- Generated sections should be wrapped where practical:

  ```html
  <!-- BEGIN: requirement-parser generated global instructions -->
  ...
  <!-- END: requirement-parser generated global instructions -->
  ```

Security & safety
- Agents should not store or leak credentials. Any integration with MCP servers must reference credentials via environment variables and never commit secrets to the repo.
- Treat destructive operations as high risk; require explicit human approval in the workflow.
