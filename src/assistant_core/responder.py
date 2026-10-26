"""Response generation behind one small interface (Adapter pattern).

``AssistantService`` depends only on the :class:`Responder` protocol, so the
provider can be swapped without touching business logic. Lab 3 ships two
offline implementations:

* :class:`TemplateResponder` -- deterministic, no AI, used as the fallback.
* :class:`StubLLMResponder` -- stands in for a real LLM and can simulate an
  outage by raising ``ProviderError``.

Both are deterministic: no randomness, no sleeping, no network and no API key,
which keeps tests and CI fast and reproducible. A real provider is added in
Week 4 by implementing ``explain`` and injecting it into the service.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from assistant_core.errors import ProviderError
from assistant_core.knowledge import Rule


@runtime_checkable
class Responder(Protocol):
    """Anything that can turn a handbook rule into an answer."""

    def explain(self, question: str, rule: Rule) -> str:
        """Return an answer for ``question`` grounded in ``rule``.

        Raises:
            ProviderError: when the provider cannot answer.
        """
        ...


class TemplateResponder:
    """Deterministic fallback that needs no provider or credentials."""

    def explain(self, question: str, rule: Rule) -> str:
        return f"{rule.title}: {rule.text}"


class StubLLMResponder:
    """A stand-in LLM used in tests and until the real provider arrives.

    Args:
        fail: when ``True``, every call raises ``ProviderError``. This lets the
            service's degraded/fallback path be tested without mocking or
            injecting a network failure.
    """

    def __init__(self, fail: bool = False) -> None:
        self.fail = fail

    def explain(self, question: str, rule: Rule) -> str:
        if self.fail:
            raise ProviderError("stub provider unavailable")
        return f"Based on '{rule.title}': {rule.text}"
