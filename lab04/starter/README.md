# Study Assistant API — Lab 4

## Setup (from repository root)

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -r lab04/starter/requirements.txt
python -m pip install -e . -e ./lab04/starter
cp lab04/starter/.env.example lab04/starter/.env
cd lab04/starter
uvicorn assistant_api.main:create_app --factory --reload
```

Open http://127.0.0.1:8000/docs. Use a local API_ADMIN_KEY in .env; never commit it.
The process environment overrides .env. Relative ASSISTANT_DATA_DIR paths are resolved
against the repository root, including when launching from this directory.
Both packages share the root assistant_core and root data; do not copy another core here.
The API uses APISettings extending the existing root Settings without changing the CLI.

## Foundation handoff

This personal candidate completes P1-P5, T1-T4 and H1; bonus rate limiting is deferred.
CI requires the full core, practice and API suites. Feedback remains isolated per app.
The team should choose and review a shared implementation before merging this candidate.

Owners: Lợi — T1 chat; Kiệt — T2 POST feedback; Trần Phúc Khánh — T3 admin GET;
Khang — T4 weather; Phát — H1 offices; Nguyễn Phúc Khánh — foundation and integration.
Limit edits to your route and tests; rebase before sequential merges. Every member still
completes P1-P5 and T1-T4 on their own branch. Teammate approval is required before merge.

## Checks

From root: `python -m pytest -q` (core).
From lab04/starter: `python -m pytest -q tests/test_foundation.py` (foundation).
After T1-T4: `python -m pytest -q tests` (full starter; bonus remains skipped).
From lab04/practice: `python -m pytest -q test_hello_api.py` (five warm-ups).
Run each suite separately to avoid duplicate test module names.

Use the starter pyproject explicitly for Lab 4 Ruff checks: root discovery intentionally
excludes unfinished teaching projects. See CI for exact commands.
After endpoints work, run `bash api-tests/curl_tests.sh` against the server and capture
a successful POST /v1/chat in /docs for the PR. Weather may return 503 if upstream is down.

## Contract

Requests/responses are defined in schemas.py and ../worksheets/api_contract.md.
HTTP errors use {"error":{"code":"...","message":"..."}}.
Feedback is in memory and disappears at restart. Weather uses the supplied timeout,
retry and stale-cache implementation; tests use MockTransport rather than the internet.
