# Request Summary

## Issue

- GitHub issue: #14 `[agent] 공연명 단독 입력 검색 기반 공연장 추론`

## Scope

- Improve agent-side venue inference for concert-name-only queries.
- Infer an MVP venue from public search results only when exactly one supported venue appears.
- Keep unsupported or multi-venue search evidence ambiguous.
- Preserve frontend -> backend -> agent dependency boundary.

## Validation Plan

- `python3 scripts/validate_harness.py`
- `uv run --python 3.11 pytest`
