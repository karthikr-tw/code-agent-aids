

# Copilot repository instructions

This file defines **repository-wide instructions** for GitHub Copilot Chat, Copilot code review, and agent mode. Use it to tell Copilot how to understand, build, test, and safely change this codebase.

---

## Project overview

> TODO: Replace this with a concise project description.

- Tech stack and major components (backend, frontend, infra, data).
- Primary use cases or workflows this repo implements.
- Links to architectural docs or ADRs (for example: `docs/architecture.md`, `AGENTS.md`).

---

## Build & test

> TODO: Replace this with the canonical build/test commands.

Describe how to build and test the project **as Copilot should do it**:

- **Build**
  - Example: `npm install && npm run build`
  - Example: `uv sync && uv run pytest`
- **Test**
  - Unit tests: `…`
  - Integration/E2E tests: `…`
- **Pre-merge checks**
  - Linters, formatters, type-checkers, security scanners.
  - Any required CI pipeline steps Copilot should respect.

Keep these commands stable; if they change, update this section before relying on Copilot for larger edits.

---

## Coding standards

> TODO: Link to or summarise your main standards/guides.

- Preferred languages, frameworks, and patterns for new code.
- Style guides:
  - Formatting (prettier/black/clang-format/etc.).
  - Naming conventions and file layout.
- Error handling and logging expectations:
  - When to throw/return errors vs. logging and continuing.
  - Required logging fields for important operations.
- Performance & resource rules:
  - Known hot paths.
  - Constraints on allocations, network calls, or database access.

If there is a dedicated style guide, link it here instead of duplicating it.

---

## Instruction layering

Copilot may combine multiple instruction sources. Use this precedence model:

1. **Global repo instructions** — this file (`.github/copilot-instructions.md`).
2. **Path-scoped instructions** — `.github/instructions/*.instructions.md`:
   - Narrow rules for specific areas (e.g., `backend`, `frontend`, `infra`, `data`).
3. **Agent instructions** — `AGENTS.md` and `.github/agents/*.agent.md`:
   - Define agent roles (planner, implement, review, tests, docs, requirement-parser, etc.).
   - Declare allowed tools, MCP servers, and handoffs.
4. **Model-specific guidance** — `CLAUDE.md`, `GEMINI.md`, or similar:
   - When to use which model.
   - Model-specific strengths/limitations.
5. **Prompt files** — `.github/prompts/*.prompt.md`:
   - Reusable workflows (plan, implement, refactor, review, tests, docs, migrations, etc.).

Guidelines:

- Keep **global rules** here; move domain-specific rules into `*.instructions.md`.
- Avoid duplicating content. Link instead:
  - Example: `[Commit message rules](instructions/commit-message.instructions.md)`
  - Example: `[Planner agent](agents/plan.agent.md)`
- When adding new instructions, include:
    - A short `description` (frontmatter) for each file.
    - Clear section headings that map to concrete behaviours (build, tests, error handling, etc.).

---

## Agent mode expectations

These rules apply to Copilot agents operating on this repo (planner, implement, review, tests, docs, etc.):

- **Scope & safety**
  - Prefer **small, incremental changes** over large speculative refactors.
  - Never introduce new frameworks or major dependencies without explicit instructions.
  - Treat anything destructive (schema changes, data migrations, shell commands that delete/modify system state) as **high risk** and require explicit human approval.

- **Commands & tools**
  - Always surface proposed commands clearly and wait for approval before running them.
  - Follow the canonical build/test commands defined in the **Build & test** section.
  - Honour workspace settings for `chat.tools.terminal.autoApprove` and `chat.tools.global.autoApprove`—do not assume auto-approval even if enabled. :contentReference[oaicite:1]{index=1}  

- **Working tree hygiene**
  - Keep diffs focused and grouped logically.
  - Do not mix unrelated refactors with feature work.
  - Keep generated files, lockfiles, and migrations consistent with repo conventions.

---

## Prompting & workflow best practices

For humans using Copilot on this repo:

- **Provide context**
  - Reference files or symbols directly (via `#file`, `#codebase`, or selections).
  - Paste or link relevant specs, ADRs, and tickets.
  - Mention the relevant instructions:
    - Example: “Follow [Commit message rules](instructions/commit-message.instructions.md) and the `planner` agent.”

