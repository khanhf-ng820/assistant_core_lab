# Personal Lab 4 verification

Captured 1 November 2026 using the actual Uvicorn app and Swagger UI.

- [Successful Swagger chat](swagger-chat.png): HTTP 200, tuition 9,450,000 VND, response fields and request ID.
- [Live curl script output](curl-results.txt): expected success, validation, auth and routing statuses; live weather returned 200.
- Core: 167 passed, 4 existing optional benchmark skips.
- Practice: 5 passed.
- Starter/API: 43 passed, 1 optional rate-limit bonus skip.
- Root and explicit Lab 4 Ruff lint/format checks passed.
- Local Python: 3.13.5; CI additionally checks Python 3.10/3.12.

The demo uses a non-production placeholder admin key. No real credentials are stored.
H2 still requires the author's own five-line reflection; see ../h2-reflection-prompt.md.
