# Performation

Performation is an Agentic Workflow demo for 공연 관람 준비 정보. A user enters a concert name or venue name, then the service collects venue basics, public web results, source confidence, and visit-prep checklist items into one guide.

## MVP Direction

- UI: Gradio
- Backend: FastAPI
- Agent workflow: LangGraph
- Search: Tavily or Brave Search style public web search API/MCP
- Data: file-based or in-memory venue data first, database later if needed
- Initial venues: KSPO DOME, Blue Square, YES24 Live Hall

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

- Planning PDF: `/Users/coldmans/Downloads/프로젝트 기획서 양식_23조_공연정보제공서비스.pdf`
- Harness reference: `https://github.com/revfactory/harness`
- Codex-native reference: `https://github.com/SaehwanPark/meta-harness`
