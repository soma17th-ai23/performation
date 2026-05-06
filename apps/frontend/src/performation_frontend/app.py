from __future__ import annotations

import os
from typing import Any

import gradio as gr
import httpx


API_URL = os.getenv("PERFORMATION_API_URL", "http://127.0.0.1:8000").rstrip("/")


def request_guide(query: str) -> str:
  query = query.strip()
  if not query:
    return "공연명 또는 공연장명을 입력해주세요."

  try:
    response = httpx.post(f"{API_URL}/guides", json={"query": query}, timeout=30.0)
    response.raise_for_status()
  except httpx.HTTPError as exc:
    return f"백엔드 API 호출에 실패했습니다: {exc}"

  return render_guide_markdown(response.json())


def render_guide_markdown(guide: dict[str, Any]) -> str:
  venue = guide.get("venue") or {}
  candidates = guide.get("event_candidates") or []
  sources = guide.get("sources") or []

  sections = [
    "# 공연 관람 준비 가이드",
    f"**입력:** {guide.get('input', '')}",
    "",
    "## 공연장 기본 정보",
    f"- 공연장: {venue.get('name', '지원 범위 밖 또는 확인 필요')}",
    f"- 주소: {venue.get('address', '확인 필요')}",
    f"- 가까운 역: {venue.get('nearest_station', '확인 필요')}",
    "",
    "## 관람 전 핵심 요약",
    *[f"- {item}" for item in guide.get("summary", [])],
    "",
    *render_candidate_section(candidates),
    "",
    "## 준비물 체크리스트",
    *[f"- [ ] {item}" for item in guide.get("checklist", [])],
    "",
    "## 교통 및 입장 팁",
    *[f"- {item}" for item in guide.get("transit_and_entry_tips", [])],
    "",
    "## 공식 확인 필요 항목",
    *[f"- {item}" for item in guide.get("official_check_required", [])],
    "",
    "## 참고 출처",
    *[
      f"- {source.get('title', '출처')} ({source.get('source_type', 'uncertain')}): {source.get('url', '')}"
      for source in sources
    ],
    "",
    "## 신뢰도 메모",
    *[f"- {item}" for item in guide.get("confidence_notes", [])],
  ]

  return "\n".join(sections)


def render_candidate_section(candidates: list[dict[str, Any]]) -> list[str]:
  if not candidates:
    return []
  lines = ["## 공연 후보"]
  for candidate in candidates:
    meta = " / ".join(
      item
      for item in (
        candidate.get("region", ""),
        candidate.get("date_text", ""),
        candidate.get("venue_name", ""),
      )
      if item
    )
    label = candidate.get("name", "후보")
    confidence = candidate.get("confidence_label", "uncertain")
    suffix = f" - {meta}" if meta else ""
    lines.append(f"- {label}{suffix} ({confidence})")
  return lines


def build_app() -> gr.Blocks:
  with gr.Blocks(title="Performation") as demo:
    gr.Markdown("# Performation")
    gr.Markdown("공연명 또는 공연장명을 입력하면 백엔드 API를 통해 관람 준비 가이드를 생성합니다.")
    query = gr.Textbox(
      label="공연명 또는 공연장명",
      placeholder="예: KSPO DOME 콘서트 준비물",
    )
    output = gr.Markdown()
    submit = gr.Button("가이드 생성", variant="primary")
    submit.click(fn=request_guide, inputs=query, outputs=output)
  return demo


if __name__ == "__main__":
  build_app().launch()
