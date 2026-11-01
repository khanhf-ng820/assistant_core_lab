# Lab 4 API contract

| Method | Path | Request | Success | Errors | Caller |
|---|---|---|---|---|---|
| GET | /health | none | 200 {status, version} | startup fails if data/config invalid | ops |
| POST | /v1/chat | message: 1–2000 chars; session_id: default anonymous, max 64 | 200 {answer,intent,sources,degraded,request_id} | 422 invalid_request | student |
| POST | /v1/feedback | request_id: 1–64 chars; rating: -1/0/1; optional comment: max 500 | 201 with id and UTC created_at | 422 invalid_request | student |
| GET | /v1/feedback | X-API-Key matching API_ADMIN_KEY | 200 feedback list | 401 missing_or_invalid_api_key | staff |
| GET | /v1/weather | none | 200 {temperature_c,wind_kmh,description,observed_at,stale} | 503 weather_service_unavailable | student |

Errors use {"error":{"code":"...","message":"..."}}; unknown routes return 404 not_found.
Clients should display validation messages, request admin access for 401, and allow retry for 503.
Changing required fields, field types, or response meanings incompatibly would require /v2.
GET /v1/offices is public: 200 list of {name,room,hours}, sorted by name.
Rate limiting remains an optional bonus and is not enabled.
