# Study Assistant — starter

A rule-based study assistant for the CSC10014 Smart Virtual Assistant project. It helps students find campus office locations and operational hours from the command line.

## Prerequisites

- Python >= 3.10
- Git

## Setup

Clone the repository and prepare your isolated virtual environment:

```bash
# Clone via HTTPS (recommended) or SSH
git clone https://github.com/khanhf-ng820/assistant_core_lab.git
# or: git clone git@github.com:khanhf-ng820/assistant_core_lab.git
cd assistant_core_lab
python3 -m venv .venv
source .venv/bin/activate  # On Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

Verify the installation:

```bash
python -m assistant_core "where is the training office?"
```

## Run

Ask a single question directly via the command line:

```bash
python -m assistant_core "where is the training office?"
# Output: Training Office: room I.101, open Mon-Fri 07:30-16:30.
```

Or enter interactive mode (type `quit` or `exit` to leave):

```bash
python -m assistant_core
# Study assistant core (interactive mode). Type 'quit' or 'exit' to exit.
# > hi
# Hello! I can help with offices, fees and rules.
# > quit
```


### Supported queries

- Greetings: `hi`, `hello`, `hey`, `xin chao`, ...
- Office lookup: `where is the library?`
- Tuition: `tuition for 18 credits and 2 retake`
- Handbook rules: `thesis registration credits`

## Test

Run automated smoke tests using pytest:

```bash
pytest -q
```

Expected result: all unit tests pass.

## Evaluate

Lab 2 benchmark artifacts (`eval/cases.csv`, `eval/run.py`) are not shipped with this repository.

## Project structure

- `data/`: Sample datasets (`offices.csv`, `handbook.json`).
- `docs/`: Project documentation, reports, and worksheets.
- `lab03/`: Lab 3 monolith (intentionally non-compliant) and worksheets.
- `src/assistant_core/`: Core application package.
- `src/assistant_api/`: FastAPI application and Lab 5 persistence layer.
- `sql/`, `scripts/`: Lab 5 migrations and migrate/seed helpers.
- `api-tests/`: Manual curl and Postman checks.
- `tests/`: Automated tests.

## Troubleshooting

- **`No module named assistant_core`**: Ensure the virtual environment is active (`source .venv/bin/activate`) and you installed the package in editable mode with `pip install -e .`.
- **PowerShell blocks script execution on Windows**: Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` before running `.venv\Scripts\Activate.ps1`, or use Git Bash.
- **Python command not found**: On macOS/Linux, try `python3`; on Windows, try `py`.

## Week 4 — team API foundation

Install using the root setup above, then run from the repository root:

```bash
cp .env.example .env  # only if you do not already have a local .env
uvicorn assistant_api.main:create_app --factory --reload
```

Open http://127.0.0.1:8000/docs. `/health`, `POST /v1/chat`, `GET /v1/feedback`,
`GET /v1/weather`, and `GET /v1/offices` are implemented. `POST /v1/feedback` (T2)
remains a named TODO and returns 500 for valid requests until its owner lands it.
See [the team handoff](docs/lab4/foundation-handoff.md) for ownership and required acceptance tests.
H1 offices and Part F rate limiting are implemented.

Use a local API_ADMIN_KEY; never commit `.env`. Shell variables override dotenv settings.
Default/relative ASSISTANT_DATA_DIR paths resolve against the repository root;
absolute overrides are honored. CLI settings and behavior remain unchanged.

If you previously installed the standalone starter, remove its editable registration first:
`python -m pip uninstall study-assistant`, then `python -m pip install -e .`.
Do not install `lab04/starter` alongside the root project. It is reference material.

Validation from root:

```bash
python scripts/check_week3_tests.py
python -m pytest -q
ruff check .
ruff format --check .
```

With the API server running locally, `bash scripts/lab04_curl_smoke.sh` exercises
the five implemented endpoints; it intentionally omits T2 until that handler lands.
See [the curl transcript](docs/lab4/curl_transcript.md) for a recorded run.

CI covers Python 3.10/3.12 and automatically collects new tests in tests/api/.
A green foundation build does not mean all six endpoints are complete.

## Lab 5 — persistence (scaffolding)

The Lab 5 database persistence layer is fully implemented and wired into the API:

