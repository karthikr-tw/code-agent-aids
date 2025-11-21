# Developer Setup & Build

This page describes how to set up a development environment, run tests, and verify agent-driven checks.

Prerequisites
- Python 3.12+ (project `pyproject.toml` requires >=3.12)
- A virtual environment (recommended)
- `uv` helper available in your environment if you use the project's run helper

Create and activate a venv (macOS / zsh):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r <(poetry export -f requirements.txt --dev --without-hashes) || pip install -r requirements.txt
```

(If you use `poetry` or another environment manager, follow your normal workflow.)

Install dependencies via `pyproject.toml` (if using pip-tools or poetry):

```bash
pip install -r requirements.txt  # if you generated one from pyproject.toml
pip install -e .
```

Running tests
- The repository contains doc structural tests under `tests/test_docs_structural.py` which validate prompt and agent frontmatter and optional forbidden-token checks.

Run the full test suite:

```bash
uv run pytest -q
```

Run a single test:

```bash
uv run pytest tests/test_docs_structural.py::test_prompts_have_frontmatter -q
```

Notes
- `uv` may be a wrapper in this workspace used by CI. If `uv` is not present, run `pytest -q` directly inside the activated venv.
- If a forbidden token check is desired, create `tests/forbidden_tokens.txt` with one token per line; the structural test will pick it up automatically.
