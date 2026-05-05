# Request Summary

## Issue

- GitHub issue: #12 `[agent] 공연명 입력 분석 및 공연장 추론 개선`

## Scope

- Improve agent-side input analysis for concert-like queries.
- Infer MVP venues from venue aliases and compact hints such as `KSPO`.
- Keep unsupported concert names ambiguous when no supported venue hint exists.
- Preserve frontend -> backend -> agent dependency boundary.

## Validation Plan

- `python3 scripts/validate_harness.py`
- `uv run --python 3.11 pytest`
