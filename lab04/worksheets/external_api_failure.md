# External service failure worksheet — Open-Meteo

Base URL: https://api.open-meteo.com/v1/forecast

| Failure | Simulation | API behavior | User experience |
|---|---|---|---|
| Timeout | MockTransport raises ConnectTimeout | retry once; stale cache or 503 | marked old data or retry later |
| HTTP 500 | MockTransport returns 500 | retry once; stale cache or 503 | same |
| Malformed payload | MockTransport returns {} | retry once; stale cache or 503 | same |
| HTTP 429 | MockTransport returns 429 | retry once; stale cache or 503 | same |

Timeout: 3 seconds per HTTP operation; one retry limits upstream load. Cache TTL: 600 seconds.
The supplied WeatherClient is unchanged. Tests: test_weather_ok,
test_weather_down_returns_503 and test_weather_stale_cache_when_upstream_fails.
Network access is unnecessary for automated tests. Live weather failure is a valid 503.
