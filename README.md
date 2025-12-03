# {{ cookiecutter.project_name }}

Repository for {{ cookiecutter.project_description }}.

Documentation
- `docs/01-project-overview.md` — Project overview and design principles.
- `docs/02-developer-setup.md` — Developer setup and test instructions.
- `docs/03-agents-and-instructions.md` — Agent behaviors, handoffs, and instruction layout.
- `docs/04-prompts-and-templates.md` — Prompt authoring and templates.

Quickstart (uv-native)
1. Sync dependencies and create `.venv` automatically: `uv sync`.
2. Run the example script: `uv run python main.py`.
3. Execute the doc/tests suite: `uv run pytest -q`.

Template Usage
1. Install the tooling once per machine with uv so it stays versioned: `uv tool install cookiecutter` and `uv tool install cruft` (use `uv tool update <name>` when you need newer releases).
2. Create a new repository directly from this template with Cruft so updates stay linkable:
	- `uvx cruft create gh:karthikr-tw/code-agent-aids`
	- Fill in the prompts for `project_name`, `project_slug`, `project_description`, and `python_version` (matching the defaults in `cookiecutter.json`).
3. Whether you use Cruft or plain Cookiecutter, the post-generation hook seeds a `.cruft.json` file that points back to `gh:karthikr-tw/code-agent-aids` and the commit that was used. If the hook cannot resolve the commit (for example, you are offline), rerun `uvx cruft link gh:karthikr-tw/code-agent-aids --checkout main` inside the generated repo to refresh it.
4. If you only need a one-off scaffold and do not care about ongoing updates, `cookiecutter gh:karthikr-tw/code-agent-aids` works too—just be aware that skipping Cruft means you will need to merge future template changes manually if you ever want them.

Keeping Projects Updated
- Every generated repo contains a `.cruft.json` file (auto-created by `hooks/post_gen_project.py`) that pins the template commit. Run `uvx cruft check` to confirm you are on the latest template revision.
- Pull template changes with `uvx cruft update`; resolve any merge prompts in-place, then rerun the usual test suite (`uv run pytest -q`).
- Commit the resulting changes once tests pass so downstream teammates inherit the refreshed instructions and prompts.

Contributing
- Update `.github/instructions/*.instructions.md` for path‑scoped rules.
- Add prompt templates under `.github/prompts/` when creating reusable flows.
- Edit agents under `.github/agents/` only when adding or refining agent responsibilities.
