# code-agent-aids template

This repository hosts a Cookiecutter + Cruft template for agent-aided coding workspaces.

- Template sources live in the `{{ cookiecutter.project_slug }}` directory.
- Generation hooks are under `hooks/`.
- Defaults and prompts are defined in `cookiecutter.json`.

## Usage

```bash
uv tool install cookiecutter
uv tool install cruft
uvx cruft create https://github.com/karthikr-tw/code-agent-aids
```

See `{{ cookiecutter.project_slug }}/README.md` inside the generated project for the full developer documentation.