- **Break work into steps**
  - Start with a **planner** agent or planning prompt for complex changes.
  - Use **implement** for scoped coding tasks.
  - Use **review** to validate correctness, security, and compliance.
  - Use **tests** to add or improve test coverage only.
  - Use **docs** to update READMEs, architecture notes, and onboarding docs.

- **Ask for validation**
  - When requesting changes, also request:
    - Tests (unit/integration/E2E as appropriate).
    - Documentation updates if behaviour or APIs change.
    - Logging or telemetry updates for critical paths.

- **Use prompt files for repeatable tasks**
  - Trigger reusable prompts by typing `/` in chat and picking from `.github/prompts/*.prompt.md`.
  - Prefer prompt files for:
    - Standard reviews (security, performance, API changes).
    - Common refactor patterns.
    - Cross-cutting concerns (logging, metrics, error handling).

---

## Customisation map

Use this repo layout as the “map” for Copilot customisation:

- **Global instructions (this file)**  
  `.github/copilot-instructions.md` — repo-wide rules for chat, code review, and agents.

- **Scoped rules**  
  `.github/instructions/*.instructions.md` — path/domain-specific rules. Use YAML frontmatter (`description`, optional `name`, optional `appliesTo`) and headings to describe scope. :contentReference[oaicite:2]{index=2}  

- **Agent personas**  
  `.github/agents/*.agent.md` — define:
  - `name`, `description`, `tools`, `mcp-servers`, and `handoffs`.
  - Behaviour sections (Operating mode, Tool usage, Instructions & scope, Safety, Summary).

- **AGENTS index**  
  `AGENTS.md` (root and optionally nested):
  - High-level overview of available agents and their roles.
  - Links to `*.agent.md` files and relevant instructions.

- **Reusable prompts**  
  `.github/prompts/*.prompt.md` — structured prompt files with:
  - `description`, `name`, `argument-hint`, `agent`, and optionally `model`/`tools`. :contentReference[oaicite:3]{index=3}  

- **Model-specific guidance**  
  `CLAUDE.md`, `GEMINI.md`, `GPT.md`, etc. — when and how to use each model family, especially in regulated or performance-critical contexts.

- **MCP tooling**  
  `mcp/*.json` — manifests describing external tools and APIs available to agents.
  - Reference them in agent frontmatter via `mcp-servers`.
  - Ensure required secrets are in environment variables, not hard-coded.

---

## Guidance for Copilot coding & code review

These rules apply to Copilot code review and coding agents as well as IDE agent mode: :contentReference[oaicite:4]{index=4}  

- **Always use tests**
  - Run or propose tests relevant to the change.
  - Never mark changes “ready” if tests are failing without clear explanation and acceptance.

- **Respect contracts**
  - When changing APIs:
    - Update backend handlers, shared models, frontend types, and tests together.
    - Note breaking changes clearly and, where required, version APIs.
  - Keep database schemas, migrations, and ORMs consistent and reversible.

- **No surprise frameworks**
  - Don’t introduce new frameworks, ORMs, or major dependencies unless explicitly requested.
  - Prefer extending existing patterns.

- **Follow scoped instructions**
  - Before suggesting or applying changes, check:
    - Relevant `*.instructions.md` for the path.
    - Relevant sections in `AGENTS.md`.
  - If instructions conflict, prefer the more specific/path-scoped rule and call out the conflict in the response.

---

## VS Code configuration checklist (optional but recommended)

These workspace settings help wire this repo’s instructions, agents, and prompts into VS Code: :contentReference[oaicite:5]{index=5}  

In `.vscode/settings.json`:

```jsonc
{
  // Use repo-wide instructions from this file
  "github.copilot.chat.codeGeneration.useInstructionFiles": true,

  // Instruction files
  "chat.instructionsFilesLocations": {
    ".github/instructions": true
  },

  // Agent files (custom agents)
  "chat.agentsFilesLocations": {
    ".github/agents": true
  },
  "chat.useAgentsMdFile": true,
  "chat.useNestedAgentsMdFiles": true,

  // Prompt files
  "chat.promptFilesLocations": {
    ".github/prompts": true
  },
  "chat.promptFilesRecommendations": true,

  // MCP servers (example)
  // "chat.mcpServers": {
  //   "analysis": {
  //     "command": "node",
  //     "args": ["./mcp/analysis-server.js"]
  //   }
  // }
}
