"""Mandatory Part F; test_rate_limit preserves the official starter assertions.

Source: CSC10014-at-fit-hcmus/public_materials, lab04/starter/tests/test_api.py.
Only the fixture is adapted to the root API and the obsolete bonus skip is removed.
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import Mock

import httpx
import pytest
from fastapi.testclient import TestClient

from assistant_api.main import create_app
from assistant_api.ratelimit import RateLimiter
from assistant_core.models import Intent, Response


@pytest.fixture
def client(settings, service):
    limited_settings = settings.model_copy(update={"rate_limit_per_min": 5})
    return TestClient(create_app(limited_settings, service))


def test_rate_limit(client):
    codes = [client.post("/v1/chat", json={"message": "hi"}).status_code for _ in range(6)]
    assert codes[-1] == 429


def test_rejected_request_does_not_call_core(settings):
    injected = Mock()
    injected.handle.return_value = Response(answer="Hello", intent=Intent.GREETING)
    app = create_app(settings.model_copy(update={"rate_limit_per_min": 5}), injected)
    client = TestClient(app)
    assert [client.post("/v1/chat", json={"message": "hi"}).status_code for _ in range(5)] == [200] * 5
    rejected = client.post("/v1/chat", json={"message": "hi"})
    assert rejected.status_code == 429
    assert rejected.json() == {"error": {"code": "too_many_requests", "message": "Too many requests"}}
    assert injected.handle.call_count == 5
    assert client.get("/health").status_code == 200


def test_client_ips_have_independent_limits_and_forwarded_headers_cannot_reset_it(settings, service):
    app = create_app(settings.model_copy(update={"rate_limit_per_min": 1}), service)

    async def exercise():
        for ip in ["192.0.2.1", "192.0.2.2"]:
            transport = httpx.ASGITransport(app=app, client=(ip, 12345))
            async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
                assert (await client.post("/v1/chat", json={"message": "hi"})).status_code == 200
                response = await client.post(
                    "/v1/chat", json={"message": "hi"}, headers={"X-Forwarded-For": "203.0.113.1"}
                )
                assert response.status_code == 429

    asyncio.run(exercise())


def test_missing_client_uses_unknown_key(settings, service):
    app = create_app(settings.model_copy(update={"rate_limit_per_min": 1}), service)

    async def exercise():
        transport = httpx.ASGITransport(app=app, client=None)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            assert (await client.post("/v1/chat", json={"message": "hi"})).status_code == 200
            assert (await client.post("/v1/chat", json={"message": "hi"})).status_code == 429

    asyncio.run(exercise())


def test_quota_recovers_after_sliding_window(client, monkeypatch):
    clock = [100.0]
    monkeypatch.setattr("assistant_api.ratelimit.time.monotonic", lambda: clock[0])
    for _ in range(5):
        assert client.post("/v1/chat", json={"message": "hi"}).status_code == 200
    clock[0] += 59
    assert client.post("/v1/chat", json={"message": "hi"}).status_code == 429
    clock[0] += 2
    assert client.post("/v1/chat", json={"message": "hi"}).status_code == 200


def test_new_app_has_fresh_quota(settings, service):
    limited_settings = settings.model_copy(update={"rate_limit_per_min": 1})
    first = TestClient(create_app(limited_settings, service))
    assert first.post("/v1/chat", json={"message": "hi"}).status_code == 200
    assert first.post("/v1/chat", json={"message": "hi"}).status_code == 429
    second = TestClient(create_app(limited_settings, service))
    assert second.post("/v1/chat", json={"message": "hi"}).status_code == 200


def test_concurrent_calls_share_one_quota(monkeypatch):
    monkeypatch.setattr("assistant_api.ratelimit.time.monotonic", lambda: 100.0)
    limiter = RateLimiter(5)
    with ThreadPoolExecutor(max_workers=16) as pool:
        accepted = list(pool.map(limiter.allow, ["client"] * 100))
    assert sum(accepted) == 5
