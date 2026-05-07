# Request Summary

## Issue

- GitHub issue: #30 `[agent] 외부 검색/LLM 호출 캐싱 추가`
- Branch: `codex/agent-provider-cache`

## Scope

- Add in-memory TTL caching for external provider calls.
- Cache public search results, KOPIS official search results, and Gemini guide draft output.
- Keep cache configurable with env vars for enable/disable, TTL, and max entries.
- Do not cache provider failures or exceptions.
- Avoid storing API keys or secrets in cache keys.
- Preserve frontend -> backend -> agent dependency boundary.

## Validation Plan

- `python3 scripts/validate_harness.py`
- `uv run --python 3.11 pytest`
- Provider call-count regression tests
- Repeated-query smoke with Tavily/Gemini/KOPIS runtime env when useful
