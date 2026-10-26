# Lab 3 — AI Extension Review (Nguyễn Phúc Khánh)

## Feature: Help command

**AI Tool:** OpenCode

**AI-assisted task:** Add a `help` command that lists what the assistant can do.

The initial AI-generated implementation was created in `src/assistant_core/service.py`. It checked `if "help" in message.lower()` and returned a generic answer.

The code was then manually reviewed and improved for correctness, testability, and interface consistency.

## Review of AI-Generated Code

| # | What the AI generated | Problem found | What was changed | Why |
|---|---|---|---|---|
| 1 | `if "help" in message.lower(): return "..."` | Any message containing "help" (e.g. "I need help with fees") would trigger the help text. | Changed to an exact match after stripping and removing trailing punctuation. | Avoids hijacking real questions. |
| 2 | Returned `Intent.UNKNOWN` for help. | Help is not an unknown query; it should not be counted as a fallback. | Returns `Intent.GREETING` for the help answer. | Keeps metrics and routing consistent. |
| 3 | No tests. | The feature could regress silently. | Added `tests/test_help.py` with exact-match and punctuation cases. | Verifies the intended behavior. |

## Human Verification

- `pytest -q`: all tests pass.
- `ruff check .`: clean.
- Confirmed `help`, `Help?!`, and `  help  ` return the capabilities text.
- Confirmed `I need help with fees` still routes to a rule/fee, not help.

## Checklist

- Interfaces: uses `AssistantService.handle(Message) -> Response`; no new dependencies.
- Security: no secrets or user data logged.
- Tests: meaningful unit tests added.