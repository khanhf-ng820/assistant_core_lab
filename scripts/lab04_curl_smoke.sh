#!/usr/bin/env bash
# Lab 4 root API smoke tests for the five implemented endpoints.
#
# Start the server first:
#   API_ADMIN_KEY=test-placeholder .venv/bin/uvicorn assistant_api.main:create_app --factory --port 8010
#
# Then run:
#   API_ADMIN_KEY=test-placeholder BASE=http://127.0.0.1:8010 bash scripts/lab04_curl_smoke.sh
#
# T2 POST /v1/feedback is intentionally omitted until the root handler lands.
set -u

BASE="${BASE:-http://127.0.0.1:8000}"
ADMIN="${API_ADMIN_KEY:-test-placeholder}"

hr() { printf '\n== %s\n' "$1"; }

hr "health (expect 200)"
curl -sS -w '  [%{http_code}]\n' "$BASE/health"

hr "chat fee (expect 200)"
curl -sS -w '  [%{http_code}]\n' -X POST "$BASE/v1/chat" \
  -H 'Content-Type: application/json' \
  -d '{"message":"tuition for 18 credits and 2 retake","session_id":"curl-smoke"}'

hr "chat invalid empty message (expect 422)"
curl -sS -w '  [%{http_code}]\n' -X POST "$BASE/v1/chat" \
  -H 'Content-Type: application/json' -d '{"message":""}'

hr "admin feedback without key (expect 401)"
curl -sS -w '  [%{http_code}]\n' "$BASE/v1/feedback"

hr "admin feedback with key (expect 200)"
curl -sS -w '  [%{http_code}]\n' -H "X-API-Key: $ADMIN" "$BASE/v1/feedback"

hr "weather (expect 200, or 503 if upstream is down)"
curl -sS -m 10 -w '  [%{http_code}]\n' "$BASE/v1/weather"

hr "offices (expect 200, Library present)"
curl -sS -w '  [%{http_code}]\n' "$BASE/v1/offices"

hr "unknown route (expect 404)"
curl -sS -w '  [%{http_code}]\n' "$BASE/v1/nope"

printf '\nT2 POST /v1/feedback omitted: root handler still TODO (owner: Lý Tuấn Kiệt).\n'
