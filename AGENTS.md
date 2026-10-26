# AGENTS.md — Study Assistant (CSC10014)

Repo-specific guidance for OpenCode agents. Every line answers: "Would an agent likely miss this without help?"

## Setup
1. `python3 -m venv .venv && source .venv/bin/activate` (Windows PowerShell: `.venv\Scripts\Activate.ps1`)
2. `pip install -r requirements.txt && pip install -e .`
- Python >= 3.10 required. `pyproject.toml` sets `pythonpath = ["src"]`.
- There is no `scripts/check_env.py` in this repo, despite README references.

## Run
- `python -m assistant_core "where is the training office?"`
- `python -m assistant_core` (interactive; `quit` or `exit` to leave)
- Logs (JSON) go to stderr; answers go to stdout.

## Tests
- `pytest -q` — currently fails collection on `main`: `tests/test_smoke.py` and `tests/test_eval.py` import the removed `assistant` package.
- `pytest tests/test_service.py -q` — passes (14 tests).
- Single test: `pytest tests/test_service.py::test_greeting -q`.
- `tests/test_eval.py` references `eval/cases.csv` and `eval/run.py`, which are not in this repo.

## Lint / format
- `ruff check .` (selects E,F,I,B,UP,BLE; line length 120)
- `ruff format --check .`
- `lab03/monolith/assistant_monolith.py` is intentionally non-compliant (the code smells are the lesson). On `main`, `ruff check .` reports errors there; open PRs add `extend-exclude = ["lab03"]`.

## Architecture
- Package is `src/assistant_core`; `src/assistant` no longer exists.
- Entry point: `src/assistant_core/__main__.py` -> `AssistantService.default()`.
- Public service: `AssistantService.handle(Message) -> Response` (`service.py`).
- On `main`, modules like `config.py`, `errors.py`, `models.py`, `router.py`, `knowledge.py`, `tools.py`, `responder.py`, `logging_setup.py` are missing or embedded in `service.py`; they exist on open PRs.
- `src/assistant_core/rules.py` is a legacy Lab 2 API; the Lab 3 target layout does not include it.
- Data: `data/offices.csv` (columns `name,room,hours`), `data/handbook.json` (array of `{id,title,text}`).
- `AssistantService.default(data_dir=...)` loads `data/` relative to repo root, with a fallback to the repo root.

## Data
- CSV columns exactly `name,room,hours`; UTF-8; no blank fields; unique names/rooms; valid 24-hour times.
- Public campus information only. No personal data, credentials, or secrets.

## Git workflow
- Work on a feature branch, not `main` (`refactor/assistant-core-<name>` / `feat/...`).
- Open a PR; at least one teammate approves before merge.
- Tests added/updated, `pytest -q` green, no secrets or personal data.
- Update README/docs if setup or behavior changed.
- Disclose AI use in the PR and `docs/ai-use-log.md`.
- Conventional commit messages (`feat:`, `fix:`, `docs:`, `chore:`).
- `main` is not currently protected and there are no CI workflows, despite `DEFINITION_OF_DONE.md` requiring CI green.

## Known sharp edges
- `README.md` is stale: wrong clone URL (`assistant-team07`), `python -m assistant`, references missing `scripts/`, `eval/`, `ui/`. Trust `pyproject.toml` and this file.
- `docs/architecture.md` may be ahead of the implementation on `main`.
- `docs/team.md` and `docs/README.md` still describe Lab 01.
- `docs/ai-interface.md` points to the deleted `src/assistant/rules.py`.
- `ui/README.md` is a separate project (AI Student Budget & Food Planner); this assistant is CLI-only.
- `CSC10014_*.docx.pdf` files must stay untracked: never `git add` them, never add them to `.gitignore`.
- `.env` is ignored; `.env.example` is committed and must contain safe placeholders only.
- `data/raw/` is ignored.
- This `AGENTS.md` is currently untracked in the working tree.