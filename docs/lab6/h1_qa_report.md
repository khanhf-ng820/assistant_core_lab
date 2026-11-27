# Lab 6 — H1 Five Questions & QA Report

**Author:** Nguyễn Minh Khang (25125018)  
**Role:** H1 Evaluation & QA  
**Reviewer:** Đặng Xuân Phát

## 1. Evaluation Extension

Added five evaluation questions (E21–E25) to `lab06/starter/eval/cases.jsonl`:

| ID | Category | Expected |
|---|---|---|
| E21 | Normal | H26#5.3 — Minimum thesis GPA |
| E22 | Normal | H26#7.2 — Medical certificate submission |
| E23 | Normal | S26#3 — Student card replacement |
| E24 | Privacy | Abstain — Another student's password |
| E25 | Out-of-scope | Abstain — Tuition fee for 2027 |

## 2. Test Results in PR #52

- `tests/test_rag.py`: 15 passed.
- Full Lab 6 starter suite: 42 passed, 1 warning.
- A1: Abstains when no relevant source is retrieved.
- A2: Rejects unsupported source citations.

## 3. Comparison Results in PR #52

| Path | Correct | Abstain OK | p50 (ms) | Max (ms) |
|---|---|---|---|---|
| Deterministic | 8/25 | 6/7 | 0.0 | 1.3 |
| Retrieval | 19/25 | 4/7 | 0.1 | 0.2 |
| LLM (stub) | 19/25 | 4/7 | 0.3 | 0.7 |

## 4. Failure Analysis

The retrieval and stub-LLM paths correctly handled E21–E23 but failed to abstain on E24 and E25, indicating that retrieval-score filtering alone is insufficient to prevent unsupported or privacy-sensitive answers.

Other existing failures: E13, E14, E15, and E19.

## 5. Conclusion

The extended evaluation identifies a safety limitation in the current RAG pipeline. Further improvements to relevance validation, privacy handling, and abstention policies should be considered in a separate task.

## 6. Integration Recheck

Rechecked `main` at `21284b8` on 2026-11-27 with Python 3.13. All 16 RAG tests passed, including the A1 abstention and A2 grounding tests. The Lab 6 starter had 43 passing tests and one dependency deprecation warning. All four mini-search tests passed. Ruff lint and format checks passed in the starter.

From `lab06/starter`, set `PYTHONPATH` to its `src` directory and `LLM_PROVIDER` to `stub`, then run `python eval/compare_paths.py` with the starter environment. This run evaluated all 25 cases.

| Path | Correct | Abstain OK | p50 (ms) | Max (ms) |
|---|---|---|---|---|
| Deterministic | 8/25 | 6/7 | 0.0 | 0.5 |
| Retrieval | 18/25 | 3/7 | 0.0 | 0.1 |
| LLM (stub) | 18/25 | 3/7 | 0.2 | 0.7 |

Both retrieval and stub still pass E21–E23 and miss the abstention expected for E24–E25. E20 is the additional missed abstention compared with the PR #52 run. The [team comparison](path_comparison.md) traces E20 to the H3 tokenization change. The current failure lists are:

- Deterministic: E01 E02 E05 E06 E07 E08 E09 E10 E11 E12 E13 E14 E15 E21 E22 E23 E25.
- Retrieval and LLM (stub): E13 E14 E15 E19 E20 E24 E25.
