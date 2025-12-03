#!/usr/bin/env python3
"""Cookiecutter hook that seeds a .cruft.json file for downstream repos."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Optional

TEMPLATE_REMOTE = "https://github.com/karthikr-tw/code-agent-aids"
TEMPLATE_CHECKOUT = "main"
TEMPLATE_REFERENCE = "{{ cookiecutter._template }}"

COOKIECUTTER_CONTEXT = {
    "project_name": "{{ cookiecutter.project_name }}",
    "project_slug": "{{ cookiecutter.project_slug }}",
    "project_description": "{{ cookiecutter.project_description }}",
    "python_version": "{{ cookiecutter.python_version }}",
    "_template": TEMPLATE_REMOTE,
}


def _run_git_command(args: list[str]) -> Optional[str]:
    try:
        result = subprocess.run(
            args,
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip() or None


def _resolve_local_template_commit() -> Optional[str]:
    template_path = Path(TEMPLATE_REFERENCE)
    if not template_path.exists():
        return None
    return _extract_commit(_run_git_command(["git", "-C", str(template_path), "rev-parse", "HEAD"]))


def _resolve_remote_template_commit() -> Optional[str]:
    return _extract_commit(
        _run_git_command(["git", "ls-remote", TEMPLATE_REMOTE, TEMPLATE_CHECKOUT])
    )


def _extract_commit(raw: Optional[str]) -> Optional[str]:
    if not raw:
        return None
    line = raw.splitlines()[0].strip()
    return line.split()[0] if line else None


def _write_cruft_file(dest: Path, commit: Optional[str]) -> None:
    state = {
        "template": TEMPLATE_REMOTE,
        "commit": commit,
        "context": {"cookiecutter": COOKIECUTTER_CONTEXT},
        "directory": "",
        "checkout": TEMPLATE_CHECKOUT,
    }
    dest.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    project_dir = Path.cwd()
    cruft_file = project_dir / ".cruft.json"
    if cruft_file.exists():
        print("[post_gen_project] .cruft.json already present; leaving as-is.")
        return

    commit = _resolve_local_template_commit() or _resolve_remote_template_commit()
    _write_cruft_file(cruft_file, commit)

    if commit:
        print(
            f"[post_gen_project] Seeded .cruft.json pinned to {commit[:7]} from {TEMPLATE_CHECKOUT}."
        )
    else:
        print(
            "[post_gen_project] Unable to determine template commit. "
            "Run `uvx cruft link https://github.com/karthikr-tw/code-agent-aids --checkout main` after install to refresh."  # noqa: E501
        )


if __name__ == "__main__":
    main()
