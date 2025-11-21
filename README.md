# agent-aided-coding-main

Repository for agent-driven coding workflows and instruction files.

Documentation
- `docs/01-project-overview.md` — Project overview and design principles.
- `docs/02-developer-setup.md` — Developer setup and test instructions.
- `docs/03-agents-and-instructions.md` — Agent behaviors, handoffs, and instruction layout.
- `docs/04-prompts-and-templates.md` — Prompt authoring and templates.

Quickstart
1. Create and activate a Python virtualenv.
2. Install dependencies from `pyproject.toml`.
3. Run tests: `uv run pytest -q` (or `pytest -q` in a venv).

Contributing
- Update `.github/instructions/*.instructions.md` for path‑scoped rules.
- Add prompt templates under `.github/prompts/` when creating reusable flows.
- Edit agents under `.github/agents/` only when adding or refining agent responsibilities.
