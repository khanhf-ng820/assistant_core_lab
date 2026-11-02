"""T4 — GET /v1/weather: external success, clean 503 and stale-cache fallback.

Assertions are preserved from public_materials/lab04/starter/tests/test_api.py; only the
imports and fixtures are adapted to the root integration.
"""

import httpx
from fastapi.testclient import TestClient

from assistant_api.main import create_app
from assistant_api.weather import WeatherClient

OK_JSON = {"current": {"time": "2026-10-05T09:00", "temperature_2m": 31.2, "weather_code": 3, "wind_speed_10m": 8.5}}


def weather_with(handler, **kwargs) -> WeatherClient:
    transport = httpx.MockTransport(handler)
    return WeatherClient("https://example.test/forecast", 10.76, 106.68, retries=1, transport=transport, **kwargs)


def test_weather_ok(settings, service):
    app = create_app(settings, service, weather_with(lambda req: httpx.Response(200, json=OK_JSON)))
    response = TestClient(app).get("/v1/weather")
    assert response.status_code == 200
    body = response.json()
    assert body["description"] == "overcast"
    assert body["temperature_c"] == 31.2
    assert body["wind_kmh"] == 8.5
    assert body["observed_at"] == "2026-10-05T09:00"
    assert body["stale"] is False


def test_weather_down_returns_503(settings, service):
    def boom(req):
        raise httpx.ConnectTimeout("timeout", request=req)

    app = create_app(settings, service, weather_with(boom))
    response = TestClient(app).get("/v1/weather")
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "weather_service_unavailable"


def test_weather_upstream_error_without_cache_returns_503(settings, service):
    app = create_app(settings, service, weather_with(lambda req: httpx.Response(500)))
    response = TestClient(app).get("/v1/weather")
    assert response.status_code == 503
    assert response.json()["error"] == {
        "code": "weather_service_unavailable",
        "message": "Weather service unavailable",
    }


def test_weather_serves_stale_cache_after_upstream_failure(settings, service):
    calls = {"n": 0}

    def flaky(req):
        calls["n"] += 1
        return httpx.Response(200, json=OK_JSON) if calls["n"] == 1 else httpx.Response(500)

    client = TestClient(create_app(settings, service, weather_with(flaky, cache_ttl_s=0)))
    assert client.get("/v1/weather").json()["stale"] is False
    second = client.get("/v1/weather")
    assert second.status_code == 200
    assert second.json()["stale"] is True


def test_weather_stale_cache_when_upstream_fails():
    calls = {"n": 0}

    def flaky(req):
        calls["n"] += 1
        if calls["n"] == 1:
            return httpx.Response(200, json=OK_JSON)
        return httpx.Response(500)

    weather = weather_with(flaky)
    weather.cache_ttl_s = 0  # force a refresh on the second call
    assert not weather.current().stale
    assert weather.current().stale
