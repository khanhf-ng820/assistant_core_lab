# Lab 5 — H1 Audit, H2 Analytics Summary, and Team QA Scorecard

**Owner:** Đặng Xuân Phát (MSSV: 25125062, `@Dang-Xuan-Phat`) — UI/UX, QA/QC  
**Reviewer:** Nguyễn Phúc Khánh (MSSV: 25125086, `@khanhf-ng820`)  
**Branch:** `feat/h2-analytics-and-audit`  
**Verified Baseline:** `fd398ca`

---

## 1. H1 & Part C/D Practice Audit (`lab05/practice/`)

Executed against the local SQLite practice database (`lab05/practice/school.db`) and test suite:

| Suite / Tool | Scope | Observed Result | Notes |
| :--- | :--- | :--- | :--- |
| `python check.py` | SQL Q1–Q10 (Must) | **10/10 OK** | Schema selection, filtering, ordering, aggregation, `IS NULL` |
| `python check.py` | SQL Q11–Q15 (Should) | **5/5 OK** | Inner joins, multi-table aggregation, `LEFT JOIN ... IS NULL` |
| `pytest -q test_school_repo.py` | Python D1–D3 (`school_repo.py`) | **5 passed** | Parameterized SQL (`?`), `test_d1_no_sql_injection`, `average_grade`, `transcript` |

### Strictness Fixes Applied During H1 Audit (`lab05/practice/my_answers.sql`)

Three queries already scored `OK` on the fixed 8-row/17-enrollment `school.db` fixture purely by coincidental storage order or lack of multi-failure rows, but did not strictly satisfy the specification in `expected.json` and the exercise comments:

1. **Q8 (`number of students per program, by program`):** `expected.json` enforces `"ordered": true`. Added missing `ORDER BY program` instead of relying on SQLite `GROUP BY` order.
2. **Q9 (`average grade in CSC10004, rounded to 2 decimals`):** Wrapped `AVG(grade)` in `ROUND(AVG(grade), 2)` to match the prompt requirement cleanly across any floating-point input.
3. **Q13 (`names of students with a grade below 5, by name`):** `expected.json` enforces `"ordered": true`. Added `DISTINCT` (so a student with multiple grades `< 5` is listed once) and `ORDER BY s.name`.

---

## 2. H2 Analytical Query Summary (`sql/my_queries.sql`)

- Preserved Lý Tuấn Kiệt's Part F markers (`-- Q1`, `-- Q2`, `-- Q3`) untouched in `sql/my_queries.sql` to avoid overlapping with `feat/part-f-queries`.
- Appended the **H2** query measuring **backup/degraded path usage share, normal vs. degraded latency, unresolved rate, and thumbs-down rate** by `(intent, topic)` alongside an `ALL / (all)` roll-up, using a `feedback`-pre-aggregated CTE (`fb_summary`) so multiple ratings per `request_id` cannot inflate interaction counts.
- Executed `sql/my_queries.sql` directly via Python `sqlite3` against the seeded 300-interaction database generated from `scripts/migrate.py` + `scripts/seed.py assistant.db 300` (`random.seed(7)`: `59` chat sessions, `300` interactions, `96` feedback rows):

| Intent | Topic | Total | Degraded | Degraded % | Avg Normal (ms) | Avg Degraded (ms) | Unresolved | Feedback | Thumbs-Down | Thumbs-Down % |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `rule` | `H26-7.2` | 11 | 4 | 36.36% | 64.7 | 236.3 | 0 | 3 | 2 | 66.7% |
| `rule` | `H26-4.2` | 45 | 11 | 24.44% | 46.3 | 184.2 | 0 | 16 | 8 | 50.0% |
| `rule` | `H26-5.3` | 84 | 19 | 22.62% | 39.4 | 163.4 | 0 | 28 | 8 | 28.6% |
| `greeting` | `(none)` | 26 | 2 | 7.69% | 1.9 | 7.8 | 0 | 7 | 2 | 28.6% |
| `office` | `(none)` | 47 | 1 | 2.13% | 3.2 | 12.1 | 0 | 13 | 3 | 23.1% |
| `fee` | `(none)` | 61 | 1 | 1.64% | 4.8 | 21.2 | 0 | 21 | 4 | 19.0% |
| `unknown` | `(none)` | 26 | 0 | 0.00% | 8.1 | NULL | 26 | 8 | 8 | 100.0% |
| **ALL** | **(all)** | **300** | **38** | **12.67%** | **20.2** | **161.2** | **26** | **96** | **35** | **36.5%** |

**Key product takeaways:**
- **12.67%** (38/300) of interactions fell back to the degraded path, increasing mean response latency from **20.2 ms** to **161.2 ms** (~8x).
- **8.67%** (26/300) of interactions remained unresolved, concentrated 100% in `intent = 'unknown'`, which received **100.0% negative feedback** (8/8).
- Among matched rule topics, `H26-7.2` (`36.36%` degraded, `66.7%` thumbs-down) and `H26-4.2` (`24.44%` degraded, `50.0%` thumbs-down) are the primary candidates for retrieval/knowledge improvement.

---

## 3. Team-Wide Lab 5 QA Audit & Release Readiness (`v0.5-data`)

