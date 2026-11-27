# Lab 7 — H2 reading

Owner: Đặng Xuân Phát (25125062)
Reading: Google PAIR Guidebook — the pages on **Feedback + Control** and **Errors + Graceful Failure**.

1. One idea I used today: From *Errors + Graceful Failure* (provide clear next steps instead of a dead end) and *Feedback + Control* (explicit user signals), our UI turns empty/overlong input, rate limits, backend outages, and low-confidence `escalate` answers into plain-language messages with a human fallback (Training Office, room I.101), while letting users rate answers with clear confirmation toasts.

2. One idea I would add: From *Feedback + Control* (pair binary ratings with specific context so feedback improves the system) and *Errors + Graceful Failure* (preserve user work on failure), I would add an optional short reason input after a negative rating and keep failed drafts editable in the prompt box on timeout or API errors so users can retry without retyping.
