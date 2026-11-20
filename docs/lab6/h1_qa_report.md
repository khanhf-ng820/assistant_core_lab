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

## 2. Test Results

- `tests/test_rag.py`: 15 passed.
- Full Lab 6 starter suite: 42 passed, 1 warning.
- A1: Abstains when no relevant source is retrieved.
- A2: Rejects unsupported source citations.

## 3. Comparison Results

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