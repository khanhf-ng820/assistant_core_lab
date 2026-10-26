# Future AI service interface

## Scope and current behaviour

This is the proposed contract for a future LLM adapter (issue #9). It defines
the boundary between the assistant and a provider; it adds no implementation,
dependency, network request, or API key requirement in this lab.

Today, [`AssistantService.handle`](../src/assistant_core/service.py) is the
synchronous backend entry point:

```python
from assistant_core.service import AssistantService, Message

service = AssistantService.default()
assert service.handle(Message(text="   ")).answer  # rejected at the boundary
```

The CLI in [`__main__.py`](../src/assistant_core/__main__.py) continues to call
that method. Its office answers come from the sample `data/offices.csv`; see the
[data specification](../data/README.md) for provenance and security limits.
This proposal does not make those records official university information.

## Function signature and data types

The future implementation is intended for `src/assistant_core/ai_service.py` (that
module does not exist yet). The following standard-library-only declarations
are a design example, not an importable service or a working LLM client:

```python
from dataclasses import dataclass
from typing import Literal, Protocol


@dataclass(frozen=True)
class Source:
    id: str
    title: str
    reference: str
    text: str


@dataclass(frozen=True)
class AIAnswer:
    text: str
    source_ids: tuple[str, ...]
    status: Literal["answered", "insufficient_context"]


class AIServiceError(Exception):
    """An operational provider failure, safe to handle with local fallback."""


class AnswerProvider(Protocol):
    def generate_answer(
        self,
        message: str,
        *,
        sources: tuple[Source, ...],
        timeout_seconds: float = 10.0,
    ) -> AIAnswer:
        ...
```

`generate_answer` is synchronous to match the current backend. The adapter
owns model selection, credentials, prompt construction, response parsing, and
the provider SDK. Callers depend only on this contract, so tests can inject an
in-memory fake provider.

## Inputs and validation

| Input | Contract |
| --- | --- |
| `message` | A string containing the student's current question. Trim surrounding whitespace; preserve original casing and language in the prompt. A direct provider call with blank input raises `ValueError`. |
| `sources` | An immutable tuple of approved context records supplied by retrieval. Each field must be non-empty, and IDs must be unique. `reference` identifies a local file or an approved public URL; it is metadata, not an instruction to fetch that URL. |
| `timeout_seconds` | A finite positive number of seconds, default `10.0`. It bounds the entire provider operation, including any retries. Invalid values raise `ValueError` before any request. |

Type mismatches raise `TypeError`; invalid field values raise `ValueError`.
An empty source tuple is valid and produces `insufficient_context` without a
network request. The first version should make one attempt with no automatic
retry, keeping the timeout behaviour predictable.

Send only the question and approved source text required to answer it. Do not
send secrets, private student records, or conversation history. Source text
and the question are untrusted content: they must not override service
instructions, select tools, or expose credentials. Retrieval and source
approval happen before calling the adapter; this function does not browse.

## Outputs and examples

| Field | Contract |
| --- | --- |
| `text` | Non-empty plain text. Render it as text in the UI rather than executing HTML or code. |
| `source_ids` | Unique IDs copied from the supplied `sources`. For `answered`, at least one supporting source is required. Resolve titles and references from the original `Source` objects, never from generated URLs. |
| `status` | `answered` when the supplied context supports the answer; `insufficient_context` when it does not. |

An `insufficient_context` result has empty `source_ids` and the fixed text
`I don't have enough verified context to answer that.` It is not a provider
outage and must not invent an answer from model memory. A parsed response with
an unknown status, missing text, duplicate or unknown source IDs, or an
`answered` status without a supporting source is an invalid response and must
raise `AIServiceError`.

Successful result using only the repository's sample data:

```python
training_source = Source(
    id="office:training",
    title="Training Office (sample data)",
    reference="data/offices.csv",
    text="Training Office: room I.101, open Mon-Fri 07:30-16:30.",
)
example_answer = AIAnswer(
    text=training_source.text,
    source_ids=(training_source.id,),
    status="answered",
)
assert example_answer.text == reply("Where is the Training Office?")

insufficient_answer = AIAnswer(
    text="I don't have enough verified context to answer that.",
    source_ids=(),
    status="insufficient_context",
)
```

These objects illustrate the contract; constructing them does not call a
model. A source ID enables traceability, but does not by itself prove that a
generated statement is supported. The adapter must check support against the
supplied context and treat unsupported output as `insufficient_context`.

## Errors and fallback

The future adapter translates provider-specific exceptions into this stable
error boundary. Exception details exposed to the UI must not contain prompts,
credentials, source contents, or raw provider responses.

| Condition | Adapter behaviour | Future caller behaviour |
| --- | --- | --- |
| Blank input, invalid source fields, or invalid timeout | Raise `ValueError` before a request. | Validate inputs; the normal chat path handles blank questions through `reply`. |
| Wrong argument type | Raise `TypeError` before a request. | Fix the caller; do not conceal programming errors as provider outages. |
| Timeout, connection failure, or provider unavailable | Raise `AIServiceError` with a safe message. | Return the original local rule response. |
| Rate limit or authentication/configuration failure | Raise `AIServiceError`; do not retry in this version. | Return the local response; log only a safe error category for maintainers. |
| Malformed or unsupported provider output, including fabricated source IDs | Raise `AIServiceError`. | Return the original local rule response. |
| Valid response with insufficient context | Return `AIAnswer` with `insufficient_context`. | Return the original local rule response. |

Proposed future integration order:

1. Compute `local_answer = reply(message)` and keep it for fallback.
2. Return it immediately for empty input, greetings, help, or a matched office.
   Before integrating AI, expose an explicit matched/unmatched signal from the
   rules layer; do not route by searching for words in a response string.
3. For an unmatched question, return `local_answer` if AI is disabled, no
   provider is configured, or approved context is empty.
4. Otherwise call `provider.generate_answer(message, sources=sources)` once.
5. Return validated answer text and its resolved sources for `answered`.
   On `AIServiceError` or `insufficient_context`, return `local_answer` with
   no AI citations. Catch only the operational error boundary; unrelated
   programming and CSV-loading errors remain visible to maintainers.

For example, an unavailable provider must preserve this existing answer:

```python
assert reply("What is the meaning of life?") == (
    "I don't know that yet. Try asking about an office, e.g. 'training office'."
)
```

This routing is a future integration plan. Current callers still use `reply`
directly, and this lab introduces no fallback wrapper or provider invocation.

## Verification and future implementation tests

For this documentation change, run the current regression suite from the
repository root:

```cmd
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\python.exe scripts\check_env.py
```

The Python examples above can be executed in order in one interpreter with
the package installed. They use only local records and standard-library types.

When the adapter is implemented, use a fake provider and a controllable clock
to test: a supported answer, empty and unrelated context, blank input, invalid
timeouts, malformed responses, unknown citation IDs, timeout and rate-limit
fallback, and preservation of greeting/help/office answers. Assert that no
provider call occurs for locally handled input or when AI is disabled. Those
future contract tests are not claimed as implemented or passed in this lab.
