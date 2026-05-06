# Performation

Performation is an Agentic Workflow demo for 공연 관람 준비 정보. A user enters a concert name or venue name, then the service collects venue basics, public web results, source confidence, and visit-prep checklist items into one guide.

## MVP Direction

- UI: Gradio
- Backend: FastAPI
- Agent workflow: LangGraph
- Search: KOPIS official performance data plus Tavily or Brave Search style public web search API/MCP
- Data: file-based or in-memory venue data first, database later if needed
- Initial venues: KSPO DOME, Blue Square, YES24 Live Hall

## Monorepo Layout

```text
apps/
  frontend/      # Gradio UI. Calls backend API only.
  backend/       # FastAPI API. Owns agent workflow execution.
packages/
  agent/         # LangGraph-oriented workflow and guide generation.
  domain/        # Shared request/response schema and confidence labels.
  venue-data/    # MVP fallback venue data and loader.
tests/           # Smoke tests and architecture boundary tests.
```

Application dependency direction:

```text
frontend -> backend -> agent -> venue-data/domain
```

The frontend must not import `performation_agent` or read venue fixtures directly. The backend is the only layer that invokes the agent workflow.

## Local Setup

```bash
uv sync --python 3.11
```

Run tests:

```bash
uv run --python 3.11 pytest
```

Run backend:

```bash
PYTHONPATH=apps/backend/src:packages/agent/src:packages/domain/src:packages/venue-data/src uv run --python 3.11 uvicorn performation_backend.main:app --reload
```

Backend API contract:

- `GET /health`: health check.
- `POST /guides`: canonical guide generation endpoint.
- `POST /analyze`: compatibility alias for backlog and frontend integration discussions.
- Request body: `{ "query": "예스24라이브홀 스탠딩" }`
- Blank or whitespace-only `query` values are rejected before agent execution.
- Successful guide responses follow the shared `GuideResponse` schema from `packages/domain`.

Optional agent data sources:

- `KOPIS_API_KEY`: enables KOPIS official performance lookup for concert/event queries.
- `TAVILY_API_KEY` or `BRAVE_SEARCH_API_KEY`: enables public web search for venue, entry, transit, locker, and review context.
- `GEMINI_API_KEY`: enables LLM-assisted guide drafting; deterministic fallback remains available without it.

Public web search may surface official SNS notice links. The agent treats them as latest official-check channels only when the result text indicates an official account or official notice; it does not log in to or directly crawl SNS platforms.

Run frontend in another terminal:

```bash
PYTHONPATH=apps/frontend/src uv run --python 3.11 python -m performation_frontend.app
```

The frontend uses `PERFORMATION_API_URL` and defaults to `http://127.0.0.1:8000`.

## Harness Setup

This repository includes a Harness-style team architecture adapted from `revfactory/harness` and installed in a Codex-friendly layout:

- `.agents/skills/harness/`: shared portable Harness meta-skill
- `.codex/skills/harness/`: Codex-native mirror of the shared Harness skill
- `.agents/skills/performation-*`: project-specific reusable skills
- `.codex/skills/performation-*`: Codex discovery mirrors for project-specific skills
- `.claude/agents/performation-*.md`: Claude Code compatible agent cards
- `docs/harness/performation/`: durable team spec, output contract, and scenario docs
- `docs/harness/performation/git-policy.md`: Korean commit rules and message types

Start with:

```bash
python3 scripts/validate_harness.py
```

Then read:

- `docs/project-brief.md`
- `docs/harness/performation/team-spec.md`
- `docs/harness/performation/git-policy.md`
- `.agents/skills/performation-orchestrator/SKILL.md`

## Source Documents

- Project brief: `docs/project-brief.md`
- Original planning PDF is not committed to this repository.
- Harness reference: `https://github.com/revfactory/harness`
- Codex-native reference: `https://github.com/SaehwanPark/meta-harness`
