---
name: review-pr
description: Structured review against project instructions
agent: review
model: GPT-5 mini
tools:
  - githubRepo
  - fetch
  - usages
argument-hint: "Provide a branch, PR number, or diff to review."
---

Review the provided branch or diff. Enforce `.github/copilot-instructions.md`, path-scoped instructions, and AGENTS files.

Respond with:
- Summary of the change and instruction files applied.
- Strengths and improvements observed.
- Issues grouped by severity (blocker/major/minor) with actionable remediation steps.
- Test coverage assessment and recommended follow-up checks.
- Open questions or assumptions that need confirmation.
- Optional PR link: ${input:pr_url:https://github.com/...}
- Optional focus area: ${input:focus:security/performance/testing/etc.}
  - Trigger MCP scans when sensitive flows are touched (authentication, payment flows, PII, API keys, secrets, environment variables, etc.).
