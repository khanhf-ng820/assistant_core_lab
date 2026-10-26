# Lab 3 — Before / After Maintainability Comparison

| Question | Before (Monolith) | After (Refactored Package) |
|---|---|---|
| Where would you change the credit rate? How many places? | One hard-coded constant (`RATE`) in the Python script. | One environment variable (`CREDIT_RATE_VND`) managed by `config.py`. Integration pending. |
| Can you run the tests without internet or an API key? | Tests are not deterministic because the simulated LLM can fail randomly. | 19 unit tests were executed offline: 7 model tests and 12 knowledge tests using a temporary `DataError` stub. Full integration tests are pending. |
| What happens if `handbook.json` is missing? | The monolith handles the error silently and continues. | `Handbook.from_json()` raises `DataError`. Integration with the team's actual `errors.py` is pending. |
| Is any secret printed or logged? | Yes. The hard-coded API key can appear in debug output. | The new models and knowledge modules do not print secrets. Full logging and configuration integration remain pending. |
| How long does it take a new teammate to find the fee logic? | They must inspect the large `handle()` function. | Fee calculations will be isolated in `tools.py`, making them easier to locate. Integration pending. |
| Number of global variables | 9, including 3 mutable globals, according to the lab analysis. | No mutable module-level state in the new models and knowledge modules. Full-package count not yet verified. |
| Number of bare `except:` blocks | 3, according to the lab analysis. | 0 in the newly implemented modules. Full-package audit pending. |
| Lines in the longest function | Approximately 65 lines in `handle()`. | The service is intended to use smaller functions. The longest function in the fully integrated package has not yet been measured. |
| `ruff check` issues | Not measured for the original monolith. | No Ruff violations in the five files contributed for the assigned modules and tests. |
| Can you swap the LLM without touching the service? | No. The LLM logic is tightly coupled to the monolith. | The proposed `Responder` interface supports dependency injection. Integration remains pending. |

## Three-Sentence Reflection

The most significant improvement is the separation of responsibilities into typed models, knowledge retrieval, and reusable test fixtures, making the code easier to test and maintain.

The refactoring introduces more files, interfaces, and dependencies, which increases integration complexity but improves modularity.

I would further improve the system by completing integration tests, verifying error handling with the real shared exceptions, and ensuring consistent interfaces across all team modules.