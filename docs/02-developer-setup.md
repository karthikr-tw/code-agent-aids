# Developer Setup & Build

This page describes how to set up a development environment, run tests, and verify agent-driven checks.

Prerequisites
- Python 3.12+ (the template targets `>=3.12`).
- [uv](https://docs.astral.sh/uv) CLI installed and on your `PATH`.
- Git (needed for Cookiecutter + Cruft links).
- Template helpers installed via uv tools so they stay isolated per user:
	- `uv tool install cookiecutter`
	- `uv tool install cruft`

## Bootstrapping from the template
- Prefer `uvx cruft create https://github.com/karthikr-tw/code-agent-aids` so the generated project carries a `.cruft.json` file pointing back to this template commit.
- Answer the prompts for `project_name`, `project_slug`, `project_description`, and `python_version`—the defaults come from `cookiecutter.json` in this repo and match the current docs.
- Inside the generated repo, run `uvx cruft check` periodically to see if template updates are available, and `uvx cruft update` to merge them (resolve conflicts and run `uv run pytest -q` afterward).
- When running plain Cookiecutter (`uvx cookiecutter https://github.com/karthikr-tw/code-agent-aids`), the `hooks/post_gen_project.py` script automatically writes `.cruft.json` by resolving the template commit with `git ls-remote`. If the hook fails (for example, Git is unavailable or you are fully offline), rerun `uvx cruft link https://github.com/karthikr-tw/code-agent-aids --checkout main` after generation to recreate the config before attempting `uvx cruft check`.
- For a one-off scaffold without upgrade tracking you can delete `.cruft.json`, but future template updates must then be merged manually.

## Working locally with uv
`uv` handles virtualenv creation, dependency installation, and command execution from `pyproject.toml`. Typical flow:

```bash
uv sync                # creates .venv and installs project dependencies
uv run python main.py  # run the sample script or CLI entry point
uv run pytest -q       # execute the structural docs/tests suite
uv run pytest tests/test_docs_structural.py::test_prompts_have_frontmatter -q
```

Running tests
- The repository contains doc structural tests under `tests/test_docs_structural.py` which validate prompt and agent frontmatter and optional forbidden-token checks.
- Use `uv run pytest -q` for the full suite or pass individual node ids (as in the example above) for focused runs.

Notes
- If a forbidden token check is desired, create `tests/forbidden_tokens.txt` with one token per line; the structural test will pick it up automatically.
