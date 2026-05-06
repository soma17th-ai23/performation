# Request Summary

## Issue

- GitHub issue: #22 `[backend] /analyze 호환 엔드포인트와 입력 검증 추가`

## Scope

- Keep `POST /guides` as the canonical guide generation endpoint.
- Add `POST /analyze` as a compatibility alias for backlog and frontend integration discussions.
- Normalize request `query` values before agent execution and reject blank or whitespace-only input.
- Preserve frontend -> backend -> agent dependency boundary.

## Validation Plan

- `python3 scripts/validate_harness.py`
- `uv run --python 3.11 pytest`
