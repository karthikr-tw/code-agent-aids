---
name: commit-message-instructions
description: Guidelines for generating commit messages.
applyTo: "**"
---
# Commit Message Guidelines
- Always reference the related ticket ID in the commit message.
- Summarise the changes made in a concise manner.
- Indicate the risk level of the changes (Low, Medium, High).
- Mention any test evidence, such as unit tests added or manual testing performed.
- Format example: `[TICKET-ID] Short summary of changes. Risk: Low/Medium/High. Tests: Unit tests added, manual testing performed.`
- Keep the commit message under 72 characters for the summary line, with additional details in the body if necessary.
- Use imperative mood in the subject line (e.g., "Fix bug" instead of "Fixed bug" or "Fixes bug").
- Separate the subject from the body with a blank line.
- Use bullet points in the body for clarity when listing multiple changes or details.
