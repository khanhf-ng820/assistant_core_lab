
# Lab 4 — Part E: QA/QC Report

**Student:** Nguyen Minh Khang  
**Student ID:** 25125018  
**GitHub:** @KaKaAkagami  
**Role:** Part E — QA/QC  
**Date:** 2026-11-01

## 1. Scope

This report documents the initial QA/QC results for the Lab 4 REST API project.

Repository: https://github.com/khanhf-ng820/assistant_core_lab

The initial API checks were performed against the team foundation and T1 Chat API at commit `f2ea073`, before final integration of all team features.

## 2. Automated Testing

### Warm-up P1–P5

Command:

```bash
python -m pytest -q lab04/practice/test_hello_api.py
```

Result: **5 passed**

Ruff: **All checks passed**

### T1 Chat API and Foundation

Command:

```bash
python -m pytest -q tests/api/test_chat.py tests/api/test_api_foundation.py
```

Result: **26 passed**

### Full Regression Suite

Command:

```bash
python -m pytest -q
```

Result:

- 193 passed
- 4 skipped
- 0 failed
- 1 deprecation warning

The four skipped tests were already present in the existing test suite.

### Static Analysis

Command:

```bash
python -m ruff check .
```

Result: **All checks passed**

## 3. Manual API Testing

Base URL: `http://127.0.0.1:8000`

| Method | Endpoint | Test Case | Expected | Actual | Result |
|---|---|---|---|---|---|
| GET | `/health` | Health check | 200 | 200 | PASS |
| POST | `/v1/chat` | Valid tuition question | 200 | 200 | PASS |
| POST | `/v1/chat` | Empty message | 422 | 422 | PASS |
| GET | `/v1/feedback` | Missing API key | 401 | 401 | PASS |

### Chat API Response

Request:

```json
{
  "message": "tuition for 18 credits and 2 retake",
  "session_id": "qa-khang"
}
```

Observed response:

```json
{
  "answer": "Your tuition is 9,450,000 VND.",
  "intent": "fee",
  "sources": [],
  "degraded": false,
  "request_id": "0c6439b4e4ab"
}
```

HTTP status: **200 OK**

### Invalid Chat Request

Request:

```json
{
  "message": ""
}
```

Observed response:

```json
{
  "error": {
    "code": "invalid_request",
    "message": "message: String should have at least 1 character"
  }
}
```

HTTP status: **422**

### Unauthorized Admin Request

Endpoint: `GET /v1/feedback`

Observed response:

```json
{
  "error": {
    "code": "missing_or_invalid_api_key",
    "message": "Missing or invalid API key"
  }
}
```

HTTP status: **401 Unauthorized**

### Health Check

Observed response:

```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

HTTP status: **200 OK**

## 4. Swagger UI Verification

Swagger UI URL: `http://127.0.0.1:8000/docs`

Verified:

- OpenAPI documentation loads successfully.
- POST `/v1/chat` accepts a valid JSON request.
- The response has HTTP status 200.
- The response includes `answer`, `intent`, `sources`, `degraded`, and `request_id`.

A screenshot of the successful chat request was captured during manual testing.

### Swagger Evidence

![Successful POST /v1/chat - HTTP 200](screenshots/swagger_chat_200.jpg)

The screenshot shows a successful POST /v1/chat request with HTTP 200 and the expected tuition response.

## 5. Cross-Review

Reviewed PR #21 — T1 Chat API.

URL: https://github.com/khanhf-ng820/assistant_core_lab/pull/21

Review status: **Approved**

The implementation and tests were checked for:

- Correct integration with `service.handle()`.
- Proper message and session ID propagation.
- Unique 12-character request IDs.
- Correct response schema.
- Input validation and HTTP 422.
- Preservation of Lab 3 behavior.

CI passed on Python 3.10 and 3.12.

## 6. Pending Integration Checks

The following requirements must be validated against the final integrated API:

| Feature | Required Check | Status |
|---|---|---|
| T2 Feedback POST | HTTP 201, sequential ID, UTC timestamp | PENDING |
| T3 Admin Feedback | Authorized access with valid key | PENDING |
| Part F Rate Limiting | HTTP 429 after exceeding request limit | PENDING |
| T4 Weather API | HTTP 200, fallback, HTTP 503 | PENDING |
| H1 Offices API | HTTP 200, Library present, sorted offices | PENDING |
| Full Team Integration | Complete test suite and CI | PENDING |

The current PASS results apply to commit `f2ea073` only. They do not establish that the final integrated Lab 4 application passes all required checks.

## 7. Conclusion

The API foundation and T1 Chat API passed the initial automated and manual QA/QC checks.

No failures were observed in the tested T1 branch. Final acceptance remains pending until all team endpoints and mandatory rate limiting are integrated and tested.
