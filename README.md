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

The Lab 5 database layer is included but not wired into the API yet:

- `src/assistant_api/db.py` — SQLModel tables (`ChatSession`, `Interaction`, `Feedback`) and `Repository`.
- `sql/migrations/` — schema migrations applied in order by `scripts/migrate.py`.
- `scripts/seed.py` — synthetic interactions/feedback only (no real student data).
- `api-tests/` — manual curl and Postman checks for the Lab 5 contract.

```bash
python scripts/migrate.py assistant.db
python scripts/seed.py assistant.db 300   # requires R1 to be completed
sqlite3 assistant.db < sql/my_queries.sql
```

`Repository.add_feedback` (R1) and `list_feedback` (R2) remain TODOs, so the
root API keeps its in-memory feedback store and the known `POST /v1/feedback`
500 behavior. `/v1/chat` does not record interactions yet, and there is no
`GET /v1/stats/intents` endpoint in the root app.

## Lab 6 — AI services & RAG (task assignment)

Status: assignment only. No Lab 6 task has been implemented yet.

Source: `CSC10014_2026_Lab06_AI_Services_RAG_Tutorial.docx.pdf` (24 pages).
Work only in `lab06/practice/` and `lab06/starter/`; do not change the root
`src/assistant_core` app for this lab.

The `lab06/starter/.venv` is already installed with Python 3.13 (the pinned
pydantic/SQLModel versions do not support 3.14). Baseline before starting:
`pytest -q` in `lab06/starter` → **2 failed (A1, A2), 40 passed**;
`pytest -q test_mini_search.py` in `lab06/practice` → **2 failed, 2 passed**.

### Common task — every member

The tutorial's Team Integration step requires each member to open a PR with:

1. A working A1 and A2 (`src/assistant_core/rag/answerer.py`,
   `src/assistant_core/llm.py`) and green tests.
2. Their own `python eval/compare_paths.py` table.

The team reviews the PRs, merges one version, and keeps the deterministic and
retrieval paths for the Week 7 comparison.

### Primary assignments (merged version)

| Member | ID | Primary responsibility | Done when |
|---|---|---|---|
| Nguyễn Phúc Khánh | 25125086 | A1 + integration lead | A1 test passes; one team version reviewed and merged; `v0.6-ai` tagged |
| Trần Thành Lợi | 25125059 | A2 + optional bonus H3 | A2 test passes; full starter suite green; E14 re-checked if H3 is done |
| Lý Tuấn Kiệt | 25125022 | S1–S3 + demo | `test_mini_search.py` 4/4 passes; explains inverted index and ranking |
| Trần Phúc Khánh | 25125020 | Comparison doc + security/data check | `docs/lab6/path_comparison.md` has the table and 3 sentences; no key or `.env` committed |
| Nguyễn Minh Khang | 25125018 | H1 five questions + QA | E21–E25 added (3 normal, 2 abstain); comparison re-run; new table + one sentence on failures |
| Đặng Xuân Phát | 25125062 | H2 reflection + optional Ollama | `docs/lab6/reflection.md` has 5 lines; optional real-model comparison recorded |

### Verification commands

```bash
cd lab06/starter
.venv/bin/python -m pytest -q                              # target: 42 passed
cd ../practice
../starter/.venv/bin/python -m pytest -q test_mini_search.py  # target: 4 passed
cd ../starter
.venv/bin/python eval/compare_paths.py                     # paste the table into the PR
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
