# Prompts & Templates

This document describes how prompt templates are structured and how to author new ones.

Prompt file format
- Location: `.github/prompts/*.prompt.md`
- Structure: A YAML frontmatter block followed by instructions.
  - Required frontmatter keys: `name`, `description`, `agent`.
  - Optional keys: `argument-hint`, `model`, `tools`.

Example frontmatter:

```yaml
---
name: implement-from-plan
description: Implement a previously generated plan
agent: implement
model: GPT-5 mini
tools:
  - githubRepo
  - runCommands
argument-hint: "Reference the plan or task you want implemented."
---
```

Authoring rules
- Keep prompts generic and domain-agnostic (no company/product tokens).
- Make prompts idempotent and explicit about the scope they act on (single feature or single file group).
- Prefer prompting for small actions and explicit approvals for commands that modify the repository or run tests.

Referencing prompts
- Link a prompt from an agent file or instruction when the workflow is repetitive (e.g. `new-feature-plan`, `implement-from-plan`, `review-pr`).
- When a new prompt is proposed by the `requirement-parser`, add it to `.github/prompts/` and reference it from the relevant `.instructions.md` or `AGENTS.md`.

Review
- Changes to prompts are code-reviewed like other docs; treat them as sensitive because they define automated behaviours.
