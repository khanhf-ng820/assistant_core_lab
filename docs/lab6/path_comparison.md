# Lab 6 — comparing the three answer paths

Section owner: **Trần Thành Lợi — 25125059** (A2 + bonus H3).

Reproduce with, from `lab06/starter/`:

```bash
LLM_PROVIDER=stub .venv/Scripts/python -m pytest -q   # Windows; on macOS/Linux use .venv/bin/python
LLM_PROVIDER=stub .venv/Scripts/python eval/compare_paths.py
```

Settings used: `LLM_PROVIDER=stub`, `RETRIEVAL_KIND=bm25`, `RETRIEVAL_MIN_SCORE=2.0`,
`PROMPT_VERSION=answer_v1`, 20 cases in `eval/cases.jsonl`.

## 1. A1 + A2 in place, `tokenize` unchanged

```text
path                correct  abstain ok  p50 ms  max ms
deterministic          7/20       5/5     0.0     0.4   fails: E01 E02 E05 E06 E07 E08 E09 E10 E11 E12 E13 E14 E15
retrieval             16/20       4/5     0.0     0.1   fails: E13 E14 E15 E19
llm (stub)            16/20       4/5     0.2     0.4   fails: E13 E14 E15 E19
```

## 2. After H3 (`tokenize` drops a final `s` from words longer than four letters)

```text
path                correct  abstain ok  p50 ms  max ms
deterministic          7/20       5/5     0.0     0.4   fails: E01 E02 E05 E06 E07 E08 E09 E10 E11 E12 E13 E14 E15
retrieval             15/20       3/5     0.0     0.1   fails: E13 E14 E15 E19 E20
llm (stub)            15/20       3/5     0.2     0.4   fails: E13 E14 E15 E19 E20
```

`pytest -q` in `lab06/starter/` reports **42 passed** in both states; the change is
visible only in the benchmark, not in the unit tests.

## 3. Three sentences

For handbook questions I would use the **llm** path: it answers as many cases as
retrieval-only (16/20) but phrases the cited paragraph instead of dumping it, and both
paths sit behind the same A1 abort and A2 citation check, so neither can answer without
a retrieved source. I would not use the **deterministic** path for handbook questions
even though it is fastest and never wrong, because it only covers fees and office
lookups and it still fails 13/20 cases here. The first failure I would fix is **E15**
("how long can I keep a library book"): the router sees "library" and sends the question
to the office lookup, so a correct loan-period paragraph in `S26#1` never gets a chance
to answer.

## 4. H3 result — E14 does not pass, and E20 regresses

`tokenize("can I take 32 credits")` becomes `['take', '32', 'credit']`, so
`H26#6.1` (Credit load) now matches on the title as well as on the text and its score
rises from 1.254 to 1.425. That is not enough:

```text
query 'can I take 32 credits'   top hits (bm25, after H3)
H26#7.2  2.086   -> wins on the word "take" (Exam absence: "... take the exam ...")
H26#6.1  1.425   -> the chunk that should answer the question
```

Two reasons E14 still fails:

1. `H26#7.2` is the only chunk that contains the verb "take", so BM25 gives that word a
   high IDF and it outweighs two occurrences of "credit" in a longer chunk.
2. Even with the verb ignored, `H26#6.1` would score 1.425, below
   `RETRIEVAL_MIN_SCORE=2.0`, so the correct behaviour would be to abstain rather than
   cite `H26#6.1`. The case needs the reader to know that 32 > 30; lexical scoring
   cannot derive that from "more than 30 credits requires approval".

The second change is real progress in retrieval quality but breaks a benchmark
expectation: `"tell me about exams"` (E20) used to abstain because `exams` never matched
`exam`; after H3 it retrieves `H26#7.2` and answers, so the abstain count drops from 4/5
to 3/5. If the team wants the old 16/20 baseline, dropping the H3 commit is enough — it
is isolated in `src/assistant_core/rag/index.py`.
