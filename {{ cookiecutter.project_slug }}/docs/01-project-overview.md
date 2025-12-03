# Project Overview

This repository provides a set of agent-focused documentation and instruction files used to run Copilot-style agents and enforce repository policies for automated code assistance and documentation generation.

Purpose
- Capture repository-wide policies for agent behavior, code changes, and documentation.
- Provide a structured place for per-path instructions and agent definitions.
- Offer reusable prompt templates for common agent workflows.

What's in this repo (relevant files)
- `.github/copilot-instructions.md` — Global rules and agent mode expectations.
- `.github/instructions/*.instructions.md` — Path-scoped instructions that extend or override global rules.
- `.github/agents/*.agent.md` — Agent definitions (planner, implement, review, tests, docs, requirement-parser, etc.).
- `.github/prompts/*.prompt.md` — Reusable prompts for standard workflows (plan, implement, review, write-tests).
- `COPILOT_REQUIREMENTS.md` — (Optional) Freeform requirements file used by the `requirement-parser` agent.
- `mcp/analysis.json` and `mcp/` tooling — Manifest for MCP servers that provide helper analyses.

Design principles
- Keep agent instructions conservative and scoped.
- Never allow automated agents to change production application code without explicit human review and cross-agent handoffs.
- Prefer small, verifiable edits over big refactors.
- Make generated sections auditable (use BEGIN/END markers and REVIEW NEEDED tags where ambiguous).

Intended audience
- Developers who will implement features and tests.
- Repository maintainers who define agent behaviour and policies.
- Copilot/agent operators integrating agent automation with CI.
