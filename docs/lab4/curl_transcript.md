# Lab 4 root API — curl smoke transcript

- **Date:** 2026-11-06
- **Commit:** `f1cc905`
- **Server:** `API_ADMIN_KEY=test-placeholder .venv/bin/uvicorn assistant_api.main:create_app --factory --port 8010`
- **Command:** `API_ADMIN_KEY=test-placeholder BASE=http://127.0.0.1:8010 bash scripts/lab04_curl_smoke.sh`

The script covers the five working root endpoints. T2 `POST /v1/feedback` is
intentionally omitted because its root handler is still a TODO owned by Lý Tuấn Kiệt.

```text
== health (expect 200)
{"status":"ok","version":"1.0.0"}  [200]

== chat fee (expect 200)
{"answer":"Your tuition is 9,450,000 VND.","intent":"fee","sources":[],"degraded":false,"request_id":"4b7c6ab7adfc"}  [200]

== chat invalid empty message (expect 422)
{"error":{"code":"invalid_request","message":"message: String should have at least 1 character"}}  [422]

== admin feedback without key (expect 401)
{"error":{"code":"missing_or_invalid_api_key","message":"Missing or invalid API key"}}  [401]

== admin feedback with key (expect 200)
[]  [200]

== weather (expect 200, or 503 if upstream is down)
{"temperature_c":28.3,"wind_kmh":4.0,"description":"clear sky","observed_at":"2026-11-06T15:00","stale":false}  [200]

== offices (expect 200, Library present)
[{"name":"IT Helpdesk","room":"E.005","hours":"Mon-Fri 08:00-17:00"},{"name":"Library","room":"B.201","hours":"Mon-Sat 07:00-20:00"},{"name":"Student Affairs","room":"I.102","hours":"Mon-Fri 08:00-16:00"},{"name":"Training Office","room":"I.101","hours":"Mon-Fri 07:30-16:30"}]  [200]

== unknown route (expect 404)
{"error":{"code":"not_found","message":"Not Found"}}  [404]

T2 POST /v1/feedback omitted: root handler still TODO (owner: Lý Tuấn Kiệt).
```
