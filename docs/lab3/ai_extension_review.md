# Lab 3 — AI Extension Review

**Author:** Đặng Xuân Phát (MSSV: 25125062)  
**Role:** Member 3 — QA/QC, UI/UX (Logging & Quality Gate)  
**Feature Extended:** Comprehensive `help` command and guided capability discovery  

---

## 1. Feature Description
Add a `help` intent/command to `assistant_core` that guides students on how to interact with the assistant (discovering office locations, calculating tuition fees, and searching handbook rules) in both English and Vietnamese.

---

## 2. Prompt Used
```text
Extend assistant_core with a 'help' command that informs students about the assistant's capabilities
(locating offices, calculating tuition fees, searching academic rules). Please implement intent routing,
service handling, and CLI integration.
```

---

## 3. Manual Review & Refactoring Table

| # | What the AI generated | Problem you found | What you changed | Why |
|---|---|---|---|---|
| **1** | Hardcoded `if "help" in text: print(...)` directly inside `execute_query` in `__main__.py` bypassing the service layer. | Violates separation of concerns and bypasses the core domain service architecture (`Intent` enum and `route()` function). Breaks if accessed via API or GUI. | Added `Intent.HELP = "help"` to `Intent(str, Enum)` in `models.py` and added `HELP_TRIGGERS = frozenset({"help", "tro giup", "huong dan", "support"})` inside `router.py` and handled it in `AssistantService.handle()`. | Preserves clean layered architecture, ensures uniform behavior across all entry points (CLI, REPL, web), and maintains type safety. |
| **2** | Emitted raw user input to stdout/logging via `logger.info(f"User asked for help: {text}")`. | Violates Twelve-Factor XI (Logs as event streams) and student privacy; logging raw query text leaks user input and potentially sensitive data into log files. | Retained structured JSON logging through `extra={"intent": "help", "latency_ms": ..., "session": ..., "degraded": False}` without logging raw student text. | Adheres to privacy standards, prevents PII leakage into log aggregation pipelines, and satisfies structured JSON logging specifications. |
| **3** | Provided a single trivial test checking `help` substring, without testing edge cases, punctuation, or logging. | Fragile test coverage that failed on punctuation (`HELP?!`), failed to test bilingual support (`tro giup`), and did not verify structured log event emission. | Created a dedicated test suite `tests/test_help.py` with 4 comprehensive tests: `test_route_help()`, `test_service_handle_help()`, `test_service_handle_vietnamese_help()`, and `test_cli_help_structured_log(caplog)`. | Enforces strict Quality Gate standards, guarantees robust regex/normalization resilience, and verifies structured JSON log records via `pytest.LogCaptureFixture`. |

---

## 4. Quality & Security Checklist

- [x] **Interfaces respected:** Returns standard `Response(answer=..., intent=Intent.HELP, sources=[], degraded=False)` conforming to the Pydantic schema contract.
- [x] **New dependencies:** Zero new dependencies introduced (uses existing standard library and core packages).
- [x] **Secrets:** No API keys or credentials leaked or required.
- [x] **Logging of user data:** No raw student text in logs; only structured metadata (`intent`, `latency_ms`, `session`, `degraded`) emitted to stderr.
- [x] **Tests added and meaningful:** 4 automated unit tests added in `tests/test_help.py` (100% pass rate).

---

## 5. Academic Integrity Disclosure
Recorded in [`docs/ai-use-log.md`](../ai-use-log.md).