### 3.1 Rubric Checkpoint (Lab 5 PDF Grading Checklist)

| Criterion | Weight | Current Status on Team Branches |
| :--- | :---: | :--- |
| SQL Q1–Q10 correct | 3 pts | **PASS** — `10/10` (`check.py`) |
| SQL Q11–Q15 correct | 2 pts | **PASS** — `5/5` (`check.py`, strictness fixes in `my_answers.sql`) |
| D1–D3 tests pass (incl. SQL injection) | 2 pts | **PASS** — `5 passed` (`test_school_repo.py`) |
| R1–R2 tests pass; feedback survives restart | 2 pts | **BLOCKED AT INTEGRATION** — R1 on `feat/r1-add-feedback`, R2 committed inside `lab05/starter/` instead of root, root API still in-memory |
| F1–F3 or H2 query with result | 1 pt | **H2 PASS** in `sql/my_queries.sql`; F1–F3 pending push on `feat/part-f-queries` |
| Bonus H3 design review | +1 pt | **PASS** — `docs/lab5/data_model.md` on `origin/docs/bonus-design-review` (cross-review ready) |

### 3.2 Per-Member Branch & Deliverable Status

| STT | Member | MSSV | Branch Observed | Commit / Files Observed | Reviewer | Audit Status |
| :---: | :--- | :---: | :--- | :--- | :--- | :--- |
| 1 | Nguyễn Phúc Khánh | 25125086 | `origin/feat/r1-add-feedback` | `3571f2c` (merged `a4331f5` + `main`): `src/assistant_api/db.py` (R1 `add_feedback`), `tests/api/test_db.py` (un-xfailed), `docs/ai-use-log.md` | Trần Thành Lợi | **Ready for merge**; `v0.5-data` tag awaits team merges + API integration |
| 2 | Trần Phúc Khánh | 25125020 | `origin/docs/bonus-design-review` | `532e5d5` (refs `#38`): `docs/lab5/data_model.md` (186 lines), `docs/README.md`, `docs/ai-use-log.md` | Đặng Xuân Phát | **Approved / ready to merge**; doc-only scope, verified claims |
| 3 | Trần Thành Lợi | 25125059 | `origin/feat/r2-list-feedback-tranthanhloi` | `e2998b5`, `d438521`, `f6f357c`: edits in `lab05/starter/src/assistant_api/db.py`, `lab05/starter/tests/test_r2_list_feedback.py`, plus binary `lab05/starter/assistant.db` | Lý Tuấn Kiệt | **Changes requested (blocker)** — R2 targets `lab05/starter/` instead of root `src/assistant_api/db.py`; tracked binary `.db` (`118,784` bytes) |
| 4 | Lý Tuấn Kiệt | 25125022 | `feat/part-f-queries` | *Not yet pushed to `origin`* (`sql/my_queries.sql` Q1–Q3 blank on `main`) | Nguyễn Minh Khang | **Pending push** |
| 5 | Nguyễn Minh Khang | 25125018 | `origin/test/persistence-verification` | `370eb35`, `a94fef7`, `982d11c`: `tests/api/test_persistence_restart.py`, `docs/lab5/qa_report.md`, logs | Trần Phúc Khánh | **Partial / Blocked by API wiring** — repository reopen tests verified on R1; live HTTP server restart verification pending API SQLite wiring |
| 6 | Đặng Xuân Phát | 25125062 | `feat/h2-analytics-and-audit` | `lab05/practice/my_answers.sql`, `sql/my_queries.sql`, `docs/lab5/h1_audit_and_scores.md`, `docs/README.md`, `docs/ai-use-log.md` | Nguyễn Phúc Khánh | **Ready for review** |

### 3.3 Release Blockers Before Tagging `v0.5-data`

1. **Port R2 (`list_feedback`) to root and remove tracked `.db`:** `origin/feat/r2-list-feedback-tranthanhloi` updates `lab05/starter/src/assistant_api/db.py` (which root CI excludes from Ruff and root `pytest` does not execute) and commits `lab05/starter/assistant.db`. Move R2 and its unit test into root `src/assistant_api/db.py` and `tests/api/`, and remove tracked binary `assistant.db` (`*.db` is ignored at root).
2. **Wire `Repository` into `src/assistant_api/main.py`:** Root `main.py` still uses `feedback_store: list[FeedbackOut] = []`, so server restarts clear feedback despite passing `Repository` unit tests. Merge R1 + ported R2, then connect `/v1/chat` and `/v1/feedback` in `src/assistant_api/main.py` to SQLite so live Uvicorn restart QA (`test_persistence_restart.py` / end-to-end HTTP check) can pass before tagging `v0.5-data`.
3. **Push Part F (`F1–F3`):** Lý Tuấn Kiệt should push `feat/part-f-queries` with `Q1–Q3` filled in `sql/my_queries.sql` alongside the `H2` block below `-- Q3`.
4. **Non-blocking DB hardening follow-ups (documented in H3):** Enable `PRAGMA foreign_keys = ON` per SQLite connection (`make_engine` / `scripts/migrate.py`) and align ORM DDL with `sql/migrations/001_init.sql` rating checks.
