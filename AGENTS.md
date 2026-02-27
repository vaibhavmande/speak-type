# AGENTS HANDBOOK

## Purpose
This document describes the baseline expectations for any autonomous or semi-autonomous developer agent contributing to the Speak-Type codebase. Follow these guardrails to maintain high-quality, auditable work that is easy for humans to review and continue.

## Core Principles
1. **Incremental delivery** – Produce code in reviewable blocks. Each block should be coherent, testable, and scoped narrowly enough that a human reviewer can understand it without tracing unrelated logic.
2. **Transparency** – Explain *why* decisions are made. Every non-trivial change should include comments or documentation updates capturing the rationale.
3. **Safety first** – Never compromise secrets, stability, or system integrity for speed.
4. **Context stewardship** – Maintain situational awareness of current instructions, prior decisions, and document updates. If context is nearing limits, trigger a handover record immediately.

## Coding Workflow
- Break features/bug fixes into small, logical commits or PR-ready bundles.
- Prefer minimal, targeted changes that solve the root cause.
- Treat warnings, test failures, and lints as blockers until resolved or explicitly triaged.
- Write descriptive commit messages (when committing) that summarize both *what* and *why*.
- Ensure adequate test coverage; add regression tests when fixing bugs whenever feasible.

## Secret & Key Management
- **Never** add plaintext secrets, API keys, certificates, or tokens to the repository.
- Warn loudly before attempting to commit changes that might include secrets (e.g., `.env`, credential files, debug dumps).
- Use environment variables, secret managers, or encrypted storage according to project conventions.
- Git history must stay free of sensitive data; if contamination occurs, escalate immediately for history rewriting.

## Command Safety
- Do **not** run destructive shell commands such as `rm -rf`, force pushes, or system-altering operations without explicit human approval.
- When in doubt, seek confirmation before executing commands that mutate the environment outside the repository.
- Prefer built-in project tooling (scripts, package managers) over ad-hoc commands; document any deviations.

## Commenting & Documentation
- Every significant code block should include comments clarifying intent or trade-offs, not just mechanics.
- Keep architectural docs, READMEs, and runbooks synchronized with decisions made during implementation. Update affected documents as part of the same change whenever possible.
- When adding new patterns or conventions, document them immediately so future agents understand the precedent.

## Context Monitoring & Handover Protocol
- Continuously monitor conversation or instruction context length. If it approaches capacity or critical instructions risk being truncated, begin a **handover document**.
- Handover docs must summarize:
  - Current objective and status.
  - Key decisions and rationale.
  - Open questions, risks, and blockers.
  - Next actionable steps for the succeeding agent.
- Store or share the handover document where the next agent can easily find it (e.g., `/handoffs/<date>-<topic>.md`).

## Documentation Maintenance
- Whenever a decision impacts architecture, processes, or dependencies, revisit relevant docs (`architecture.md`, runbooks, workflow guides) and keep them current.
- Treat documents as living artifacts; outdated guidance is a bug. Schedule time in each task to verify whether documentation needs updates.

## Review Readiness Checklist
1. Code organized into reviewer-friendly chunks.
2. Tests (unit/integration) added or updated as needed and passing.
3. Comments explain intent and rationale.
4. Secrets verified absent; tooling alerted if necessary.
5. Documentation updated to reflect new decisions.
6. Context health confirmed or handover document prepared.

Following these practices ensures that human collaborators can trust agent contributions, keep momentum across context windows, and maintain a secure, high-quality codebase.
