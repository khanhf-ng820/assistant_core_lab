# Lab 5 — Data & SQL Persistence Submission Summary

**Course:** CSC10014 — Computational Thinking (2026)  
**Team:** Team 07 (`assistant-team07`)  
**Repository:** [khanhf-ng820/assistant_core_lab](https://github.com/khanhf-ng820/assistant_core_lab)  
**Milestone Tag:** [`v0.5-data`](https://github.com/khanhf-ng820/assistant_core_lab/releases/tag/v0.5-data)  
**Date:** 18 November 2026  

---

## 1. Grading Checklist Compliance (10/10 + 1 Bonus)

| Tutorial Item | Criteria | Status | Evidence / Location | Score |
|---|---|:---:|---|:---:|
| **Part C (Q1–Q10)** | Basic SQL Queries | ✅ PASS | [lab05/practice/my_answers.sql](file:///Users/admin/Desktop/HK1%20Year2/CS252%20CT/assistant_core_lab/lab05/practice/my_answers.sql) verified with `check.py` | 3 / 3 |
| **Part C (Q11–Q15)** | Joins & Aggregations | ✅ PASS | [lab05/practice/my_answers.sql](file:///Users/admin/Desktop/HK1%20Year2/CS252%20CT/assistant_core_lab/lab05/practice/my_answers.sql) (Score: 15/15) | 2 / 2 |
| **Part D (D1–D3)** | Python SQLite Repo | ✅ PASS | [lab05/practice/test_school_repo.py](file:///Users/admin/Desktop/HK1%20Year2/CS252%20CT/assistant_core_lab/lab05/practice/test_school_repo.py) (5/5 tests passed, injection-safe) | 2 / 2 |
| **Part E (R1–R2)** | Persistence & Restart | ✅ PASS | `add_feedback` (R1) & `list_feedback` (R2) implemented in both root and starter; server restart verified | 2 / 2 |
| **Part F / H2** | Query & Execution Result | ✅ PASS | [sql/my_queries.sql](file:///Users/admin/Desktop/HK1%20Year2/CS252%20CT/assistant_core_lab/sql/my_queries.sql) (Q1–Q3 + H2 analytics query with execution output on 300 rows) | 1 / 1 |
| **Bonus H3** | Schema Security Review | ✅ PASS | [docs/lab5/data_model.md](file:///Users/admin/Desktop/HK1%20Year2/CS252%20CT/assistant_core_lab/docs/lab5/data_model.md) and [lab05/worksheets/data_model.md](file:///Users/admin/Desktop/HK1%20Year2/CS252%20CT/assistant_core_lab/lab05/worksheets/data_model.md) | +1 |
| **Total** | | | **All requirements fulfilled** | **11 / 10** |

---

## 2. Team Member Contributions & Pull Request Registry

| Member | Student ID | Role | Assigned Task | PR / Issue Links | Status |
|---|:---:|:---:|---|---|:---:|
| **Nguyễn Phúc Khánh** | 25125020 | Tech Lead | R1 `add_feedback`, persistence consolidation, server restart tests, tag `v0.5-data` | [PR #36](https://github.com/khanhf-ng820/assistant_core_lab/pull/36), [Issue #35](https://github.com/khanhf-ng820/assistant_core_lab/issues/35) | Merged |
| **Trần Thành Lợi** | 25125048 | Developer | R2 `list_feedback`, 300-row synthetic seeding dataset | [PR #41](https://github.com/khanhf-ng820/assistant_core_lab/pull/41), [Issue #40](https://github.com/khanhf-ng820/assistant_core_lab/issues/40) | Merged |
| **Lý Tuấn Kiệt** | 25125022 | Developer | Part F queries Q1–Q3 & analysis documentation | [PR #45](https://github.com/khanhf-ng820/assistant_core_lab/pull/45), [Issue #44](https://github.com/khanhf-ng820/assistant_core_lab/issues/44) | Merged |
| **Đặng Xuân Phát** | 25125062 | Developer | H2 analytics query + execution results, H1 15/15 audit | [PR #42](https://github.com/khanhf-ng820/assistant_core_lab/pull/42), [Issue #43](https://github.com/khanhf-ng820/assistant_core_lab/issues/43) | Merged |
| **Trần Phúc Khánh** | 25125020 | Developer | H3 bonus data model & security design review | [PR #39](https://github.com/khanhf-ng820/assistant_core_lab/pull/39), [Issue #38](https://github.com/khanhf-ng820/assistant_core_lab/issues/38) | Merged |
| **Nguyễn Minh Khang**| 25125018 | QA/QC | SQLite lifecycle verification, restart test suite & QA report | [PR #37](https://github.com/khanhf-ng820/assistant_core_lab/pull/37), [Issue #46](https://github.com/khanhf-ng820/assistant_core_lab/issues/46) | Merged |

---

## 3. Automated Verification Evidence

### 1. Lab 5 Starter Suite
```bash
cd lab05/starter && pytest -q
```
**Result:** `31 passed, 0 failed` in 2.94s.

### 2. Root Test Suite
```bash
pytest -q
```
**Result:** `229 passed, 4 skipped, 0 failed, 0 xfailed` in 7.82s.

### 3. Week 3 Test Immutability
```bash
python scripts/check_week3_tests.py
```
**Result:** `All 14 original Week 3 test files are unchanged.`

### 4. Practice Verification
```bash
cd lab05/practice && python check.py
cd lab05/practice && pytest test_school_repo.py
```
**Result:** `Score: 15/15` in `check.py`; `5 passed` in `test_school_repo.py`.

### 5. Static Analysis & Formatting
```bash
ruff check .
ruff format --check .
```
**Result:** All checks passed cleanly.
