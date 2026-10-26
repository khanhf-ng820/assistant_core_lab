"""Unit tests for assistant_core.router.

Tests deterministic intent classification across greetings, tuition/fee queries,
campus office searches, handbook rules, and edge cases.
"""

import pytest

from assistant_core.models import Intent
from assistant_core.router import GREETINGS, route

SAMPLE_OFFICE_NAMES = {"training office", "library", "student affairs"}


# ===========================================================================
# 1. Greeting Intent Tests
# ===========================================================================


@pytest.mark.parametrize(
    "greeting_text",
    [
        "hi",
        "hello",
        "hey",
        "xin chao",
        "chao",
        "good morning",
        "good afternoon",
        "good evening",
        "HI",
        "Hello!",
        "Hey???",
        "  xin chao  ",
        "Good Morning.",
    ],
)
def test_route_greetings(greeting_text: str):
    assert route(greeting_text, SAMPLE_OFFICE_NAMES) == Intent.GREETING


def test_greetings_constant_is_frozenset():
    assert isinstance(GREETINGS, frozenset)
    assert "hello" in GREETINGS
    assert "xin chao" in GREETINGS


# ===========================================================================
# 2. Fee Intent Tests
# ===========================================================================


@pytest.mark.parametrize(
    "fee_query",
    [
        "tuition for 18 credits",
        "what is the tuition fee?",
        "fee 15 credits",
        "TUITION DEADLINE",
        "tuition for 10 credits and 2 retake",
        "how much is the fee?",
    ],
)
def test_route_fee_queries(fee_query: str):
    assert route(fee_query, SAMPLE_OFFICE_NAMES) == Intent.FEE


# ===========================================================================
# 3. Office Intent Tests
# ===========================================================================


@pytest.mark.parametrize(
    "office_query",
    [
        "Where is the library?",
        "what time does the Training Office open?",
        "student affairs room",
        "LIBRARY location",
        "can you tell me where is Student Affairs?",
    ],
)
def test_route_office_queries(office_query: str):
    assert route(office_query, SAMPLE_OFFICE_NAMES) == Intent.OFFICE


def test_route_office_none_or_empty_names():
    # If no office names are provided, queries fall through to RULE
    assert route("Where is the library?", office_names=None) == Intent.RULE
    assert route("Where is the library?", office_names=set()) == Intent.RULE


# ===========================================================================
# 4. Rule Intent Tests (Default Knowledge Fallback)
# ===========================================================================


@pytest.mark.parametrize(
    "rule_query",
    [
        "can I register my thesis with 118 credits?",
        "exam absence policy",
        "graduation requirements",
        "what happens if I miss a midterm?",
        "where is the astronomy lab?",  # Unlisted office defaults to handbook search
    ],
)
def test_route_rule_queries(rule_query: str):
    assert route(rule_query, SAMPLE_OFFICE_NAMES) == Intent.RULE


# ===========================================================================
# 5. Empty / Punctuation Edge Cases
# ===========================================================================


@pytest.mark.parametrize(
    "empty_text",
    [
        "",
        "   ",
        "???",
        "!",
        "...",
        "   ?!.,   ",
    ],
)
def test_route_empty_and_punctuation_only_returns_unknown(empty_text: str):
    assert route(empty_text, SAMPLE_OFFICE_NAMES) == Intent.UNKNOWN
