# Lab 6 — H2: Reflection and Real-Model Comparison

**Author:** Đặng Xuân Phát (MSSV: 25125062, `@Dang-Xuan-Phat`)  
**Reviewer:** Nguyễn Phúc Khánh (MSSV: 25125086, `@khanhf-ng820`)  

---

## 1. H2 — Reflection (5 lines)

1. Imagine taking an exam: instead of relying on pure memory (which can misremember or invent details), you take an **open-book exam** where you first look up the relevant textbook pages and base your answers strictly on those open pages.
2. That is RAG (Retrieval-Augmented Generation): a search engine retrieves exact handbook policies from our local database, and only then does the AI read those excerpts to compose a clear, helpful response for the student.
3. If search finds nothing relevant (or relevance scores fall below our minimum threshold), our code stops before calling the model and **abstains** (`A1`), immediately escalating to a human advisor instead of allowing the model to fabricate answers.
4. When the model does respond, our code enforces a strict **grounding check** (`A2`): it verifies that every cited source ID belongs to the chunks actually retrieved, catching ungrounded citations (`ProviderError`) and falling back to quoting verified handbook text directly.
5. In short, while an LLM produces fluent language, it cannot assess its own knowledge boundaries or guarantee factual truth; our programmatic wrapper acts as a strict proctor enforcing document grounding, citation provenance, and privacy guardrails.

---

## 2. Bonus — Real-Model Comparison (Ollama)

### Reproducibility Details
- **Command:**
  ```bash
  cd lab06/starter
  LLM_PROVIDER=ollama LLM_MODEL=qwen2.5-coder:7b .venv/bin/python eval/compare_paths.py
  ```
  *(On Windows PowerShell: `$env:LLM_PROVIDER="ollama"; $env:LLM_MODEL="qwen2.5-coder:7b"; .\.venv\Scripts\python.exe eval/compare_paths.py`)*
- **Model Metadata:** `qwen2.5-coder:7b` (Qwen2.5-Coder architecture, 7.6B parameters, GGUF Q4_K_M quantization, 32k context length).
- **Environment:** Ollama version `0.40.16` running locally on `http://localhost:11434`.
- **Model Selection Rationale:** `qwen2.5-coder:7b` was chosen as it was pre-installed and verified in the local developer environment, avoiding repetitive downloads of large model weights while offering robust structured JSON output compliance (`format="json"`).

### Comparison Results (across 20 cases in `eval/cases.jsonl`)

```
path                correct  abstain ok  p50 ms  max ms
deterministic          7/20       5/5     0.0     0.8   fails: E01 E02 E05 E06 E07 E08 E09 E10 E11 E12 E13 E14 E15
retrieval             16/20       4/5     0.1     0.2   fails: E13 E14 E15 E19
llm (stub)            16/20       4/5     0.3     0.6   fails: E13 E14 E15 E19
llm (ollama)          18/20       5/5  1204.1 14114.2   fails: E13 E15
```

### Key Observations:
- **Accuracy Improvement (16/20 → 18/20):**  
  The real model correctly solved **E19** ("is the final exam open-book", `expect_abstain: true`), successfully returning an abstention where retrieval-only quoted irrelevant text.  
  Furthermore, on **E14** ("can I take 32 credits", `expect_source: H26#6.1`), even though the BM25 retrieval ranked `H26#7.2` (Exam absence) first due to keyword overlap with "take", Ollama inspected both retrieved context chunks, identified that `H26#6.1` (Credit load) actually addressed credits, grounded its response in `H26#6.1`, and cited it correctly!
- **Latency Trade-off:**  
  The local model has a median latency of **1,204.1 ms** (with a max of 14,114.2 ms on initial cold-start model load into memory), compared to sub-millisecond execution for deterministic and retrieval paths.
- **Remaining Failures (E13, E15):**  
  Both cases failed at the retrieval stage (the BM25 index did not rank the target handbook chunk in the top-$k$ results for those phrasing variants), demonstrating that RAG generation quality is fundamentally bounded by retrieval recall.
