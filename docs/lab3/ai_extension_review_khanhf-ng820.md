# Lab 3 — AI Extension Review (Nguyễn Phúc Khánh)

## Feature: Help command

**AI Tool:** OpenCode

**AI-assisted task:** Add a `help` command that lists what the assistant can do.

The initial AI-generated implementation checked `if "help" in message.lower()` and returned a generic answer.

## Review of AI-Generated Code

| # | What the AI generated | Problem found | What was changed | Why |
|---|---|---|---|---|
| 1 | `if "help" in message.lower()` | Any message containing "help" triggered the help text. | Changed to an exact match after stripping and removing trailing punctuation. | Avoids hijacking real questions. |
| 2 | Returned `Intent.UNKNOWN` for help. | Help is not an unknown query. | Returns `Intent.GREETING` for the help answer. | Keeps routing consistent. |
| 3 | No tests. | The feature could regress silently. | Added `tests/test_help.py` with exact-match, punctuation, and non-hijack cases. | Verifies intended behavior. |

## Human Verification

- `pytest -q`: all tests pass.
- `ruff check .`: clean.
- Confirmed `help`, `Help?!`, and `  help  ` return the capabilities text.
- Confirmed `I need help with fees` does not return the help text.