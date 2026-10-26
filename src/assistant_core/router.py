"""Deterministic intent router for incoming student queries.

Classifies user inquiries into Intent categories using pattern matching
and keyword rules, without external LLM dependencies.
"""

from __future__ import annotations

from collections.abc import Iterable

from assistant_core.models import Intent

GREETINGS: frozenset[str] = frozenset(
    {
        "hi",
        "hello",
        "hey",
        "xin chao",
        "chao",
        "good morning",
        "good afternoon",
        "good evening",
    }
)


def route(text: str, office_names: Iterable[str] | None = None) -> Intent:
    """Classify student input message into an Intent.

    Evaluation precedence:
        1. Empty / whitespace -> Intent.UNKNOWN
        2. Greeting match -> Intent.GREETING
        3. Fee or tuition keywords -> Intent.FEE
        4. Matching campus office directory name -> Intent.OFFICE
        5. Fallback -> Intent.RULE

    Args:
        text: Student message text.
        office_names: Optional iterable of known office names in lower-case.

    Returns:
        Intent: Classified intent enum value.
    """
    normalized = text.lower().strip().rstrip("?!.,")
    if not normalized:
        return Intent.UNKNOWN

    if normalized in GREETINGS:
        return Intent.GREETING

    if "fee" in normalized or "tuition" in normalized:
        return Intent.FEE

    if office_names:
        for name in office_names:
            if name and name.lower() in normalized:
                return Intent.OFFICE

    return Intent.RULE
