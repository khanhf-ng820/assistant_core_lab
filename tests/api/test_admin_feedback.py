"""T3 checks for the root API; T2 owns POST/GET roundtrip integration."""

from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from assistant_api.main import create_app
from assistant_api.schemas import FeedbackOut

ADMIN_KEY = "test-only-admin"


@pytest.fixture
def admin_app(settings, service):
    return create_app(settings.model_copy(update={"api_admin_key": ADMIN_KEY}), service)


def test_valid_key_returns_empty_list(admin_app):
    response = TestClient(admin_app).get("/v1/feedback", headers={"X-API-Key": ADMIN_KEY})
    assert response.status_code == 200
    assert response.json() == []


def test_valid_key_lists_shared_store_in_order(admin_app):
    items = [
        FeedbackOut(
            id=index,
            request_id=f"request-{index}",
            rating=rating,
            comment=comment,
            created_at=datetime(2026, 11, 1, tzinfo=timezone.utc),
        )
        for index, rating, comment in [(1, -1, "Please check this"), (2, 1, None)]
    ]
    # Seed the same per-app store used by T2; do not replace its unfinished POST handler.
    admin_app.state.feedback_store.extend(items)
    response = TestClient(admin_app).get("/v1/feedback", headers={"X-API-Key": ADMIN_KEY})
    assert response.status_code == 200
    assert response.json() == [item.model_dump(mode="json") for item in items]


@pytest.mark.parametrize("key", [None, "", "incorrect", "test-only-admi"])
def test_missing_or_wrong_key_denies_access_without_disclosure(admin_app, key, caplog):
    headers = {} if key is None else {"X-API-Key": key}
    response = TestClient(admin_app).get("/v1/feedback", headers=headers)
    assert response.status_code == 401
    assert response.json() == {"error": {"code": "missing_or_invalid_api_key", "message": "Missing or invalid API key"}}
    assert ADMIN_KEY not in response.text + caplog.text
    if key:
        assert key not in response.text + caplog.text


@pytest.mark.parametrize("configured", [None, ""])
def test_unconfigured_key_fails_closed(settings, service, configured):
    app = create_app(settings.model_copy(update={"api_admin_key": configured}), service)
    response = TestClient(app).get("/v1/feedback", headers={"X-API-Key": ADMIN_KEY})
    assert response.status_code == 401


def test_feedback_store_is_not_shared_between_apps(settings, service, admin_app):
    admin_app.state.feedback_store.append(
        FeedbackOut(id=1, request_id="r", rating=1, created_at=datetime.now(timezone.utc))
    )
    fresh_app = create_app(settings.model_copy(update={"api_admin_key": ADMIN_KEY}), service)
    response = TestClient(fresh_app).get("/v1/feedback", headers={"X-API-Key": ADMIN_KEY})
    assert response.status_code == 200 and response.json() == []


def test_admin_header_and_unauthorized_response_are_documented(admin_app):
    operation = admin_app.openapi()["paths"]["/v1/feedback"]["get"]
    assert any(p["in"] == "header" and p["name"] == "x-api-key" for p in operation["parameters"])
    assert "401" in operation["responses"]
    assert ADMIN_KEY not in str(operation)
