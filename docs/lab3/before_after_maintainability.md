# Lab 3 — Before / After Maintainability Comparison

Fill in for the monolith (before) and your refactored package (after).

| Question | Before (Monolith) | After (assistant_core) |
|---|---|---|
| Where would you change the credit rate? How many places? | 1 hard-coded constant (`RATE = 450000`) in code. | 1 environment variable (`CREDIT_RATE_VND`) in `.env`, loaded via `Settings`. |
| Can you run the tests without internet or an API key? | No. Random failures in simulated LLM make tests flaky and non-deterministic. | Yes. Deterministic offline tests using `StubLLMResponder` and characterisation tests. |
| What happens if `handbook.json` is missing? | Prints `"could not load handbook"` and continues silently, causing hidden failures later. | Raises `DataError` at startup or service initialisation, failing fast with a clear message. |
| Is any secret printed or logged? | Yes. Hard-coded `API_KEY` is printed in debug messages. | No. `llm_api_key` uses `repr=False` in Pydantic; `JsonFormatter` sanitizes sensitive keys and omits secrets. |
| How long does it take a new teammate to find the fee logic? | 10–15 minutes scanning through the 163-line mixed `handle()` function. | Less than 1 minute; isolated in pure functions inside `tools.py` with dedicated unit tests. |
| Number of global variables | 9 module-level globals (3 mutable: `history`, `offices`, `handbook`). | 0 module-level mutable globals; dependencies injected via `AssistantService.__init__`. |
| Number of bare `except:` blocks | 3 (`except:` in `load()` and `main()`), catching even `KeyboardInterrupt`. | 0 bare `except:`; specific named exceptions derived from `AssistantError` and built-ins. |
| Lines in the longest function | ~65 lines (`handle()` doing routing, parsing, searching, calling LLM). | ~15 lines (`AssistantService.handle()` delegating to dedicated modules). |
| `ruff check` issues | 9+ errors (`E401`, `E722` bare except, `BLE001` blind except, `E501` line too long, `I001`). | 0 errors (`All checks passed!`, including `ruff check --select BLE .`). |
| Can you swap the LLM without touching the service? | No. Directly coupled to hard-coded `llm()` function. | Yes. Follows the Adapter pattern via `Responder` Protocol; swap providers without altering service code. |

## Three-Sentence Reflection

1. **What improved most:** The separation of concerns into single-responsibility modules, complete elimination of global mutable state and bare excepts, and structured JSON logging that strictly prevents secret and query leakage.
2. **What got more complex:** The number of files, directory layout, and architectural layers (Pydantic models, custom exception hierarchies, adapter protocols) increased compared to a single flat script.
3. **What I would still change:** Add asynchronous streaming responses for future real LLM providers in Lab 4, and introduce a persistent vector or SQLite database for the handbook knowledge base.
