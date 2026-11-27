# Lab 7 — Usability checklist (tick before your user test)

- [x] The first screen says what the assistant can do, with example questions
- [x] Empty or too-long input shows a friendly message (not a crash)
- [x] While waiting, the user sees "Thinking…"
- [ ] Every answer from documents shows its sources *(pending L1 `format_sources` in `ui/logic.py`)*
- [x] "I don't know" answers tell the user who can help (escalation)
- [x] If the backend is down, the page says so clearly
- [ ] Each answer has 👍 / 👎, and clicking gives a "thanks" message *(👍 present; 👎 pending F1 PR #63)*
- [x] The page says it is an AI assistant
- [x] Text is readable (size, contrast); buttons have clear labels
- [x] Works on a phone-width window
