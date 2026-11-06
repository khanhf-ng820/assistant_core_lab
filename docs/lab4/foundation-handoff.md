# Lab 4 team foundation handoff

The LMS homework screenshot governs scope: six HTTP operations (D.2 + H1),
mandatory Part F rate limiting, unchanged Week 3 tests, and submission on the Week 3 repo.
PDF sections D.2/E/F/H1 supply the contract and testing examples.
Official source: https://github.com/CSC10014-at-fit-hcmus/public_materials/tree/main/lab04

## Current status (2026-11-06)

| Item | Status |
|---|---|
| T1 `POST /v1/chat` | Implemented and tested |
| T2 `POST /v1/feedback` | **Not implemented** in the root API; valid requests return 500. Owner: Lý Tuấn Kiệt. |
| T3 `GET /v1/feedback` | Implemented and tested |
| T4 `GET /v1/weather` | Implemented and tested |
| H1 `GET /v1/offices` | Implemented and tested |
| Part F rate limiting | Implemented and tested (429 envelope) |
| `v0.4-api` tag | **Pending** T2 and final evidence |
| `lab04/starter` | Reference/practice only; its T1/T3/T4 tests are not green |

## Starting point

Install only the root project. src/assistant_api is the active API; lab04 is reference/practice.
APISettings extends core Settings. create_app(settings=None, service=None, weather=None)
accepts injected components for offline tests and defaults to AssistantService.default().
Message comes from assistant_core.models; the root package has no build_service().

Each factory call owns one feedback_store (also app.state.feedback_store) and
app.state.rate_limiter configured by RATE_LIMIT_PER_MIN (default 30).
POST and GET feedback must use that same list. Never create a global store or limiter.
The chat owner and security owner add the rate check before service.handle(), using
request.client.host (or "unknown") as the client key. Exhaustion returns HTTP 429 with
error.code="too_many_requests". Enforcement is implemented in chat() before service.handle() (PR #33).
The supplied limiter uses a sliding 60-second window; independent app instances reset it.

## Ownership and acceptance

The latest user-provided assignment supersedes the earlier role split. Nguyễn Minh Khang
(@KaKaAkagami) reviews T1. Only T1 implementation/tests are added after this clarification;
other owners retain their endpoint and QA work. Rate limiting is mandatory under the LMS
homework even though the role table calls it a bonus.


| Owner | Operation | Required checks |
|---|---|---|
| Nguyễn Phúc Khánh | T1 POST /v1/chat, PR coordination, integration/tag | 200 response fields + fresh 12-char ID; tuition 9,450,000 VND; invalid input 422 |
| Lý Tuấn Kiệt | POST /v1/feedback | 201; sequential ID and UTC timestamp; rating outside -1/0/1 rejected |
| Trần Phúc Khánh | GET /v1/feedback + Part F | correct key 200; missing/wrong key 401; sixth chat at limit 5 returns 429 |
| Trần Thành Lợi | T4 GET /v1/weather | fake HTTP 200; failure/no cache 503; stale cache fallback |
| Nguyễn Minh Khang | Part E QA/QC | integrated tests, curl, Swagger screenshot and demo |
| Đặng Xuân Phát | GET /v1/offices + practice QA | 200; Library present; name/room/hours sorted by name; two H1 tests; Swagger clarity |

Endpoint stubs and owner labels are in main.py. Limit edits to your route; coordinate
T1/Part F and T2/T3 before merging. Rebase on the reviewed foundation; merge sequentially.
API schemas retain the official starter contracts. HTTP errors share
{"error":{"code":"...","message":"..."}}, including 401/422/429/503 and routing errors.

For H1, AssistantService.default() currently creates the OfficeDirectory from
assistant_core.service, not the separate class in assistant_core.knowledge.
Add all() to the actual runtime class and test the default factory. Do not rewrite core
behavior or consolidate those classes as part of this foundation.

## Tests and completion

All original tests (including tests/conftest.py) at baseline d4b55f5 must retain their
contents and paths. scripts/check_week3_tests.py enforces this and permits new files.
Add Week 4 fixtures/tests under tests/api/; fixtures there do not alter Week 3 tests.
Preserve the assertions from public_materials/lab04/starter/tests/test_api.py when
adapting each feature's tests. Adjust imports/fixtures for root integration, not assertions.
Do not import tests of unfinished routes merely to skip them. Activate the Week 4
rate-limit test when the feature lands: its starter "bonus" skip is not valid here.
The existing four optional Week 3 benchmark skips remain unchanged.

CI runs the full root test suite, including the Week 4 API tests for T1, T3, T4, H1
and rate limiting. T2 has no success-path test yet because the root handler is still
TODO. Final team acceptance requires all six operations plus active 429 tests, H1 tests,
offline weather tests, full CI, curl evidence and a successful Swagger chat screenshot.
P1-P5 practice and H2 (five lines in each author's own words) remain PDF companion work.
A second external API does not replace mandatory rate limiting.

## PR and release sequence

Root integration and T1 PR #21 closes #24 and requests @KaKaAkagami review.
The obsolete personal candidate #22 / #23 is superseded; its branch is reference only.
No separate full personal API PR is required by this team plan.
Disclose AI use in each PR and docs/ai-use-log.md. Teammates add their feature PRs and
new tests; the leader checks the final merged main, then tags v0.4-api after approval.
The tag is not created yet: it is blocked on T2. Re-run the evidence checks after T2
lands, then tag the final merged main.
Confirm the actual Lab 5/LMS deadline instead of inventing a calendar date.
