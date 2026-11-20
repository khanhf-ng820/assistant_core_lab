# Lab 6 — Three assistant paths

Run `python eval/compare_paths.py` and fill in.

| Path | Correct /20 | Abstain correct /5 | p50 latency | Controllability (1–5) | Main failure mode |
|---|:---:|:---:|:---:|:---:|---|
| deterministic | 7/20 | 5/5 | 0.0 ms | 5 | Cannot answer policy questions outside hardcoded rules/tools. |
| retrieval | 16/20 | 4/5 | 0.0 ms | 4 | Paraphrase vocabulary mismatch (E13–E15) and false match on ambiguous query (E19). |
| llm (provider: stub) | 16/20 | 4/5 | 0.3 ms | 4 | Strictly bounded by top retrieval hit; fails when top hit is incorrect. |
| llm (provider: ollama) | 18/20 | 5/5 | 1204.1 ms | 3 | High latency; fails when retrieval misses target chunk in top-k context. |

Which path would you ship for policy questions, and why? (3 sentences)

For institutional policy questions, I would ship the grounded LLM path with automated fallback to verbatim retrieval. The LLM path flexibly understands paraphrased student queries while our code strictly controls accuracy by verifying that all cited section IDs exist in the retrieved context and abstaining immediately when retrieval scores fall below threshold. If the model is offline, experiences high latency, or fails validation twice, the system gracefully degrades to quoting the exact handbook chunk directly, ensuring students always receive verified policy facts without hallucinations.
