"""H1 - GET /v1/offices: campus office directory listing."""

import pytest
from fastapi.testclient import TestClient

from assistant_api.main import create_app


@pytest.fixture
def client(settings, service):
    return TestClient(create_app(settings, service))


def test_offices_status_ok(client):
    response = client.get("/v1/offices")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_offices_sorted_and_contains_library(client):
    response = client.get("/v1/offices")
    assert response.status_code == 200
    offices = response.json()
    assert len(offices) == 4
    names = [office["name"] for office in offices]
    assert names == ["IT Helpdesk", "Library", "Student Affairs", "Training Office"]
    assert all({"name", "room", "hours"}.issubset(office.keys()) for office in offices)


def test_offices_openapi_schema(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    endpoint_doc = response.json()["paths"]["/v1/offices"]["get"]
    assert endpoint_doc["tags"] == ["offices"]
    assert endpoint_doc["summary"] == "List campus offices"
    assert "alphabetically" in endpoint_doc["description"]
