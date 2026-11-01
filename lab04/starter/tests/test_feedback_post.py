"""Unit and API tests for POST /v1/feedback endpoint (Task T2).

Verifies payload validation, auto-incrementing ID generation, UTC timestamping,
and in-memory storage behavior.
"""

from __future__ import annotations

import httpx
import pytest
from fastapi.testclient import TestClient

from assistant_api.main import create_app
from assistant_api.weather import WeatherClient

OK_WEATHER = {
    "current": {
        "time": "2026-10-05T09:00",
        "temperature_2m": 31.2,
        "weather_code": 3,
        "wind_speed_10m": 8.5,
    }
}


def _dummy_weather() -> WeatherClient:
    transport = httpx.MockTransport(lambda req: httpx.Response(200, json=OK_WEATHER))
    return WeatherClient("https://example.test/forecast", 10.76, 106.68, retries=1, transport=transport)


@pytest.fixture
def feedback_client(settings, service):
    """Fixture providing a fresh TestClient instance with an isolated in-memory feedback store."""
    app = create_app(settings, service, _dummy_weather())
    return TestClient(app)


def test_post_feedback_success_minimal(feedback_client):
    """POST /v1/feedback should succeed with valid request_id and rating, omitting comment."""
    payload = {"request_id": "req-101", "rating": 1}
    response = feedback_client.post("/v1/feedback", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["request_id"] == "req-101"
    assert data["rating"] == 1
    assert data["comment"] is None
    assert "created_at" in data


def test_post_feedback_success_with_comment(feedback_client):
    """POST /v1/feedback should succeed with optional user comment."""
    payload = {
        "request_id": "req-102",
        "rating": -1,
        "comment": "The response was slightly inaccurate regarding office hours.",
    }
    response = feedback_client.post("/v1/feedback", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["request_id"] == "req-102"
    assert data["rating"] == -1
    assert data["comment"] == "The response was slightly inaccurate regarding office hours."


def test_post_feedback_id_auto_increment(feedback_client):
    """Successive feedback submissions should assign auto-incrementing integer IDs."""
    ratings = [-1, 0, 1]
    for expected_id, rating in enumerate(ratings, start=1):
        payload = {"request_id": f"req-{expected_id}", "rating": rating}
        res = feedback_client.post("/v1/feedback", json=payload)
        assert res.status_code == 201
        assert res.json()["id"] == expected_id

    # Verify that in-memory store preserves all submissions
    assert len(feedback_client.app.state.feedback_store) == len(ratings)


@pytest.mark.parametrize("valid_rating", [-1, 0, 1])
def test_post_feedback_valid_ratings(feedback_client, valid_rating):
    """Endpoint should accept boundary rating values: -1 (down), 0 (neutral), 1 (up)."""
    payload = {"request_id": f"req-rating-{valid_rating}", "rating": valid_rating}
    response = feedback_client.post("/v1/feedback", json=payload)
    assert response.status_code == 201
    assert response.json()["rating"] == valid_rating


@pytest.mark.parametrize("invalid_rating", [-5, -2, 2, 5, 10])
def test_post_feedback_invalid_rating_range(feedback_client, invalid_rating):
    """Endpoint should reject ratings outside [-1, 1] with HTTP 422."""
    payload = {"request_id": "req-bad-rating", "rating": invalid_rating}
    response = feedback_client.post("/v1/feedback", json=payload)

    assert response.status_code == 422
    data = response.json()
    assert data["error"]["code"] == "invalid_request"
    assert "rating" in data["error"]["message"]


def test_post_feedback_missing_required_fields(feedback_client):
    """Endpoint should return 422 when required fields are missing."""
    # Missing rating
    res1 = feedback_client.post("/v1/feedback", json={"request_id": "req-missing-rating"})
    assert res1.status_code == 422
    assert res1.json()["error"]["code"] == "invalid_request"

    # Missing request_id
    res2 = feedback_client.post("/v1/feedback", json={"rating": 1})
    assert res2.status_code == 422
    assert res2.json()["error"]["code"] == "invalid_request"


def test_post_feedback_empty_request_id(feedback_client):
    """Endpoint should reject empty request_id with HTTP 422."""
    payload = {"request_id": "", "rating": 1}
    response = feedback_client.post("/v1/feedback", json=payload)

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "invalid_request"


def test_post_feedback_request_id_too_long(feedback_client):
    """Endpoint should reject request_id longer than 64 characters with HTTP 422."""
    payload = {"request_id": "x" * 65, "rating": 1}
    response = feedback_client.post("/v1/feedback", json=payload)

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "invalid_request"


def test_post_feedback_comment_too_long(feedback_client):
    """Endpoint should reject comment longer than 500 characters with HTTP 422."""
    payload = {
        "request_id": "req-comment-too-long",
        "rating": 1,
        "comment": "a" * 501,
    }
    response = feedback_client.post("/v1/feedback", json=payload)

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "invalid_request"
    assert "comment" in response.json()["error"]["message"]

