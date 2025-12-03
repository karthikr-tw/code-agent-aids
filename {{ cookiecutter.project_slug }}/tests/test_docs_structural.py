import os
import re
from pathlib import Path
from typing import Optional

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _extract_yaml_block(text: str, fence: Optional[str] = None) -> str:
    """Extract YAML frontmatter inside an optional fenced block, with fallback.

    Some files (like prompts) may omit the ```prompt fence and start directly with
    `---`. This helper first tries to locate the specified fence; if not found, it
    falls back to detecting top-of-file YAML blocks.
    """

    if fence:
        idx = text.find(fence)
        if idx != -1:
            # find first '---' after fence
            rest = text[idx + len(fence):]
            start = rest.find('---')
            if start != -1:
                start += idx + len(fence)
                # find the next '---' after start
                end = text.find('---', start + 3)
                if end != -1:
                    return text[start + 3:end]

    return _extract_unfenced_yaml(text)


def _extract_unfenced_yaml(text: str) -> str:
    stripped = text.lstrip()
    if not stripped.startswith('---'):
        return ""

    lines = stripped.splitlines()
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == '---':
            return '\n'.join(lines[1:i])
    return ""


def _has_key_in_yaml(yaml_text: str, key: str) -> bool:
    # simple regexp to find key: value (allowing spaces)
    pattern = re.compile(r'^\s*' + re.escape(key) + r'\s*:\s*\S+', re.MULTILINE)
    return bool(pattern.search(yaml_text))


def test_prompts_have_frontmatter():
    prompts_dir = ROOT / '.github' / 'prompts'
    assert prompts_dir.exists(), f"Prompts directory not found at {prompts_dir}"
    prompt_files = list(prompts_dir.glob('*.prompt.md'))
    assert prompt_files, "No prompt files found in .github/prompts"

    for p in prompt_files:
        content = p.read_text(encoding='utf-8')
        yaml_block = _extract_yaml_block(content, '```prompt')
        assert yaml_block, f"Missing YAML frontmatter in {p.name} (expected inside a ```prompt fenced block)"
        assert _has_key_in_yaml(yaml_block, 'name'), f"Prompt {p.name} missing 'name' in frontmatter"
        assert _has_key_in_yaml(yaml_block, 'description'), f"Prompt {p.name} missing 'description' in frontmatter"
        assert _has_key_in_yaml(yaml_block, 'agent'), f"Prompt {p.name} missing 'agent' in frontmatter"


def test_agent_files_have_frontmatter():
    agents_dir = ROOT / '.github' / 'agents'
    assert agents_dir.exists(), f"Agents directory not found at {agents_dir}"
    agent_files = list(agents_dir.glob('*.agent.md'))
    assert agent_files, "No agent files found in .github/agents"

    for a in agent_files:
        content = a.read_text(encoding='utf-8')
        # agent files may use different fences; prefer ```chatagent, fall back to first ```
        yaml_block = _extract_yaml_block(content, '```chatagent')
        if not yaml_block:
            # try any fenced block starting with ```
            idx = content.find('```')
            if idx != -1:
                # take substring from the first fence
                rest = content[idx:]
                yaml_block = _extract_yaml_block(rest, '```')
        assert yaml_block, f"Missing YAML frontmatter in {a.name} (expected inside a fenced block)"
        assert _has_key_in_yaml(yaml_block, 'name'), f"Agent file {a.name} missing 'name' in frontmatter"
        assert _has_key_in_yaml(yaml_block, 'description'), f"Agent file {a.name} missing 'description' in frontmatter"
        # tools may be a YAML list; check for the 'tools' key presence
        assert re.search(r'^\s*tools\s*:', yaml_block, re.MULTILINE), f"Agent file {a.name} missing 'tools' entry in frontmatter"


def test_copilot_instructions_have_description():
    f = ROOT / '.github' / 'copilot-instructions.md'
    assert f.exists(), f"Global instructions file not found at {f}"
    content = f.read_text(encoding='utf-8')
    yaml_block = _extract_yaml_block(content, '```instructions')
    assert yaml_block, "Missing YAML frontmatter in .github/copilot-instructions.md (expected inside a ```instructions fenced block)"
    assert _has_key_in_yaml(yaml_block, 'description'), "Global instructions missing 'description' in frontmatter"


def test_no_forbidden_tokens_if_configured():
    # Optional: if tests/forbidden_tokens.txt exists, load tokens (one per line) and assert none appear in docs
    cfg = ROOT / 'tests' / 'forbidden_tokens.txt'
    if not cfg.exists():
        pytest.skip('No forbidden token list configured (tests/forbidden_tokens.txt missing)')

    tokens = [line.strip() for line in cfg.read_text(encoding='utf-8').splitlines() if line.strip() and not line.strip().startswith('#')]
    assert tokens, 'forbidden_tokens.txt is empty'

    # search docs and prompts for tokens
    search_paths = [ROOT / '.github', ROOT]
    occurrences = []
    for p in search_paths:
        for fpath in p.rglob('*.md'):
            # skip tests/ itself
            if 'tests/forbidden_tokens.txt' in str(fpath):
                continue
            text = fpath.read_text(encoding='utf-8')
            for t in tokens:
                if t in text:
                    occurrences.append((str(fpath), t))
    assert not occurrences, f"Forbidden tokens found: {occurrences}"
