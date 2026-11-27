# Lab 7 — D.4 browser acceptance

Runner: Nguyễn Minh Khang (25125018)
Sign-off: Nguyễn Phúc Khánh (25125086)
Status: **Preliminary browser QA recorded. Integration rerun and sign-off pending.**

Run with both servers from `lab07/starter/`:

```bash
# terminal 1
uvicorn assistant_api.main:create_app --factory

# terminal 2
streamlit run ui/app.py
```

## Browser run on 2026-11-27

Ran Chrome at 1366 × 960 against Streamlit 1.39.0 and a local FastAPI server using the stub provider and disposable SQLite data. The first run used `main` at `21284b8`. The team preview used [PR #63](https://github.com/khanhf-ng820/assistant_core_lab/pull/63) at `47ffb73` with the starter's documented L1 source formatter applied in an isolated copy so that the remaining states could be exercised.

| # | State | Expected | `main` at `21284b8` | Team preview |
|---|---|---|---|---|
| 1 | Click an example in the sidebar | Question and answer appear | **Fail.** Clicking the library example reached the API and then raised `NotImplementedError: L1` in the UI. | **Pass.** Clicking the thesis example displayed the question and answer. |
| 2 | Ask “Can I register my thesis with 118 credits?” | Answer with source `H26#5.3` | **Fail.** L1 raised while rendering the answer. | **Pass.** The answer showed the 120-credit requirement and `H26#5.3`. The lost-card question also returned Student Affairs, room I.102, and `S26#3`. [Screenshot](screenshots/d4-preview-sources.png) |
| 3 | Ask “what is the capital of France” | Escalation note with the Training Office | **Fail.** L1 raised before the note rendered. | **Pass.** The note directed the user to the Training Office, room I.101. |
| 4 | Press Enter on an empty box | Nothing is sent | **Pass.** The conversation and SQLite interaction count stayed the same. | **Pass.** Same result. |
| 5 | Click 👍 | Thank-you toast and rating buttons disappear | **Blocked.** L1 prevented any answer with a rating button from rendering. | **Fail.** The toast appeared and the `+1` row persisted. Both rating buttons remained visible immediately after voting. [Screenshot](screenshots/d4-preview-upvote.png) |
| 6 | Stop the API and ask again | Unreachable message without a crash | **Pass.** The backend warning and “Cannot reach the assistant” chat message appeared. [Screenshot](screenshots/d4-main-backend-down.png) | **Pass.** The chat reported the outage without a Streamlit exception. |

The practice suite passed all four tests. The starter suite on `main` had 48 passes and the L1 failure in `test_format_sources`. The preview passed all 49 starter tests.

## F1 extra check

- **Blocked on `main`.** The F1 button is in PR #63.
- **Pass on the preview.** Clicking 👎 displayed “Thanks — we will look at this answer,” hid both rating buttons and persisted one `rating = -1` row in SQLite. [Screenshot](screenshots/d4-preview-downvote.png)

Repeat D.4 and the F1 extra check on the integrated build once L1 and F1 land. The 👍 result remains open under [issue #69](https://github.com/khanhf-ng820/assistant_core_lab/issues/69).

Sign-off: ____________________  Date: ____________
