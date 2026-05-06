# Delivery Summary

## Issue

- #24 `[agent] KOPIS 공연 공식 데이터 조회 도구 추가`

## Changes

- Added an optional KOPIS performance-list provider that reads `KOPIS_API_KEY`.
- Converted KOPIS XML performance results into existing `SearchResult` evidence.
- Added a `search_kopis_official` workflow node after public web search.
- Classified KOPIS evidence as `official_confirmed` for source, event info, and candidate flows.
- Documented KOPIS env settings and updated harness/project docs to include official performance lookup.
- Filtered KOPIS short-term false positives so `EK` does not match unrelated titles like `WEEK` or `NEKIRU`.
- Expanded official event candidates to include non-MVP regions from KOPIS, verified with `워터밤 서울` and `워터밤 속초`.
- Addressed PR review feedback by using canonical HTTPS KOPIS transport, bounding lookahead days, hardening XML parsing, and prioritizing KOPIS evidence before public search results.
- Added KOPIS alias expansion for known Korean event names, starting with `랩비트` -> `RAPBEAT` / `RAP BEAT` variants.

## Validation

- `python3 scripts/validate_harness.py` - pass
- `uv run --python 3.11 pytest` - pass, 78 passed
- `git diff --check` - pass
- Manual smoke:
  - KOPIS key injected through hidden stdin/env + `generate_visit_guide("EK 콘서트")` returned YES24 Live Hall, `2026년 5월 10일`, `official_confirmed`
  - KOPIS key injected through hidden stdin/env + `generate_visit_guide("워터밤")` returned 서울/속초 official candidates
  - `랩비트 페스티벌` returned no KOPIS result, so it remains covered by public search/fallback behavior
  - Alias-expanded `랩비트 페스티벌` KOPIS smoke still returned no current KOPIS result
