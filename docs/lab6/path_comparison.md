# Lab 6 — Three assistant paths

Owner: Trần Phúc Khánh (25125020) · Reviewer: Nguyễn Minh Khang

Command (run in `lab06/starter`, A1 + A2 implemented, no `.env`, so the LLM
path uses the offline `stub` provider; retrieval is BM25 with `min_score = 2.0`):

```text
$ python eval/compare_paths.py
path                correct  abstain ok  p50 ms  max ms
deterministic          7/20       5/5     0.0     0.6   fails: E01 E02 E05 E06 E07 E08 E09 E10 E11 E12 E13 E14 E15
retrieval             16/20       4/5     0.0     0.1   fails: E13 E14 E15 E19
llm (stub)            16/20       4/5     0.1     0.4   fails: E13 E14 E15 E19
```

Starter suite at the same commit: `pytest -q` → 42 passed.

| Path | Correct /20 | Abstain correct /5 | p50 latency | Controllability (1–5) | Main failure mode |
|---|---|---|---|---|---|
| deterministic | 7 | 5 | 0.0 ms | 5 | Cannot answer any rule/policy question (E01, E05–E15); only fee calc and office lookup work |
| retrieval | 16 | 4 | 0.0 ms | 4 | Wrong top chunk on lexical mismatch (E13 ranks F26#1 above F26#3; E14 "credits" ≠ "credit"); false confidence on E19 (score 5.6 on H26#7.2 for an open-book question) |
| llm (provider: stub) | 16 | 4 | 0.1 ms | 3 | Same as retrieval: it can only be as good as the retrieved sources; the grounding check (A2) stops invented citations but not a wrong-but-retrieved source |

Failure notes (checked by printing the BM25 hits):

- **E13** "when is tuition due" → F26#1 (2.28) beats F26#3 (1.48).
- **E14** "can I take 32 credits" → H26#7.2 (2.09) beats H26#6.1 (1.48); the
  plural `credits` does not match `credit` (this is the H3 bonus fix).
- **E15** "how long can I keep a library book" → the router treats "library" as
  an office lookup before retrieval runs.
- **E19** "is the final exam open-book" should abstain, but "final exam" gives
  H26#7.2 a high score, so A1's score threshold does not trigger.

## Which path would you ship for policy questions, and why?

I would ship the retrieval path for policy questions, because it gets the same
16/20 as the LLM path while every answer is a direct quote of a cited handbook
section, so there is nothing the model can paraphrase wrongly. It is also the
most controllable of the paths that can answer policy questions at all: it has
no provider cost, no network dependency, and fails in ways we can see and fix
(ranking and tokenization, as in E13/E14), whereas the deterministic path
answers only 7/20. The LLM path is worth keeping behind A1 (abstain before the
model) and A2 (grounding check) for nicer wording, but only after a real model
beats retrieval on this eval, since the stub adds latency without adding
correctness.

## Security / data check

| Check | Result |
|---|---|
| `.env` committed anywhere in history (`git log --all -- '*.env'`) | None; only `.env.example` files are tracked |
| `lab06/starter/.gitignore` ignores `.env`, `.venv/`, `*.db` | Yes |
| Real API keys in tracked files (`sk-…`, non-empty `LLM_API_KEY=`) | None; the only match is the fake `test-file-key` in a test fixture |
| `.env.example` contains placeholders only | Yes |
| LLM path sends only retrieved handbook chunks + the question to the provider (no student data, no DB rows) | Yes, see `build_prompt` in `src/assistant_core/llm.py` |
| Provider errors are logged by exception type only, not with the prompt or key | Yes (`ProviderError(f"...: {type(exc).__name__}")`) |