- `src/assistant_api/db.py` — SQLModel tables (`ChatSession`, `Interaction`, `Feedback`) and `Repository`.
- `sql/migrations/` — schema migrations applied in order by `scripts/migrate.py`.
- `scripts/seed.py` — synthetic interactions/feedback only (no real student data).
- `sql/my_queries.sql` — Part F analytical queries (Q1–Q3) and H2 advanced analysis with results.
- `api-tests/` — manual curl and Postman checks for the Lab 5 contract.

```bash
python scripts/migrate.py assistant.db
python scripts/seed.py assistant.db 300
sqlite3 assistant.db < sql/my_queries.sql
```

`Repository.add_feedback` (R1) and `list_feedback` (R2) are fully implemented across both root and
`lab05/starter/`. The API records interactions in `/v1/chat`, persists feedback across server restarts
in `POST /v1/feedback`, lists feedback in `GET /v1/feedback` (with fallback support), and exposes
`GET /v1/stats/intents`.

## Lab 6 — AI services & RAG (completed & integrated)

Status: **Completed & Merged**. All Lab 6 tasks (S1–S3, A1–A2, H1–H3) are implemented, verified, merged into `main`, and tagged `v0.6-ai`.

Source: `CSC10014_2026_Lab06_AI_Services_RAG_Tutorial.docx.pdf` (24 pages).
Work done in `lab06/practice/`, `lab06/starter/`, and `docs/lab6/`. Root `src/assistant_core` remains untouched.

Current status on `main`:
- `lab06/starter`: **43 passed** in `pytest -q`
- `lab06/practice`: **4 passed** in `pytest -q test_mini_search.py`
- Path comparison (`eval/compare_paths.py`): **25 test cases** evaluated across deterministic, retrieval, and LLM (stub + Ollama)

### Team integration & PR registry

