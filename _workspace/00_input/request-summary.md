# Request Summary

## Issue

- GitHub issue: #28 `[agent] 공개 후기/SNS 기반 관람 꿀팁 수집 확장`
- Branch: `codex/agent-public-review-tips`

## Scope

- Extend public-search query coverage for public review/SNS practical tips.
- Use public blogs, public review pages, and public-search-discovered SNS snippets as `public_review_reference` only.
- Add public review tip categories for entry/standing, locker, exit/transit, and preparation.
- Keep official information and public-review tips separated in wording; public tips must start with `후기 참고:`.
- Preserve the project boundary: no direct SNS login crawling, page scraping, comments crawling, or login-gated access.
- Preserve frontend -> backend -> agent dependency boundary.

## Validation Plan

- `python3 scripts/validate_harness.py`
- `uv run --python 3.11 pytest`
- Live smoke with Tavily/Gemini/KOPIS runtime env when useful
