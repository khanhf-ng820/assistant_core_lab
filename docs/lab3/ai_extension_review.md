# Lab 3 — AI Extension Review

This file collects the team's individual AI-extension reviews.

---

## Review 1 — Exam Absence Assistant (Nguyễn Minh Khang)

**AI Tool:** ChatGPT (OpenAI)

**AI-assisted task:** Implement a feature that answers student questions about missing a final examination using the university handbook.

The initial AI-generated implementation was created in `src/assistant_core/exam_absence.py`. It loaded `data/handbook.json`, searched for rule `H26-7.2`, and returned the rule's text.

The code was then manually reviewed and improved for reliability, correctness, and testability.

### Review of AI-Generated Code

| # | What the AI generated | Problem found | What was changed | Why |
|---|---|---|---|---|
| 1 | `open("data/handbook.json")` | The relative path depends on the current working directory. | Replaced it with `pathlib.Path` using the module's location. | Allows the feature to work when launched from different directories. |
| 2 | `if "exam" not in message.lower(): return None` | Any exam-related question could trigger the absence response, even questions about exam schedules. | Added separate exam and absence keyword checks using `casefold()`. | Reduces incorrect intent detection and unrelated answers. |
| 3 | Direct `json.load()` without error handling or validation. | Missing files, invalid JSON, and malformed records were not handled consistently. | Added `ExamAbsenceDataError`, specific exception handling, and data structure validation. | Produces predictable errors and improves reliability. |

### Human Verification

- Added `tests/test_exam_absence.py`: 10 unit tests.
- Added `tests/test_exam_absence_integration.py`: 4 integration tests.
- **14/14 tests passed.**
- **Ruff: All checks passed.**
- Confirmed exam absence questions return the deadline of **3 working days** from handbook rule `H26-7.2`.
- Confirmed unrelated exam questions do not return the absence rule.
- Confirmed existing greeting and office lookup behavior remains functional.

### Checklist

- Interfaces: integrated with the starter `reply()` function; integration with the final `AssistantService` architecture is still pending.
- Dependencies: no additional third-party dependencies.
- Security: no API keys or secrets added.
- Logging: no user messages or confidential data logged.
- Tests: meaningful unit and integration tests added.
- Error handling: explicit handling for missing or malformed knowledge data.

### Remaining Improvements

The final implementation should reuse the team's shared `Handbook` and `DataError` interfaces once their modules are integrated. The team should also connect the feature through the final `router.py` and `service.py` architecture rather than relying only on the starter `rules.py`.

---

## Review 2 — Help Command (Đặng Xuân Phát, MSSV: 25125062)

**Role:** Member 3 — QA/QC, UI/UX (Logging & Quality Gate)

**Feature Extended:** Comprehensive `help` command and guided capability discovery

### Prompt Used

```text
Extend assistant_core with a 'help' command that informs students about the assistant's capabilities
(locating offices, calculating tuition fees, searching academic rules). Please implement intent routing,
service handling, and CLI integration.
```

### Manual Review & Refactoring

| # | What the AI generated | Problem found | What was changed | Why |
|---|---|---|---|---|
| 1 | Hardcoded `if "help" in text: print(...)` directly inside `execute_query` in `__main__.py`. | Violates separation of concerns and bypasses the core domain service architecture. | Added `Intent.HELP = "help"` to `models.py` and `HELP_TRIGGERS` to `router.py`, handled in `AssistantService.handle()`. | Preserves clean layered architecture and type safety. |
| 2 | Emitted raw user input via `logger.info(f"User asked for help: {text}")`. | Violates Twelve-Factor XI and student privacy. | Retained structured JSON logging via `extra={"intent": "help", ...}` without raw text. | Prevents PII leakage into logs. |
| 3 | Single trivial test for `help` substring. | Fragile coverage; no punctuation, bilingual, or logging tests. | Created `tests/test_help.py` with 4 comprehensive tests. | Enforces quality gate standards. |

### Quality & Security Checklist

- Interfaces respected: returns standard `Response(answer=..., intent=Intent.HELP, sources=[], degraded=False)`.
- New dependencies: none.
- Secrets: none leaked.
- Logging of user data: no raw student text.
- Tests: 4 automated unit tests (100% pass rate).

### Academic Integrity Disclosure

Recorded in `docs/ai-use-log.md`.