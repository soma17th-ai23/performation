from __future__ import annotations

from performation_agent.state import GuideState


def assign_confidence(state: GuideState) -> GuideState:
  if state.get("venue") is None:
    confidence_notes = ["지원 범위 밖이거나 입력이 모호하여 로컬 공연장 데이터와 매칭하지 못했습니다."]
  else:
    confidence_notes = [
      "공식 또는 안정적인 공연장 기본 정보와 공연별 변동 가능성이 큰 정보를 분리했습니다.",
      "검색 API 미설정 상태에서는 공개 후기나 최신 공지 검색 결과를 사용하지 않습니다.",
    ]

  return {"confidence_notes": confidence_notes}
