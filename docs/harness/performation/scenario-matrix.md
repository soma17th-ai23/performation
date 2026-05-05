# Scenario Matrix

Use these cases for smoke testing app behavior, prompts, and harness output.

| ID | Input | Expected Classification | Key Checks |
| --- | --- | --- | --- |
| S1 | `KSPO DOME` | venue_name | venue basics, transit, entry notes, official-check section |
| S2 | `KSPO DOME 콘서트 준비물` | venue_with_detail_question | checklist emphasis, source labels, latest official check |
| S3 | `블루스퀘어` | venue_name | local venue coverage and supported-venue wording |
| S4 | `예스24라이브홀 스탠딩` | venue_with_detail_question | standing-specific uncertainty and official-check wording |
| S5 | unknown small venue | unsupported_or_ambiguous | ask for more detail or say MVP venue support is limited |
| S6 | search API error | provider_failure | local-data fallback and transparent missing-web-evidence note |
| S7 | official source conflicts with public review | conflict | official source wins, public review stays reference-only |

## Minimum Demo Pass

- Run at least S1, S2, S5, and S6 before demo delivery.
- Include exact command output or screenshots in `_workspace/04_demo-qa_report.md` when app code exists.
- For documentation-only changes, verify structure with `python3 scripts/validate_harness.py`.
