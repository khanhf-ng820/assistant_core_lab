# Lab 6 — Three Assistant Paths Comparison

**Author:** Đặng Xuân Phát (MSSV: 25125062, `@Dang-Xuan-Phat`)  
**Reviewer:** Nguyễn Phúc Khánh (MSSV: 25125086, `@khanhf-ng820`)  

---

## 1. Path Comparison Table (Required)

Results from `python eval/compare_paths.py` evaluated across 20 cases (`eval/cases.jsonl`):

| Path | Correct /20 | Abstain correct /5 | p50 latency | Controllability (1–5) | Main failure mode |
|---|:---:|:---:|:---:|:---:|---|
| **deterministic** | 7/20 | 5/5 | 0.0 ms | 5 | Cannot answer rule/policy questions not covered by hardcoded intents/tools (fails E01–E02, E05–E15). |
| **retrieval** | 16/20 | 4/5 | 0.0 ms | 4 | Vulnerable to vocabulary mismatch/paraphrasing (E13, E14, E15) and false-positive retrieval on ambiguous queries (E19). |
| **llm (stub)** | 16/20 | 4/5 | 0.3 ms | 4 | Bounded strictly by top retrieval hit; echoes first sentence of top-ranked chunk without semantic re-ranking. |

### Bonus: Local Real-Model Evaluation (Ollama `qwen2.5-coder:7b`)

| Path | Correct /20 | Abstain correct /5 | p50 latency | Controllability (1–5) | Main failure mode |
|---|:---:|:---:|:---:|:---:|---|
| **llm (ollama: qwen2.5-coder:7b)** | 18/20 | 5/5 | 1204.1 ms | 3 | High cold-start latency; fails when retrieval completely misses target chunk in top-$k$ context (E13, E15). |

---

## 2. Recommendation

**Which path would you ship for policy questions, and why? (3 sentences)**

1. For institutional policy questions, I would ship the **grounded LLM path with automated fallback to verbatim retrieval** because it combines conversational flexibility with strict citation grounding.
2. If the model is offline, experiences high latency, or fails validation twice, the system gracefully degrades to quoting the exact handbook chunk directly, ensuring students always receive verified policy facts without hallucinations.
3. The first failure I would fix is **retrieval recall on paraphrased queries (E13 and E15)**, because generation quality across all grounded paths is fundamentally bounded by the top-$k$ retrieved context.
