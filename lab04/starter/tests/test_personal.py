"""Personal submission coverage beyond the supplied endpoint examples."""

import re
from datetime import datetime, timedelta

import pytest
from assistant_api.main import create_app
from fastapi.testclient import TestClient

from assistant_core.responder import StubLLMResponder


@pytest.mark.parametrize("message,intent", [("hi", "greeting"), ("where is the library", "office"), ("help", "help")])
def test_chat_uses_root_core(settings, service, message, intent):
    client = TestClient(create_app(settings, service))
    first = client.post("/v1/chat", json={"message": message}).json()
    second = client.post("/v1/chat", json={"message": message}).json()
    assert first["intent"] == intent
    assert re.fullmatch(r"[0-9a-f]{12}", first["request_id"])
    assert first["request_id"] != second["request_id"]


def test_rule_sources_survive_fallback(settings, service):
    service.responder = StubLLMResponder(fail=True)
    response = TestClient(create_app(settings, service)).post(
        "/v1/chat", json={"message": "thesis registration credits"}
    )
    body = response.json()
    assert body["intent"] == "rule" and body["degraded"]
    assert body["sources"][0]["id"] == "H26-5.3"


def test_feedback_isolation_and_timestamp(settings):
    settings = settings.model_copy(update={"api_admin_key": "test-placeholder"})
    first, second = TestClient(create_app(settings)), TestClient(create_app(settings))
    for rating in (-1, 0, 1):
        response = first.post("/v1/feedback", json={"request_id": "example", "rating": rating})
        assert response.status_code == 201
        assert response.json()["id"] == rating + 2
        timestamp = datetime.fromisoformat(response.json()["created_at"].replace("Z", "+00:00"))
        assert timestamp.utcoffset() == timedelta(0)
    headers = {"X-API-Key": "test-placeholder"}
    assert len(first.get("/v1/feedback", headers=headers).json()) == 3
    assert second.get("/v1/feedback", headers=headers).json() == []


@pytest.mark.parametrize("body", [{"message": 123}, {"message": "x" * 2001}])
def test_chat_invalid_types_and_length(body):
    response = TestClient(create_app()).post("/v1/chat", json=body)
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "invalid_request"


@pytest.mark.parametrize(
    "body",
    [
        {"request_id": "", "rating": 1},
        {"request_id": "id", "rating": -2},
        {"request_id": "id", "rating": 1, "comment": "x" * 501},
    ],
)
def test_feedback_boundaries(body):
    response = TestClient(create_app()).post("/v1/feedback", json=body)
    assert response.status_code == 422


def test_offices_status():
    assert TestClient(create_app()).get("/v1/offices").status_code == 200


def test_offices_contains_library_and_is_sorted():
    offices = TestClient(create_app()).get("/v1/offices").json()
    names = [office["name"] for office in offices]
    assert "Library" in names
    assert names == sorted(names)
    assert all(set(office) == {"name", "room", "hours"} for office in offices)
