# Lab 3 — Before / After Maintainability Comparison

| Question | Before (Monolith) | After (Refactored Package) |
|---|---|---|
| Where would you change the credit rate? How many places? | One hard-coded constant (`RATE`) in the script. | One environment variable (`CREDIT_RATE_VND`) in `.env`, read by `config.py`. |
| Can you run the tests without internet or an API key? | No — the simulated LLM fails randomly. | Yes — 149 tests pass offline with `StubLLMResponder`; no API key required. |
| What happens if `handbook.json` is missing? | Prints and continues silently. | `Handbook.from_json()` raises `DataError` at startup. |
| Is any secret printed or logged? | Yes — the hard-coded API key can appear in debug output. | No — `llm_api_key` uses `repr=False` and logs never include the raw message or key. |
| How long does it take a new teammate to find the fee logic? | Inspect the ~65-line `handle()` function. | Open `src/assistant_core/tools.py` (`parse_credits`, `tuition`). |
| Number of global variables | 9 (3 mutable), per the lab analysis. | 0 mutable module-level globals (only immutable constants/loggers). |
| Number of bare `except:` blocks | 3, per the lab analysis. | 0 (specific exceptions only). |
| Lines in the longest function | ~65 (`handle`). | ~25 (`AssistantService.handle`). |
| `ruff check` issues | Not clean (monolith is intentionally non-compliant). | 0 (`lab03/` excluded). |
| Can you swap the LLM without touching the service? | No — LLM logic is coupled to the monolith. | Yes — `Responder` protocol with dependency injection. |

## Three-Sentence Reflection

The biggest improvement is the split into single-responsibility modules with typed contracts, which makes the fee logic, routing, and knowledge retrieval independently testable.

The refactor adds more files and interfaces, which increases navigation cost but removes hidden coupling and global state.

I would still improve request-level logging of latency and add a real provider implementation behind the `Responder` protocol in Week 4.