| Member | ID | Primary responsibility | Rotation reviewer | Status & PR link | Done when |
|---|---|---|---|---|---|
| Nguyễn Phúc Khánh | 25125086 | A1 + integration lead | Trần Thành Lợi | [PR #51](https://github.com/khanhf-ng820/assistant_core_lab/pull/51) (Merged) | A1 test passes; one team version reviewed and merged; `v0.6-ai` tagged |
| Trần Thành Lợi | 25125059 | A2 + optional bonus H3 | Lý Tuấn Kiệt | [PR #49](https://github.com/khanhf-ng820/assistant_core_lab/pull/49) (Merged) | A2 test passes; full starter suite green; E14 re-checked if H3 is done |
| Lý Tuấn Kiệt | 25125022 | S1–S3 + demo | Trần Phúc Khánh | [PR #54](https://github.com/khanhf-ng820/assistant_core_lab/pull/54) (Merged) | `test_mini_search.py` 4/4 passes; explains inverted index and ranking |
| Trần Phúc Khánh | 25125020 | Comparison doc + security/data check | Nguyễn Minh Khang | [PR #58](https://github.com/khanhf-ng820/assistant_core_lab/pull/58) (Merged) | `docs/lab6/path_comparison.md` has the table and 3 sentences; no key or `.env` committed |
| Nguyễn Minh Khang | 25125018 | H1 five questions + QA | Đặng Xuân Phát | [PR #52](https://github.com/khanhf-ng820/assistant_core_lab/pull/52) (Merged) | E21–E25 added (3 normal, 2 abstain); comparison re-run; new table + failure analysis |
| Đặng Xuân Phát | 25125062 | H2 reflection + optional Ollama | Nguyễn Phúc Khánh | [PR #55](https://github.com/khanhf-ng820/assistant_core_lab/pull/55) (Merged) | `docs/lab6/reflection.md` has 5 lines; optional real-model comparison recorded |

### Verification commands

```bash
cd lab06/starter
.venv/bin/python -m pytest -q                              # result: 43 passed
cd ../practice
../starter/.venv/bin/python -m pytest -q test_mini_search.py  # result: 4 passed
cd ../starter
.venv/bin/python eval/compare_paths.py                     # runs 25 cases (E01–E25)
```

Bonus options: **H3** — in `src/assistant_core/rag/index.py`, make `tokenize`
remove a final `s` from words longer than four letters, then re-run the
comparison and check E14; or **Ollama** — run
`LLM_PROVIDER=ollama LLM_MODEL=llama3.2 python eval/compare_paths.py` if the
model is installed.

### Submission checklist

| What | When | How |
|---|---|---|
| S1–S3 + A1–A2, tests green | end of session | PR link on the LMS |
| Comparison table + 3 sentences | end of session | `docs/lab6/path_comparison.md` in the PR |
| Team merge and tag `v0.6-ai` | 23:59 the day before Lab 7 | tag link |
| H1 five questions + new table; H2 reflection | 23:59 the day before Lab 7 | PR link on the LMS |

### Grading

| Criterion | Points |
|---|---|
| S1–S3 mini search tests pass | 2 |
| A2 grounding check — tests pass | 2 |
| A1 abstain before the model — tests pass | 2 |
| Comparison table + three sentences | 1 |
| H1 five questions added, table re-run | 2 |
| H2 reflection | 1 |
| Bonus (Ollama run or H3 fix) | +1 |
| **Total** | **10 (+1)** |

## Lab 7 — UI & full-stack (in progress)

Status: **In progress — Core UI (L1, L2, F1), streaming bonus, Lab 7 CI, E.1–E.3, and H2 merged; H1 usability test, final D.4 sign-off, and `v0.7-mvp` tag remain.** `lab07/practice` is **4 passed** and `lab07/starter` is **55 passed**.

Source: `CSC10014_2026_Lab07_UI_Fullstack_Tutorial.docx.pdf` (20 pages).
Work done in `lab07/practice/`, `lab07/starter/`, and `lab07/worksheets/`. Root `src/` remains untouched.

### How to run both servers

The UI never imports `assistant_core`; it talks to the backend only through the HTTP API. Start the API
first, then the Streamlit page in a second terminal (both from `lab07/starter/`):

```bash
# terminal 1 — backend (http://127.0.0.1:8000)
cd lab07/starter
source .venv/bin/activate
uvicorn assistant_api.main:create_app --factory

# terminal 2 — UI (http://localhost:8501)
cd lab07/starter
source .venv/bin/activate
streamlit run ui/app.py
```

Set `ASSISTANT_API_URL=http://<host>:<port>` before `streamlit run` if the API is not on port 8000.

### Current status on `main`

- `lab07/practice`: **4 passed** — U1–U4 complete (merged via [PR #61](https://github.com/khanhf-ng820/assistant_core_lab/pull/61))
- `lab07/starter`: **55 passed** — L1 ([PR #73](https://github.com/khanhf-ng820/assistant_core_lab/pull/73)), L2 ([PR #61](https://github.com/khanhf-ng820/assistant_core_lab/pull/61)), F1 ([PR #63](https://github.com/khanhf-ng820/assistant_core_lab/pull/63)), streaming bonus ([PR #67](https://github.com/khanhf-ng820/assistant_core_lab/pull/67)), and UI accessibility tests ([PR #70](https://github.com/khanhf-ng820/assistant_core_lab/pull/70)) merged
- `tests/test_ui.py`: **7 passed**; `tests/test_streaming.py`: **2 passed**; `tests/test_ui_accessibility.py`: **4 passed**
- UI files: `ui/app.py` (page), `ui/api_client.py` (HTTP client), `ui/logic.py` (testable helpers), and `ui/streaming.py` (streaming bonus)
- Baseline committed in `f13bdf1`; root Ruff exclusion in `1e9c94b`
- Root CI and the dedicated Lab 7 CI job ([PR #66](https://github.com/khanhf-ng820/assistant_core_lab/pull/66)) are green on `main` (Python `3.10` and `3.12`)
- Bonus streaming ([issue #65](https://github.com/khanhf-ng820/assistant_core_lab/issues/65)) is merged via [PR #67](https://github.com/khanhf-ng820/assistant_core_lab/pull/67)

U1–U4: implemented and merged via [PR #61](https://github.com/khanhf-ng820/assistant_core_lab/pull/61); Nguyễn Phúc Khánh owns the evidence/verification. The PDF
describes the warm-up as an individual exercise; other members may still run it for practice.

### Team integration & PR registry

| Member | ID | Primary responsibility | Rotation reviewer | Status & PR link | Done when |
|---|---|---|---|---|---|
| Nguyễn Phúc Khánh | 25125086 | Integration lead: U1–U4 evidence, streaming bonus, CI, merge UI, README, tag `v0.7-mvp` | Trần Thành Lợi | [PR #66](https://github.com/khanhf-ng820/assistant_core_lab/pull/66) & [PR #67](https://github.com/khanhf-ng820/assistant_core_lab/pull/67) (Merged); [`docs/lab07/u1-u4.md`](docs/lab07/u1-u4.md); tag pending H1 + final D.4 | One UI version merged; both start commands documented; `v0.7-mvp` tagged; CI green |
| Trần Thành Lợi | 25125059 | L1 — show sources under each answer | Lý Tuấn Kiệt | [PR #73](https://github.com/khanhf-ng820/assistant_core_lab/pull/73) (Merged); [`docs/lab07/l1_sources.md`](docs/lab07/l1_sources.md) | `test_format_sources` passes; sources visible in the browser |
| Lý Tuấn Kiệt | 25125022 | L2 — escalation and degraded notes | Trần Phúc Khánh | [PR #61](https://github.com/khanhf-ng820/assistant_core_lab/pull/61) (Merged) | `test_status_note` passes; both notes verified in D.4 |
| Trần Phúc Khánh | 25125020 | F1 — 👎 feedback button + security/data check | Nguyễn Minh Khang | [PR #63](https://github.com/khanhf-ng820/assistant_core_lab/pull/63) (Merged) | Rating `-1` persists; toast appears; buttons disappear; no secrets committed |
| Nguyễn Minh Khang | 25125018 | H1 — real-user usability test + D.4 QA | Đặng Xuân Phát | [PR #71](https://github.com/khanhf-ng820/assistant_core_lab/pull/71) (Merged — preliminary D.4); H1 session + final D.4 pending | Three observations in the worksheet; one fix with before/after screenshot; D.4 states checked and signed off |
| Đặng Xuân Phát | 25125062 | UI/UX: checklist, accessibility, hallway test, H2 reading | Nguyễn Phúc Khánh | [PR #70](https://github.com/khanhf-ng820/assistant_core_lab/pull/70) (Merged) | Checklist 10/10 ticked; phone-width check; H2 two sentences; E.3 observation |

### Verification commands

```bash
cd lab07/practice
../starter/.venv/bin/python -m pytest -q                     # result: 4 passed
cd ../starter
.venv/bin/python -m pytest -q                               # result: 55 passed
.venv/bin/python -m pytest -q tests/test_ui.py              # result: 7 passed
```

### Lab 7 evidence

- U1–U4 warm-up: [`docs/lab07/u1-u4.md`](docs/lab07/u1-u4.md)
- L1 show sources: [`docs/lab07/l1_sources.md`](docs/lab07/l1_sources.md)
- D.4 browser acceptance: [`docs/lab07/d4_acceptance.md`](docs/lab07/d4_acceptance.md)
- H1 usability test: [`docs/lab07/h1_usability.md`](docs/lab07/h1_usability.md)
- H2 reading: [`docs/lab07/h2_reading.md`](docs/lab07/h2_reading.md)
- E.3 hallway test: [`docs/lab07/hallway_test.md`](docs/lab07/hallway_test.md)
- Raw worksheets: [`lab07/worksheets/`](lab07/worksheets/)

Bonus: **streaming/typewriter** — tracked in [issue #65](https://github.com/khanhf-ng820/assistant_core_lab/issues/65); a client-side `stream_text` helper plus
`st.write_stream` for the newest answer. It must not block the tag. A better sources display remains an
alternative.

### Submission checklist

| What | When | How |
|---|---|---|
| U1–U4 + L1, L2, F1, tests green; checklist ticked | end of session (draft PR OK) | PR link on the LMS |
| Team MVP v1, tag `v0.7-mvp`, README with both start commands | 23:59 the day before Lab 8 | Tech Lead: tag link |
| H1 observations + one fix; H2 two sentences | 23:59 the day before Lab 8 | PR link on the LMS |

### Grading

| Criterion | Points |
|---|---|
| U1–U4 tests pass | 2 |
| L1, L2 tests pass; F1 works in the browser | 3 |
| Every state in D.4 behaves as expected | 2 |
| Usability checklist completed | 1 |
| H1 three observations + one fix | 2 |
| Bonus (streaming or nicer sources) | +1 |
| **Total** | **10 (+1)** |
