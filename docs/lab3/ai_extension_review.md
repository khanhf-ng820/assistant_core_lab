# Lab 3 — AI Extension Review

## 1. Feature: Exam Absence Assistant

**AI Tool:** ChatGPT (OpenAI)

**AI-assisted task:** Implement a feature that answers student questions about missing a final examination using the university handbook.

The initial AI-generated implementation was created in `src/assistant_core/exam_absence.py`. It loaded `data/handbook.json`, searched for rule `H26-7.2`, and returned the rule's text.

The code was then manually reviewed and improved for reliability, correctness, and testability.

## 2. Review of AI-Generated Code

| # | What the AI generated | Problem found | What was changed | Why |
|---|---|---|---|---|
| 1 | `open("data/handbook.json")` | The relative path depends on the current working directory. | Replaced it with `pathlib.Path` using the Python module's location. | Allows the feature to work when launched from different directories. |
| 2 | `if "exam" not in message.lower(): return None` | Any exam-related question could trigger the absence response, even questions about exam schedules. | Added separate exam and absence keyword checks using `casefold()`. | Reduces incorrect intent detection and unrelated answers. |
| 3 | Direct `json.load()` without error handling or validation. | Missing files, invalid JSON, and malformed records were not handled consistently. | Added `ExamAbsenceDataError`, specific exception handling, and data structure validation. | Produces predictable errors and improves reliability. |

## 3. Human Verification

Added the following tests:

- `tests/test_exam_absence.py`: 10 unit tests.
- `tests/test_exam_absence_integration.py`: 4 integration tests.

Verification results:

- **14/14 tests passed.**
- **Ruff: All checks passed.**
- Confirmed that exam absence questions return the deadline of **3 working days** from handbook rule `H26-7.2`.
- Confirmed that unrelated exam questions do not return the absence rule.
- Confirmed that existing greeting and office lookup behavior remains functional in the starter responder.

## 4. Review Checklist

- **Interfaces:** Integrated with the existing starter `reply()` function. Integration with the final `AssistantService` architecture is still pending.
- **Dependencies:** No additional third-party dependencies introduced.
- **Security:** No API keys or secrets added.
- **Logging:** No user messages or confidential data logged.
- **Tests:** Added meaningful unit and integration tests.
- **Error handling:** Added explicit handling for missing or malformed knowledge data.

## 5. Remaining Improvements

The final implementation should reuse the team's shared `Handbook` and `DataError` interfaces once their modules are integrated. The team should also connect the feature through the final `router.py` and `service.py` architecture rather than relying only on the starter `rules.py`.

## 6. Conclusion

The AI-generated implementation provided a functional starting point but required human review to improve portability, intent detection, and error handling. Automated tests verified these improvements and helped prevent regressions in existing assistant functionality.