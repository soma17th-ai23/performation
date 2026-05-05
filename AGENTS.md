# Repository Agents Guide

Keep this file short and repo-wide. Put role-specific workflow details in the harness docs and skills linked below.

## What

- Performation is a local Agentic Workflow demo that creates concert and venue visit-prep guides from venue data and public web information.
- Planned stack: FastAPI backend, Gradio UI, LangGraph workflow, Tavily or Brave Search, and file-based or in-memory venue data for the MVP.
- Canonical harness artifacts live in `docs/harness/performation/` and `.agents/skills/performation-*`.
- Codex can discover the same workflow through `.codex/skills/`; Claude Code compatibility cards live in `.claude/agents/`.

## Why

- The product promise is practical: help first-time concertgoers find entry, transit, locker, preparation, source, and official-check information without visiting many search channels manually.
- The core safety boundary is source confidence. Official sources must be separated from public reviews, and uncertain or event-specific information must be marked as requiring latest official confirmation.
- MVP scope is intentionally narrow: KSPO DOME, Blue Square, YES24 Live Hall, public web search, and no SNS login crawling, ticketing, payments, seat-view image collection, real-time crowding, or real-time merch stock.

## How

- Before implementation or review, read `docs/project-brief.md` and `docs/harness/performation/team-spec.md`.
- Use `_workspace/` for deterministic phase handoffs and review evidence.
- Use the `performation-orchestrator` skill for end-to-end feature work, and route focused work to the specialist skills under `.agents/skills/performation-*`.
- Verify harness structure with `python3 scripts/validate_harness.py`.
- Before committing, follow `docs/harness/performation/git-policy.md`; use commit messages like `feat: 한글 요약`, `fix: 한글 요약`, or `test: 한글 요약`.
- When application code is added, update this file with the exact build, test, and run commands.
