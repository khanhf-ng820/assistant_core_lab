# Study Assistant — backend (Lab 5 reference)

## Setup
> **Python version:** Python 3.10+ is supported. On Python 3.14, `requirements.txt`
> selects `pydantic 2.12.5` and `SQLModel 0.0.48`; Python 3.10–3.13 keeps the
> original `pydantic 2.9.2` / `SQLModel 0.0.22` pins. If `.venv` already exists from
> a different interpreter, remove it first (`rm -rf .venv`) so the environment is clean.

```
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt && pip install -e .
cp .env.example .env
```
## Run the API
```
uvicorn assistant_api.main:create_app --factory --reload
```
Open http://127.0.0.1:8000/docs for the interactive OpenAPI documentation.

## API contract (v1)
| Method | Path | Body | Success | Errors |
|---|---|---|---|---|
| GET | `/health` | — | 200 `{"status":"ok","version":...}` | — |
| POST | `/v1/chat` | `{"message": str 1–2000, "session_id": str}` | 200 `{answer, intent, sources[], degraded, request_id}` | 422 invalid, 429 rate limit |
| POST | `/v1/feedback` | `{"request_id": str, "rating": -1/0/1, "comment"?: str ≤500}` | 201 feedback with `id`, `created_at` | 422 |
| GET | `/v1/feedback` | header `X-API-Key` | 200 list | 401 |
| GET | `/v1/stats/intents` | header `X-API-Key` | 200 `[{intent, requests, avg_latency_ms, unresolved}]` | 401 |
| GET | `/v1/weather` | — | 200 `{temperature_c, wind_kmh, description, observed_at, stale}` | 503 upstream down |

All errors use one shape: `{"error": {"code": "...", "message": "..."}}`.

## Database (Lab 5)
```
python scripts/migrate.py assistant.db      # apply sql/migrations in order
python scripts/seed.py assistant.db 300     # synthetic data only
sqlite3 assistant.db < sql/queries.sql      # the five queries + product questions
```
New endpoint: `GET /v1/stats/intents` (header `X-API-Key`). `POST /v1/feedback` now returns 404 for an unknown `request_id`.

## Tests
```
pytest -q                          # unit + API tests (external API mocked)
bash api-tests/curl_tests.sh       # manual tests against a running server
```
Postman / Bruno: import `api-tests/study-assistant.postman_collection.json`.
