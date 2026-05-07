# Delivery Summary

## Issue

- #28 `[agent] 공개 후기/SNS 기반 관람 꿀팁 수집 확장`

## Changes

- Added public-review tip search coverage:
  - `관람 후기 꿀팁`
  - `입장 대기 스탠딩 후기`
  - `물품보관 퇴장 교통 후기`
- Expanded SNS/community domains for public-search-discovered evidence, including TikTok, Facebook, and Weverse.
- Added deterministic public-review tip extraction for entry/standing, locker, exit/transit, and preparation categories.
- Preserved trust boundaries:
  - practical tips are emitted as `후기 참고:`
  - public review/SNS tips remain `public_review_reference`
  - official-check items remain separate from anecdotal tips
- Added review tips to performance-name-only flows, including broad `event_candidates` responses.
- Updated LLM prompt payload with public-review snippets and tip candidates while keeping secrets out of prompts.
- Added cap/dedupe handling so review tips do not flood the response when LLM output is verbose.

## Validation

- `uv run --python 3.11 pytest tests/test_agent_workflow.py tests/test_source_classifier.py tests/test_llm_tool.py` - pass, 75 passed
- `uv run --python 3.11 pytest` - pass, 100 passed
- `python3 scripts/validate_harness.py` - pass
- `git diff --check` - pass
- Live smoke covered `KSPO DOME 스탠딩`, `YES24 Live Hall 물품보관`, and `워터밤 준비물 꿀팁` with Tavily+Gemini and KOPIS configured through runtime env.
- Performance-name-only smoke covered `워터밤` and `세븐틴 콘서트`.
