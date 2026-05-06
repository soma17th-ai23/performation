from fastapi.testclient import TestClient

from performation_backend.main import app


client = TestClient(app)


def test_health_check() -> None:
  response = client.get("/health")

  assert response.status_code == 200
  assert response.json() == {"status": "ok"}


def test_create_guide_uses_agent_workflow() -> None:
  response = client.post("/guides", json={"query": "예스24라이브홀 스탠딩"})

  assert response.status_code == 200
  payload = response.json()
  assert payload["input_type"] == "venue_with_detail_question"
  assert payload["venue"]["name"] == "YES24 Live Hall"
  assert payload["event_info"] is None
  assert payload["event_candidates"] == []
  assert payload["fallback_used"] is True
