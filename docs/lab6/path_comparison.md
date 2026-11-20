# Lab 6 — Three assistant paths

Owner: Trần Phúc Khánh (25125020) · Reviewer: Nguyễn Minh Khang
Ollama bonus run: Đặng Xuân Phát (25125062) · Reviewer: Nguyễn Phúc Khánh

## 1. Comparison table (team version on `main`)

Command, run in `lab06/starter` on `main` after A1, A2, H3 and S1–S3 were
merged. There is no `.env`, so the LLM path uses the offline `stub` provider.
Retrieval is BM25 with `min_score = 2.0`.

```text
$ python eval/compare_paths.py
path                correct  abstain ok  p50 ms  max ms
deterministic          7/20       5/5     0.0     0.8   fails: E01 E02 E05 E06 E07 E08 E09 E10 E11 E12 E13 E14 E15
retrieval             15/20       3/5     0.0     0.1   fails: E13 E14 E15 E19 E20
llm (stub)            15/20       3/5     0.2     0.5   fails: E13 E14 E15 E19 E20
```

Run twice with identical scores. At the same commit, `pytest -q` → 43 passed and
`pytest -q test_mini_search.py` → 4 passed.

| Path | Correct /20 | Abstain correct /5 | p50 latency | Controllability (1–5) | Main failure mode |
|---|---|---|---|---|---|
| deterministic | 7 | 5 | 0.0 ms | 5 | Cannot answer any rule/policy question (E01, E05–E15); only fee calc and office lookup work |
| retrieval | 15 | 3 | 0.0 ms | 4 | Wrong top chunk on lexical mismatch (E13, E14), and false confidence on off-topic exam questions (E19, E20) |
| llm (provider: stub) | 15 | 3 | 0.2 ms | 3 | Same as retrieval: it can only be as good as the retrieved sources; the grounding check (A2) stops invented citations but not a wrong-but-retrieved source |
| llm (provider: ollama `qwen2.5-coder:7b`, bonus) | 18 | 5 | 1204.1 ms | 3 | High latency; fails when retrieval misses the target chunk entirely (E13, E15) |

The Ollama row is Phát's bonus run from PR #55, measured before H3 was merged,
so it was not re-run here (Ollama is not installed on this machine).

### Failure notes (checked by printing the BM25 hits)

- **E13** "when is tuition due" → F26#1 (2.28) beats F26#3 (1.48).
- **E14** "can I take 32 credits" → after H3 the plural `credits` becomes
  `credit` and now matches, but H26#7.2 (2.09) still beats H26#6.1 (1.43).
- **E15** "how long can I keep a library book" → the router treats "library" as
  an office lookup before retrieval runs.
- **E19** "is the final exam open-book" should abstain, but "final exam" gives
  H26#7.2 a score of 5.62, so A1's threshold does not trigger.
- **E20** "tell me about exams" is a **new failure caused by H3**: before H3,
  `exams` matched nothing and the question abstained; now it stems to `exam`
  and hits H26#7.2 at 4.0. H3 fixed a term match on E14 without changing its
  result, and turned one correct abstain into a wrong answer.

## 2. Which path would you ship for policy questions, and why?

I would ship the retrieval path for policy questions, because it gets the same
15/20 as the stub LLM path while every answer is a direct quote of a cited
handbook section, so there is nothing a model can paraphrase wrongly. It is the
most controllable path that can answer policy questions at all: no provider
cost, no network dependency, and its failures are visible and fixable in
ranking and tokenization (E13, E14, E20), whereas the deterministic path answers
only 7/20. The real-model LLM path scored best in Phát's Ollama run (18/20) and
is worth enabling behind A1 and A2 with retrieval as the fallback, but only once
its ~1.2 s latency is acceptable and it is re-checked after H3.

## 3. Security / data check

| Check | Result |
|---|---|
| `.env` committed anywhere in history (`git log --all -- '*.env'`) | None; only `.env.example` files are tracked |
| `lab06/starter/.gitignore` ignores `.env`, `.venv/`, `*.db` | Yes |
| Real API keys in tracked files (`sk-…`, non-empty `LLM_API_KEY=`) | None; the only match is the fake `test-file-key` in a test fixture |
| `.env.example` contains placeholders only | Yes |
| LLM path sends only retrieved handbook chunks + the question to the provider (no student data, no DB rows) | Yes, see `build_prompt` in `src/assistant_core/llm.py` |
| Provider errors are logged by exception type only, not with the prompt or key | Yes (`ProviderError(f"...: {type(exc).__name__}")`) |
