# Delivery Summary

## Issue

- #30 `[agent] 외부 검색/LLM 호출 캐싱 추가`

## Changes

- Added a small in-memory TTL cache utility for agent provider calls.
- Cached successful public search results by provider/query/purpose/max result count.
- Cached successful KOPIS official search results by query and provider date-window settings.
- Cached successful Gemini guide drafts by provider/model/prompt hash.
- Serialized same-key cache misses with a per-key lock so concurrent requests do not repeat the same external provider factory call.
- Added cache controls:
  - `PERFORMATION_CACHE_ENABLED`
  - `PERFORMATION_CACHE_TTL_SECONDS`
  - `PERFORMATION_SEARCH_CACHE_TTL_SECONDS`
  - `PERFORMATION_KOPIS_CACHE_TTL_SECONDS`
  - `PERFORMATION_LLM_CACHE_TTL_SECONDS`
  - `PERFORMATION_CACHE_MAX_ITEMS`
- Kept provider failures uncached so transient failures can recover on the next request.

## Validation

- `uv run --python 3.11 pytest tests/test_cache_tool.py tests/test_search_tool.py tests/test_kopis_tool.py tests/test_llm_tool.py` - pass, 32 passed
- `uv run --python 3.11 pytest` - pass, 109 passed
- `python3 scripts/validate_harness.py` - pass
- `git diff --check` - pass
- Repeated live `워터밤` smoke with Tavily+Gemini+KOPIS runtime env - pass, first run about 16.21s and second cached run about 0.00s.
