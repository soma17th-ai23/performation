# Request Summary

## Issue

- GitHub issue: #24 `[agent] KOPIS 공연 공식 데이터 조회 도구 추가`

## Scope

- Add optional KOPIS official performance lookup for concert/event queries.
- Convert KOPIS XML performance list results into existing `SearchResult` evidence.
- Preserve Tavily/Brave public search and local venue fallback behavior when KOPIS is unconfigured or unavailable.
- Classify KOPIS sources as `official_confirmed`.
- Preserve frontend -> backend -> agent dependency boundary.

## Validation Plan

- `python3 scripts/validate_harness.py`
- `uv run --python 3.11 pytest`
