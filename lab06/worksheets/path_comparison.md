# Lab 6 — Three assistant paths

Run `python eval/compare_paths.py` and fill in.

| Path | Correct /20 | Abstain correct /5 | p50 latency | Controllability (1–5) | Main failure mode |
|---|:---:|:---:|:---:|:---:|---|
| deterministic | 7/20 | 5/5 | 0.0 ms | 5 | Cannot answer policy questions outside hardcoded rules/tools (fails E01–E02, E05–E15). |
| retrieval | 16/20 | 4/5 | 0.0 ms | 4 | Paraphrase vocabulary mismatch (E13–E15) and false match on ambiguous query (E19). |
| llm (provider: stub) | 16/20 | 4/5 | 0.3 ms | 4 | Strictly bounded by top retrieval hit; echoes top chunk without semantic re-ranking. |

### Optional Bonus: Local Model Comparison

| Path | Correct /20 | Abstain correct /5 | p50 latency | Controllability (1–5) | Main failure mode |
|---|:---:|:---:|:---:|:---:|---|
| llm (provider: ollama) | 18/20 | 5/5 | 1204.1 ms | 3 | High cold-start latency; bounded when retrieval misses target chunk in top-k context. |

Which path would you ship for policy questions, and why? (3 sentences)

For institutional policy questions, I would ship the grounded LLM path with automated fallback to verbatim retrieval because it combines conversational flexibility with strict citation grounding. If the model is offline, experiences high latency, or fails validation twice, the system gracefully degrades to quoting the exact handbook chunk directly, ensuring students always receive verified policy facts without hallucinations. The first failure I would fix is retrieval recall on paraphrased queries (E13 and E15), because generation quality across all grounded paths is fundamentally bounded by the top-k retrieved context.
