# Lab 6 — AI Services & RAG Submission Summary

**Course:** CSC10014 — Computational Thinking (2026)  
**Team:** Team 07 (`assistant-team07`)  
**Repository:** [khanhf-ng820/assistant_core_lab](https://github.com/khanhf-ng820/assistant_core_lab)  
**Milestone Tag:** [`v0.6-ai`](https://github.com/khanhf-ng820/assistant_core_lab/releases/tag/v0.6-ai)  
**Date:** 20 November 2026  

---

## 1. Grading Checklist Compliance (10/10 + 1 Bonus)

| Tutorial Item | Criteria | Status | Evidence / Location | Score |
|---|---|:---:|---|:---:|
| **Part B (S1–S3)** | Mini search tests pass | ✅ PASS | [lab06/practice/mini_search.py](file:///Users/admin/Desktop/HK1%20Year2/CS252%20CT/assistant_core_lab/lab06/practice/mini_search.py) (4/4 tests passed via `test_mini_search.py`) | 2 / 2 |
| **Part D (A2)** | Grounding check — tests pass | ✅ PASS | [lab06/starter/src/assistant_core/llm.py](file:///Users/admin/Desktop/HK1%20Year2/CS252%20CT/assistant_core_lab/lab06/starter/src/assistant_core/llm.py#L57-L58) (`test_citation_of_unretrieved_source_is_rejected` passed) | 2 / 2 |
| **Part E (A1)** | Abstain before model — tests pass | ✅ PASS | [lab06/starter/src/assistant_core/rag/answerer.py](file:///Users/admin/Desktop/HK1%20Year2/CS252%20CT/assistant_core_lab/lab06/starter/src/assistant_core/rag/answerer.py#L43-L50) (`test_abstain_when_nothing_relevant` passed) | 2 / 2 |
| **Part F** | Comparison table + 3 sentences | ✅ PASS | [docs/lab6/path_comparison.md](file:///Users/admin/Desktop/HK1%20Year2/CS252%20CT/assistant_core_lab/docs/lab6/path_comparison.md) and [lab06/worksheets/path_comparison.md](file:///Users/admin/Desktop/HK1%20Year2/CS252%20CT/assistant_core_lab/lab06/worksheets/path_comparison.md) | 1 / 1 |
| **Homework H1** | 5 questions added, table re-run | ✅ PASS | E21–E25 in [lab06/starter/eval/cases.jsonl](file:///Users/admin/Desktop/HK1%20Year2/CS252%20CT/assistant_core_lab/lab06/starter/eval/cases.jsonl) & report in [docs/lab6/h1_qa_report.md](file:///Users/admin/Desktop/HK1%20Year2/CS252%20CT/assistant_core_lab/docs/lab6/h1_qa_report.md) | 2 / 2 |
| **Homework H2** | Reflection (5 lines) | ✅ PASS | [docs/lab6/reflection.md](file:///Users/admin/Desktop/HK1%20Year2/CS252%20CT/assistant_core_lab/docs/lab6/reflection.md) (open-book exam picture + code check vs model) | 1 / 1 |
| **Bonus (H3 / Ollama)** | H3 Plural stem fix & Ollama run | ✅ PASS | H3 in [lab06/starter/src/assistant_core/rag/index.py](file:///Users/admin/Desktop/HK1%20Year2/CS252%20CT/assistant_core_lab/lab06/starter/src/assistant_core/rag/index.py#L38-L40); Ollama run (`qwen2.5-coder:7b`) in [docs/lab6/reflection.md](file:///Users/admin/Desktop/HK1%20Year2/CS252%20CT/assistant_core_lab/docs/lab6/reflection.md) | +1 |
| **Total** | | | **All requirements fulfilled** | **11 / 10** |

---

## 2. Team Member Contributions & Pull Request Registry

| Member | Student ID | Role | Assigned Task | PR / Issue Links | Status |
|---|:---:|:---:|---|---|:---:|
| **Nguyễn Phúc Khánh** | 25125086 | Tech Lead | Task A1 abstain check, starter unit tests, team integration merge, milestone tag `v0.6-ai` | [PR #51](https://github.com/khanhf-ng820/assistant_core_lab/pull/51), [Issue #50](https://github.com/khanhf-ng820/assistant_core_lab/issues/50) | Merged |
| **Trần Thành Lợi** | 25125059 | Developer | Task A2 grounding check in `parse_draft`, Bonus H3 plural stem in `tokenize` | [PR #49](https://github.com/khanhf-ng820/assistant_core_lab/pull/49) | Merged |
| **Lý Tuấn Kiệt** | 25125022 | Developer | Task S1–S3 mini search engine (`build_index`, `search` scoring/ranking) | [PR #54](https://github.com/khanhf-ng820/assistant_core_lab/pull/54), [Issue #53](https://github.com/khanhf-ng820/assistant_core_lab/issues/53) | Merged |
| **Trần Phúc Khánh** | 25125020 | Developer | Part F path comparison table, 3-sentence recommendation, failure diagnosis & security/data audit | [PR #58](https://github.com/khanhf-ng820/assistant_core_lab/pull/58) | Merged |
| **Nguyễn Minh Khang** | 25125018 | QA/QC | Homework H1: five questions (E21–E25 in `cases.jsonl`), re-run comparison table & QA analysis | [PR #52](https://github.com/khanhf-ng820/assistant_core_lab/pull/52) | Merged |
| **Đặng Xuân Phát** | 25125062 | Developer | Homework H2 reflection (5 lines) & Ollama real-model comparison (`qwen2.5-coder:7b`) | [PR #55](https://github.com/khanhf-ng820/assistant_core_lab/pull/55) | Merged |

---

## 3. Automated Verification Evidence

### 1. Lab 6 Starter Test Suite
```bash
cd lab06/starter && .venv/bin/python -m pytest -q
```
**Result:** `43 passed, 1 warning` in 2.82s.

### 2. Lab 6 Practice Test Suite
```bash
cd lab06/practice && ../starter/.venv/bin/python -m pytest -q test_mini_search.py
```
**Result:** `4 passed` in 0.05s.

### 3. Path Comparison Evaluation (25 Test Cases)
```bash
cd lab06/starter && .venv/bin/python eval/compare_paths.py
```
**Result:**
```text
path                correct  abstain ok  p50 ms  max ms
deterministic          8/25       6/7     0.0     1.5   fails: E01 E02 E05 E06 E07 E08 E09 E10 E11 E12 E13 E14 E15 E21 E22 E23 E25
retrieval             18/25       3/7     0.1     0.1   fails: E13 E14 E15 E19 E20 E24 E25
llm (stub)            18/25       3/7     0.3     1.0   fails: E13 E14 E15 E19 E20 E24 E25
```

### 4. Root Test Suite & Invariants
```bash
pytest -q
python scripts/check_week3_tests.py
```
**Result:** `229 passed, 4 skipped, 0 failed`; all 14 baseline Week 3 test files remain untouched.

### 5. Static Analysis & Formatting
```bash
ruff check . && ruff format --check .
```
**Result:** All checks passed cleanly.
