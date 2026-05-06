# Delivery Summary

## Issue

- #24 `[agent] KOPIS 공연 공식 데이터 조회 도구 추가`

## Changes

- Added an optional KOPIS performance-list provider that reads `KOPIS_API_KEY`.
- Converted KOPIS XML performance results into existing `SearchResult` evidence.
- Added a `search_kopis_official` workflow node after public web search.
- Classified KOPIS evidence as `official_confirmed` for source, event info, and candidate flows.
- Documented KOPIS env settings and updated harness/project docs to include official performance lookup.

## Validation

- `python3 scripts/validate_harness.py`
- `uv run --python 3.11 pytest`
- Manual smoke:
  - no `KOPIS_API_KEY` configured locally, so the agent skips KOPIS and continues with existing search/fallback behavior
