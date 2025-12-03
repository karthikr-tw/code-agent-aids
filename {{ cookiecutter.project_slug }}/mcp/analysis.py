# analysis/server.py
"""
Analysis MCP server for the agent-aided-coding demo.

Tools exposed (aligned with mcp/analysis.json):
1. openapi_diff   - Compare two OpenAPI docs and summarise potential breaking changes.
2. a11y_audit     - Flag common accessibility issues in JSX/HTML snippets.
3. test_heuristics - Suggest additional test cases based on a provided diff or source snippet.
"""

from __future__ import annotations

import asyncio
import difflib
import json
import pathlib
import re
from dataclasses import dataclass
from typing import Any, Iterable
from urllib.parse import urlparse

import requests
import yaml
from bs4 import BeautifulSoup
from fastmcp import FastMCP, tools

app = FastMCP("analysis", instructions="Static analysis helpers for the Copilot agent demo.")


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def _load_text(ref: str) -> str:
    """Load text content from a filesystem path or HTTP(S) URL."""
    parsed = urlparse(ref)
    if parsed.scheme in {"http", "https"}:
        response = requests.get(ref, timeout=10)
        response.raise_for_status()
        return response.text
    path = pathlib.Path(ref).expanduser().resolve()
    return path.read_text(encoding="utf-8")


def _load_structured(ref: str) -> dict[str, Any]:
    """Attempt to parse YAML or JSON; fall back to raw text if parsing fails."""
    raw = _load_text(ref)
    try:
        return yaml.safe_load(raw) or {}
    except yaml.YAMLError:
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {"__raw__": raw}


def _flatten_paths(node: Any, prefix: str = "") -> set[str]:
    """Collect dotted paths for keys in a nested dict/list structure."""
    paths: set[str] = set()
    if isinstance(node, dict):
        for key, value in node.items():
            path = f"{prefix}.{key}" if prefix else key
            paths.add(path)
            paths.update(_flatten_paths(value, path))
    elif isinstance(node, list):
        for idx, value in enumerate(node):
            path = f"{prefix}[{idx}]"
            paths.add(path)
            paths.update(_flatten_paths(value, path))
    return paths


def _extract_identifiers(source: str) -> list[str]:
    """Grab function/class signatures from a Python or TypeScript snippet."""
    identifiers: list[str] = []
    for line in source.splitlines():
        line = line.strip()
        if line.startswith("def ") or line.startswith("class "):
            identifiers.append(line.split("(")[0])
        elif line.startswith("function ") or line.startswith("export function "):
            identifiers.append(line.split("(")[0])
    return identifiers


# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------

@dataclass
class DiffSummary:
    added: set[str]
    removed: set[str]

    @property
    def potentially_breaking(self) -> set[str]:
        """Heuristic: removed endpoints or schemas may indicate breaking changes."""
        return {path for path in self.removed if ".paths." in path or ".components.schemas." in path}


@app.tool(
    name="openapi_diff",
    description="Compare two OpenAPI specs and summarise headline differences.",
)
def openapi_diff(baseline: str, candidate: str) -> dict[str, Any]:
    """
    Parameters
    ----------
    baseline: Path/URL to the current OpenAPI document.
    candidate: Path/URL to the proposed OpenAPI document.
    """
    base_doc = _load_structured(baseline)
    cand_doc = _load_structured(candidate)

    base_paths = _flatten_paths(base_doc)
    cand_paths = _flatten_paths(cand_doc)

    summary = DiffSummary(
        added=cand_paths - base_paths,
        removed=base_paths - cand_paths,
    )

    diff_lines = difflib.unified_diff(
        json.dumps(base_doc, indent=2, sort_keys=True).splitlines(),
        json.dumps(cand_doc, indent=2, sort_keys=True).splitlines(),
        fromfile="baseline",
        tofile="candidate",
        lineterm="",
    )

    return {
        "summary": {
            "added_paths": sorted(summary.added),
            "removed_paths": sorted(summary.removed),
            "potentially_breaking": sorted(summary.potentially_breaking),
        },
        "diff_preview": "\n".join(list(diff_lines)[:2000]),  # cap output
    }


A11Y_CHECKS: Iterable[tuple[str, str]] = (
    ("img:not([alt])", "Images should include meaningful alt text."),
    ("button:not([aria-label]):not(:has-text)", "Buttons require visible text or aria-label."),
    ("a[href='#']", "Anchor tags should point to real destinations."),
    ("[role='button']:not([aria-label])", "Interactive elements with role=button need labels."),
    ("input:not([aria-label]):not([id])", "Inputs should be labelled via aria-label or associated <label>."),
)


@app.tool(
    name="a11y_audit",
    description="Audit JSX/HTML markup for common accessibility issues.",
)
def a11y_audit(source: str, context: str | None = None) -> dict[str, Any]:
    """
    Parameters
    ----------
    source: JSX or HTML snippet to analyse.
    context: Optional component or route identifier for labelling.
    """
    soup = BeautifulSoup(source, "html.parser")
    issues: list[dict[str, Any]] = []

    for selector, message in A11Y_CHECKS:
        for el in soup.select(selector):
            snippet = el if isinstance(el, str) else str(el)[:200]
            issues.append({"selector": selector, "message": message, "element": snippet})

    # Check for missing heading hierarchy
    headings = [int(match.group(1)) for match in re.finditer(r"<h([1-6])", source, flags=re.IGNORECASE)]
    if headings:
        if headings[0] != 1:
            issues.append({"selector": "h1", "message": "First heading should usually be <h1> for semantic structure."})
        for prev, current in zip(headings, headings[1:], strict=False):
            if current - prev > 1:
                issues.append({
                    "selector": f"h{current}",
                    "message": f"Heading level jumps from h{prev} to h{current}; avoid skipping levels.",
                })

    return {"context": context or "unknown", "issues": issues, "passed": not issues}


@app.tool(
    name="test_heuristics",
    description="Suggest additional tests based on a diff or source snippet.",
)
def test_heuristics(diff: str, language: str | None = None) -> dict[str, Any]:
    """
    Parameters
    ----------
    diff: Unified diff or code snippet representing recent changes.
    language: Optional hint (python/typescript) to tailor suggestions.
    """
    changed_identifiers = _extract_identifiers(diff)
    risk_areas = []

    if "async" in diff or "await" in diff:
        risk_areas.append("Asynchronous behaviour – include tests for awaited branches and concurrency.")
    if "raise " in diff or "throw " in diff:
        risk_areas.append("Error handling – add tests for raised exceptions and failure paths.")
    if "datetime" in diff or "Date" in diff:
        risk_areas.append("Time-dependent logic – ensure deterministic tests using frozen time or fixtures.")
    if "requests." in diff or "httpx." in diff or "fetch(" in diff:
        risk_areas.append("External IO – mock HTTP clients to cover success and failure scenarios.")

    suggestions = [f"Add unit tests covering {identifier}" for identifier in changed_identifiers]
    suggestions.extend(risk_areas)

    if not suggestions:
        suggestions.append("No obvious targets detected – consider regression tests for the modified modules.")

    return {
        "language": language or "auto",
        "identifiers": changed_identifiers,
        "suggestions": suggestions,
    }


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Launch the FastMCP server."""
    asyncio.run(app.run())


if __name__ == "__main__":
    main()