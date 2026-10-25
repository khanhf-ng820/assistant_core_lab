# System Architecture: `assistant_core`

This document outlines the architecture, component boundaries, service interface contract, and core design decisions of the `assistant_core` package.

---

## 1. Module Responsibility Table

In accordance with Single Responsibility (cohesion) and Loose Coupling, each module owns one specific concern:

| Module | Responsibility |
|---|---|
| `config.py` | Reads and validates settings from environment variables and `.env`. |
| `errors.py` | Defines the named domain exception hierarchy (`AssistantError`, `ConfigError`, `DataError`, `InvalidRequest`, `ProviderError`). |
| `models.py` | Defines public typed data contracts (`Message`, `Response`, `Intent`, `Source`) via Pydantic. |
| `router.py` | Determines the student's `Intent` using deterministic pattern-matching rules. |
| `knowledge.py` | Encapsulates campus office directory (CSV) and student handbook (JSON) retrieval with search. |
| `tools.py` | Provides pure, deterministic tuition calculation functions without side effects or I/O. |
| `responder.py` | Implements the response generation adapter pattern behind a common `Responder` protocol (`TemplateResponder`, `StubLLMResponder`). |
| `service.py` | Contains `AssistantService.handle(Message) -> Response` — the single orchestrator and public entry point. |
| `logging_setup.py` | Configures structured JSON logging with security guards to prevent credential and message leakage. |
| `__main__.py` | Provides the Command-Line Interface supporting both argument-based queries and interactive REPL sessions. |

---

## 2. The Service Interface Contract

The central interface is `AssistantService.handle(msg: Message) -> Response`:

```python
AssistantService.handle(msg: Message) -> Response
```

### Input Model: `Message`
- `text: str`: Cleaned user query (1 to 2000 characters).
- `session_id: str`: Session identifier (defaults to `"local"`).

### Output Model: `Response`
- `answer: str`: Human-readable answer text.
- `intent: Intent`: Classified intent (`GREETING`, `FEE`, `OFFICE`, `RULE`, or `UNKNOWN`).
- `sources: list[Source]`: List of cited knowledge sources containing `id` and `title` (empty for non-rule intents).
- `degraded: bool`: Flag indicating whether a fallback responder was used (`True` if the primary provider failed).

### Error Boundaries & Lifecycle
- **Input Validation**: Invalid or empty requests raise a `ValidationError` at the API boundary before execution.
- **Startup Errors**: Missing or invalid environment configurations raise `ConfigError`; unreadable data files raise `DataError`.
- **Runtime Provider Failures**: External provider failures (e.g., LLM network outage, timeout) raise `ProviderError` inside the adapter, but are caught by `AssistantService.handle()`. The service logs a warning, switches to `TemplateResponder`, and returns the exact rule citation with `degraded = True`. Provider failures never crash the calling application.

---

## 3. Architecture Decisions & Rationales

### Decision 1: Deterministic Fee Calculation in `tools.py` (Never by LLM)
- **Context**: Tuition calculations must be legally and financially accurate. LLMs are non-deterministic and prone to arithmetic hallucination.
- **Decision**: All fee computations are isolated into pure, deterministic functions (`parse_credits` and `tuition`) in `tools.py`.
- **Rationale**: Pure functions have no side effects, require no network I/O, and can be thoroughly validated with characterisation and boundary unit tests.

### Decision 2: LLM Adapter Behind `Responder` Protocol
- **Context**: Relying on live external LLM APIs causes test flakiness, slows down continuous integration (CI), consumes tokens, and requires API keys during development.
- **Decision**: The LLM interaction is abstracted behind a `Responder` Protocol (the Adapter Pattern), with interchangeable implementations (`TemplateResponder` and `StubLLMResponder`).
- **Rationale**: Developers and automated CI pipelines can run the entire test suite completely offline without API credentials. In Week 4, a real provider class will be plugged in without changing a single line of `AssistantService`.

### Decision 3: 12-Factor Configuration via Environment Variables & `.env.example`
- **Context**: Hardcoding rates, API keys, or paths inside source code violates Factor III of The Twelve-Factor App and risks leaking credentials into version control.
- **Decision**: Configuration is loaded strictly from environment variables through `Settings` in `config.py`, with safe defaults and placeholders documented in `.env.example`.
- **Rationale**: Keeps sensitive credentials out of Git history and allows seamless configuration shifts between local development, testing, and production environments. Sensitive keys use `repr=False` to ensure they never leak into logs or error traces.
