---
name: write-tests
description: Generate or improve tests for a module
agent: tests
model: GPT-5 mini
tools:
  - githubRepo
  - edit
  - search
argument-hint: "Which module or behaviour needs automated tests?"
---

Generate or refine tests for the given area, keeping them deterministic and aligned with `tests.instructions.md`.

Target module or change: ${input:target}

Include:
- Summary of behaviours under test and relevant instruction files.
- Proposed test cases (success, failure, edge conditions) with rationale.
- Code edits limited to test files/fixtures.
- Commands to run (pytest, coverage) and expected outcomes.
- Optional coverage goal: ${input:coverage:Target % or qualitative goal}
- Optional MCP analysis toggle: ${input:use_mcp:yes/no}
