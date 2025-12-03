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
	- `uvx cruft create https://github.com/karthikr-tw/code-agent-aids`
	- Fill in the prompts for `project_name`, `project_slug`, `project_description`, and `python_version` (matching the defaults in `cookiecutter.json`).
3. Whether you use Cruft or plain Cookiecutter, the post-generation hook seeds a `.cruft.json` file that points back to `https://github.com/karthikr-tw/code-agent-aids` and the commit that was used. If the hook cannot resolve the commit (for example, you are offline), rerun `uvx cruft link https://github.com/karthikr-tw/code-agent-aids --checkout main` inside the generated repo to refresh it.
4. If you only need a one-off scaffold and do not care about ongoing updates, `uvx cookiecutter https://github.com/karthikr-tw/code-agent-aids` works too—just be aware that skipping Cruft means you will need to merge future template changes manually if you ever want them.

## Adopting this template in an existing repository

Follow the official Cookiecutter + Cruft workflow when you need to retrofit an existing codebase: first import the files yourself (without clobbering custom docs), then let Cruft track future diffs.

### Phase 1 — Render and copy the baseline (automatically)
1. **Run Cookiecutter directly inside your repo with `--skip-if-file-exists` and a replay file.** The [CLI docs](https://cookiecutter.readthedocs.io/en/stable/cli_options.html#cmdoption-cookiecutter-replay-file) show how to pre-answer prompts so you never have to type anything interactively.
	```bash
	uv tool install cookiecutter
	repo_root=$PWD
	repo_parent=$(dirname "$repo_root")
	repo_name=$(basename "$repo_root")
	cat > /tmp/code-agent-replay.json <<EOF
	{
	  "cookiecutter": {
	    "project_name": "$repo_name",
	    "project_slug": "$repo_name",
	    "project_description": "Imported from template",
	    "python_version": "3.12"
	  }
	}
	EOF  # tweak description/python_version as needed
	BASELINE_REF=952e324f956a682e825ae3df76756aea7b366230
	uvx cookiecutter https://github.com/karthikr-tw/code-agent-aids \
	    --checkout "$BASELINE_REF" \
		--overwrite-if-exists \
	    --skip-if-file-exists \
	    --output-dir "$repo_parent" \
	    --replay-file /tmp/code-agent-replay.json
	```
   Cookiecutter overlays the template into your repo automatically while leaving custom Markdown, prompt, or MCP files intact.
2. **Inspect the diff and delete anything you do not want.** If you skipped a file by mistake, rerun the command without `--skip-if-file-exists` and copy that one path.
3. **Commit the imported baseline.** Cruft can now diff against it.

### Phase 2 — Link + update with Cruft
1. **Clean the working tree.** Commit or stash changes so Cruft can write `.cruft.json`.
2. **Link using the baseline commit you imported.**
	```bash
	uv tool install cruft
	BASELINE_REF=952e324f956a682e825ae3df76756aea7b366230
	uvx cruft link https://github.com/karthikr-tw/code-agent-aids --checkout "$BASELINE_REF" --no-input
	```
   Commit/stash the generated `.cruft.json`, or leave it untracked if you plan to pass `--allow-untracked-files` in the next step.
3. **Upgrade to the template version you need (usually `main`).**
	```bash
	TARGET_REF=main
	uvx cruft update --checkout "$TARGET_REF" --skip-apply-ask --allow-untracked-files
	```
   Drop the `--allow-untracked-files` flag when nothing untracked remains. This step now applies the diff between your baseline and the latest template commit across the files you imported.
4. **Resolve conflicts, run `uv run pytest -q`, and commit.** Future updates reduce to `uvx cruft check` followed by `uvx cruft update`.

Pro tips:
- Record any files you intentionally skipped inside `.cruft.json`’s `"skip": [...]` list (or `[tool.cruft] skip = [...]` in `pyproject.toml`) so future updates never touch them.
- Use `git ls-remote https://github.com/karthikr-tw/code-agent-aids` to find other tags/commits when you need to pin to a release instead of `main`.
- Keep `--allow-untracked-files` handy if you have artifacts you cannot stash; it only suppresses warnings about untracked files.
