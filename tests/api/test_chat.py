"""T1 contract checks; existing Week 3 tests are untouched."""

import re
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from assistant_api.main import create_app
from assistant_core.models import Intent, Message, Response, Source
from assistant_core.responder import StubLLMResponder


@pytest.fixture
def client(settings, service):
    return TestClient(create_app(settings, service))


@pytest.mark.parametrize(
    "message,intent,answer",
    [
        ("hi", "greeting", "Hello"),
        ("tuition for 18 credits and 2 retake", "fee", "9,450,000 VND"),
        ("where is the library", "office", "B.201"),
        ("help", "help", "I can help"),
    ],
)
def test_chat_matches_core_results(client, message, intent, answer):
    response = client.post("/v1/chat", json={"message": message})
    assert response.status_code == 200
    body = response.json()
    assert set(body) == {"answer", "intent", "sources", "degraded", "request_id"}
    assert body["intent"] == intent and answer in body["answer"]
    assert body["sources"] == [] and body["degraded"] is False
    assert re.fullmatch(r"[0-9a-f]{12}", body["request_id"])


def test_request_ids_change_for_identical_messages(client):
    first = client.post("/v1/chat", json={"message": "hi"}).json()
    second = client.post("/v1/chat", json={"message": "hi"}).json()
    assert first["request_id"] != second["request_id"]


@pytest.mark.parametrize("session_id", [None, "student-session"])
def test_typed_message_and_all_core_response_fields_are_preserved(settings, session_id):
    expected = Response(
        answer="fallback answer",
        intent=Intent.RULE,
        sources=[Source(id="rule-1", title="Example")],
        degraded=True,
    )
    injected = Mock()
    injected.handle.return_value = expected
    payload = {"message": "example question"}
    if session_id is not None:
        payload["session_id"] = session_id
    response = TestClient(create_app(settings, injected)).post("/v1/chat", json=payload)
    assert response.status_code == 200
    injected.handle.assert_called_once_with(Message(text="example question", session_id=session_id or "anonymous"))
    body = response.json()
    assert {key: body[key] for key in expected.model_dump()} == expected.model_dump(mode="json")


def test_handbook_citations_and_provider_fallback(settings, service):
    service.responder = StubLLMResponder(fail=True)
    response = TestClient(create_app(settings, service)).post(
        "/v1/chat",
        json={"message": "thesis registration credits"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "rule" and body["degraded"] is True
    assert body["sources"][0]["id"] == "H26-5.3"


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"message": ""},
        {"message": 123},
        {"message": "x" * 2001},
        {"message": "hi", "session_id": "x" * 65},
    ],
)
def test_invalid_chat_returns_422_without_calling_service(settings, payload):
    injected = Mock()
    response = TestClient(create_app(settings, injected)).post("/v1/chat", json=payload)
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "invalid_request"
    injected.handle.assert_not_called()
