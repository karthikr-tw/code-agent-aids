# code-agent-aids template

Cookiecutter + Cruft template for agent-aided coding workspaces.

## Repository layout
- `cookiecutter.json` — prompts/defaults shown during generation.
- `hooks/` — `post_gen_project.py` seeds `.cruft.json` so downstream repos can `uvx cruft check` / `uvx cruft update` without extra wiring.
- `{{ cookiecutter.project_slug }}/` — the actual project skeleton that becomes the generated repository (docs, `.github`, tests, `main.py`, etc.). Modify files in this folder when evolving the template.

## Generate a project (Cruft recommended)

```bash
uv tool install cookiecutter
uv tool install cruft

# create a new repo that tracks template updates
uvx cruft create https://github.com/karthikr-tw/code-agent-aids

# later, inside the generated repo
uvx cruft check   # see if updates exist
uvx cruft update  # pull changes, then run `uv run pytest -q`
```

If you only need a one-off scaffold, you can run `uvx cookiecutter https://github.com/karthikr-tw/code-agent-aids`—the `hooks/post_gen_project.py` script will still create `.cruft.json`, but you may delete it to opt out of update tracking.

## Adopting the template in an existing repository

Cruft’s [link workflow](https://cruft.github.io/cruft/#linking-an-existing-project) assumes your repo already contains a copy of the template. When you are retrofitting an unrelated project, follow the two-phase process below so you import only the files you really want while protecting project-specific docs or prompts.

### Phase 1 — Import the baseline files via `uvx cookiecutter`
1. **Render straight into your repo using Cookiecutter’s CLI options (no prompts).** The official [command-line docs](https://cookiecutter.readthedocs.io/en/stable/cli_options.html#cmdoption-cookiecutter-replay-file) describe `--replay-file`, which lets you predefine every answer. Combine it with `--skip-if-file-exists` so existing Markdown/prompt files remain untouched:
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
	EOF  # adjust description/python_version if your project needs different values
	BASELINE_REF=952e324f956a682e825ae3df76756aea7b366230
	uvx cookiecutter https://github.com/karthikr-tw/code-agent-aids \
	    --checkout "$BASELINE_REF" \
		--overwrite-if-exists \
	    --skip-if-file-exists \
	    --output-dir "$repo_parent" \
	    --replay-file /tmp/code-agent-replay.json
	```
   Cookiecutter now writes the template into your existing repo folder without prompting and without overwriting files that already exist.
2. **Review the git diff.** Delete anything you do not want, or add missing docs by re-running the same command without `--skip-if-file-exists` for targeted paths.
3. **Commit this baseline snapshot.** Cruft now has something concrete to diff against.

### Phase 2 — Link and let Cruft manage future diffs
1. **Clean working tree again** (commit or stash any changes, especially `.cruft.json`).
2. **Link with the baseline commit you imported.**
	```bash
	uv tool install cruft
	BASELINE_REF=952e324f956a682e825ae3df76756aea7b366230
	uvx cruft link https://github.com/karthikr-tw/code-agent-aids --checkout "$BASELINE_REF" --no-input
	```
   Commit or stash the `.cruft.json` that gets created (or keep it untracked and pass `--allow-untracked-files` in the next step).
3. **Run the upgrade you actually care about.**
	```bash
	TARGET_REF=main
	uvx cruft update --checkout "$TARGET_REF" --skip-apply-ask --allow-untracked-files
	```
   Drop `--allow-untracked-files` if your working tree is clean. The moment this succeeds you now have a repo containing template files plus a `.cruft.json` pointing at the latest commit.
4. **Resolve conflicts, run `uv run pytest -q`, and commit.** Future maintenance is the normal `uvx cruft check` / `uvx cruft update` loop.

Tips:
- When importing the baseline, keep a list of files you intentionally skipped; add them to `.cruft.json`’s `skip` stanza (or `pyproject.toml`’s `[tool.cruft] skip = [...]`) so future `cruft update` runs never clobber them.
- `git ls-remote https://github.com/karthikr-tw/code-agent-aids` shows every tag/commit you can use for `BASELINE_REF` or `TARGET_REF`.
- If your repo contains large untracked artifacts you cannot stash, keep using the `--allow-untracked-files` option. It mirrors Cruft’s documented CLI flag and only ignores untracked paths.

## Maintaining the template locally
1. Edit files under `{{ cookiecutter.project_slug }}/` (or adjust prompts/hooks as needed).
2. Dry-run the template without pushing: `uvx cookiecutter . --no-input --output-dir /tmp` or interactively to test prompt changes.
3. Once satisfied, commit and push so others can consume via `uvx cruft create https://github.com/karthikr-tw/code-agent-aids`.

Generated projects contain their own README (`{{ cookiecutter.project_slug }}/README.md`) with full developer setup instructions.
