# Lab 7 — D.4 browser acceptance

Runner: Nguyễn Minh Khang (25125018)
Sign-off: Nguyễn Phúc Khánh (25125086)
Status: **Pending — requires L1 and F1 merged.**

Run with both servers from `lab07/starter/`:

```bash
# terminal 1
uvicorn assistant_api.main:create_app --factory

# terminal 2
streamlit run ui/app.py
```

| # | State | Expected | Result | Evidence |
|---|---|---|---|---|
| 1 | Click an example in the sidebar | Question and answer appear | Pending | |
| 2 | Ask "Can I register my thesis with 118 credits?" | Answer + `Sources: H26#5.3 — …` | Pending | |
| 3 | Ask "what is the capital of France" | Escalation note with the Training Office | Pending | |
| 4 | Press Enter on an empty box | Nothing is sent | Pending | |
| 5 | Click 👍 | "Thanks" toast; the buttons disappear | Pending | |
| 6 | Stop the API, ask again | "Cannot reach the assistant…" instead of a crash | Pending | |

## F1 extra check

- Click 👎 → toast says "Thanks — we will look at this answer."
- Both rating buttons disappear after the vote.
- A `rating = -1` row is persisted in SQLite.

Sign-off: ____________________  Date: ____________
