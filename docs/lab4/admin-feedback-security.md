# Lab 4 T3 and mandatory Part F

Owner: Tran Phuc Khanh (25125020). Issue #32. Review: @Dang-Xuan-Phat.

## Admin feedback

GET /v1/feedback reads the per-app feedback_store shared with T2. Send the
X-API-Key header matching API_ADMIN_KEY. Missing, wrong, empty, or unconfigured
keys return 401 with the same generic error; no supplied/configured key is echoed.
Comparison uses hmac.compare_digest. Keep real keys in the ignored local .env,
never in commits, screenshots, curl transcripts, or PR descriptions. Use HTTPS
when deployed; this lab's in-memory feedback is not persistent storage.

The root POST /v1/feedback is still T2's TODO at base df1d11d. Its merged starter
implementation has not been ported into the active root API. T3 tests therefore
seed the shared store directly. This checks listing and authorization, but does
not establish a passing POST/GET roundtrip. T2 and the integration owner must use
this same store and run the official roundtrip before final acceptance.

## Chat rate limiting

RATE_LIMIT_PER_MIN defaults to 30. A valid chat consumes one slot for its
request.client.host (or "unknown") before service.handle runs. Exhaustion returns
429 with {"error":{"code":"too_many_requests","message":"Too many requests"}}.
Other endpoints remain available. The provided sliding 60-second window is
retained, with a lock around quota checks/updates for concurrent sync handlers.

Client-supplied X-Forwarded-For does not bypass the quota. Configure trusted
proxy handling at deployment if needed. Limits and feedback are per application
process: restart resets them, and multiple workers do not share limits. This
matches the starter's in-memory lab contract.

## Checks and official materials

The active test_rate_limit assertion body is taken unchanged from:
https://github.com/CSC10014-at-fit-hcmus/public_materials/blob/main/lab04/starter/tests/test_api.py
(blob 1ceb1a1e6c10a58f3e742161eabde8b02d1bbd4c). The fixture uses the root
API factory and limit 5; the starter bonus skip is removed because LMS requires F.

Added tests cover missing/wrong/empty/unconfigured admin keys, ordered feedback
serialization, app isolation, 401/429 envelopes, no core call after exhaustion,
separate client IPs, missing client fallback, window recovery, and concurrent
quota use. Existing Week 3 tests are unchanged; check with:

```text
python scripts/check_week3_tests.py
python -m pytest -q
python -m ruff check .
python -m ruff format --check .
```

For Part E, run with a test-only local admin key and RATE_LIMIT_PER_MIN=5.
Verify GET /v1/feedback without a key returns 401 and with the configured key
returns 200. Six chat requests from one client must yield five 200s then 429.
After T2 integration, run the unmodified official feedback_roundtrip assertions
against the root API. H1 and final curl/Swagger evidence remain their owners' work.
