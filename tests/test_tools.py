"""Characterisation and unit tests for assistant_core.tools.

Captures legacy behavior from assistant_monolith.py and provides thorough
boundary and edge-case testing for pure tuition calculation and credit parsing.
"""

import pytest

from assistant_core.errors import InvalidRequest
from assistant_core.tools import parse_credits, tuition

# ===========================================================================
# 1. Characterisation Tests (Parity with assistant_monolith.py)
# ===========================================================================


def test_characterisation_monolith_normal_tuition_with_retake():
    """Verify parity with monolith: 'tuition for 18 credits and 2 retake'."""
    text = "tuition for 18 credits and 2 retake"
    credits, retake = parse_credits(text)
    assert credits == 18
    assert retake == 2

    # Monolith formula: 18 * 450000 + 2 * 450000 * 1.5 = 8,100,000 + 1,350,000 = 9,450,000
    total = tuition(credits=credits, retake=retake, rate=450_000, retake_multiplier=1.5, max_credits=30)
    assert total == 9_450_000


def test_characterisation_monolith_too_many_credits():
    """Verify parity with monolith: 'tuition 40 credits' exceeds 30 credit limit."""
    text = "tuition 40 credits"
    credits, retake = parse_credits(text)
    assert credits == 40
    assert retake == 0

    with pytest.raises(InvalidRequest, match="Credits must be between 1 and 30"):
        tuition(credits=credits, retake=retake, rate=450_000, retake_multiplier=1.5, max_credits=30)


def test_characterisation_monolith_missing_credits():
    """Verify parity with monolith: missing credits prompts 'How many credits?'."""
    with pytest.raises(InvalidRequest, match="How many credits?"):
        parse_credits("tuition")

    with pytest.raises(InvalidRequest, match="How many credits?"):
        parse_credits("what is the fee?")


def test_characterisation_monolith_zero_credits():
    """Verify parity with monolith: 0 credits triggers 'How many credits?'."""
    with pytest.raises(InvalidRequest, match="How many credits?"):
        parse_credits("tuition for 0 credits")


# ===========================================================================
# 2. Unit Tests for parse_credits
# ===========================================================================


@pytest.mark.parametrize(
    ("input_text", "expected_credits", "expected_retake"),
    [
        ("tuition for 15 credits", 15, 0),
        ("fee 20", 20, 0),
        ("tuition for 18 credits and 2 retake", 18, 2),
        ("fee for 10 credits and 1 retakes", 10, 1),
        ("2 retake and 14 credits", 14, 2),
        ("4 credits and 4 retake", 4, 4),
        ("TUITION FOR 16 CREDITS AND 2 RETAKE", 16, 2),
        ("fee 1 credit", 1, 0),
        ("tuition 30 credits", 30, 0),
        # Edge cases: mixed-unit phrases & large retake counts
        ("tuition for 15 hours and 2 retake courses", 15, 2),
        ("fee for 20 credits, 3 retakes and 2 lab sessions", 20, 3),
        ("tuition for 15 credits and 100 retake", 15, 100),
    ],
)
def test_parse_credits_valid(input_text: str, expected_credits: int, expected_retake: int):
    credits, retake = parse_credits(input_text)
    assert credits == expected_credits
    assert retake == expected_retake


@pytest.mark.parametrize(
    "invalid_input",
    [
        "",
        "   ",
        "tuition",
        "how much is the fee?",
        "tuition for 2 retake",  # Only retake given, missing main course credits
        "tuition for 0 credits",
        # Edge cases: non-numeric credit values & mixed ambiguous text
        "tuition for ten credits",
        "calculate tuition fee for full semester",
        "how much is tuition for three courses?",
    ],
)
def test_parse_credits_invalid_raises(invalid_input: str):
    with pytest.raises(InvalidRequest, match="How many credits?"):
        parse_credits(invalid_input)


# ===========================================================================
# 3. Unit Tests for tuition (Pure Function Boundary Checks)
# ===========================================================================


def test_tuition_standard_calculation():
    """Test standard tuition computation without retakes."""
    result = tuition(credits=10, retake=0, rate=450_000, retake_multiplier=1.5, max_credits=30)
    assert result == 4_500_000


def test_tuition_with_retake_calculation():
    """Test standard tuition computation with retakes."""
    # 10 * 450,000 + 2 * 450,000 * 1.5 = 4,500,000 + 1,350,000 = 5,850,000
    result = tuition(credits=10, retake=2, rate=450_000, retake_multiplier=1.5, max_credits=30)
    assert result == 5_850_000


def test_tuition_minimum_boundary():
    """Test lower boundary: 1 credit."""
    result = tuition(credits=1, retake=0, rate=450_000, retake_multiplier=1.5, max_credits=30)
    assert result == 450_000


def test_tuition_maximum_boundary():
    """Test upper boundary: 30 credits."""
    result = tuition(credits=30, retake=0, rate=450_000, retake_multiplier=1.5, max_credits=30)
    assert result == 13_500_000


@pytest.mark.parametrize("invalid_credits", [0, -1, -10, 31, 35, 100])
def test_tuition_credits_out_of_bounds_raises(invalid_credits: int):
    """Test that credits < 1 or credits > max_credits raise InvalidRequest."""
    with pytest.raises(InvalidRequest, match="Credits must be between 1 and 30"):
        tuition(credits=invalid_credits, retake=0, rate=450_000, retake_multiplier=1.5, max_credits=30)


def test_tuition_negative_retake_raises():
    """Test that negative retake credits raise InvalidRequest."""
    with pytest.raises(InvalidRequest, match="Retake credits cannot be negative"):
        tuition(credits=15, retake=-1, rate=450_000, retake_multiplier=1.5, max_credits=30)


def test_tuition_large_retake_calculation():
    """Verify that very large retake counts compute deterministically without error."""
    # 15 * 450,000 + 100 * 450,000 * 1.5 = 6,750,000 + 67,500,000 = 74,250,000
    result = tuition(credits=15, retake=100, rate=450_000, retake_multiplier=1.5, max_credits=30)
    assert result == 74_250_000


def test_tuition_custom_settings():
    """Verify that tuition correctly accepts custom rate and maximum settings."""
    # Custom rate: 500,000, custom limit: 40
    result = tuition(credits=35, retake=5, rate=500_000, retake_multiplier=2.0, max_credits=40)
    # 35 * 500,000 + 5 * 500,000 * 2.0 = 17,500,000 + 5,000,000 = 22,500,000
    assert result == 22_500_000


def test_tuition_pure_function_deterministic():
    """Verify that function is purely deterministic with no side effects or mutations."""
    res1 = tuition(credits=15, retake=2, rate=450_000, retake_multiplier=1.5, max_credits=30)
    res2 = tuition(credits=15, retake=2, rate=450_000, retake_multiplier=1.5, max_credits=30)
    res3 = tuition(credits=15, retake=2, rate=450_000, retake_multiplier=1.5, max_credits=30)
    assert res1 == res2 == res3 == 8_100_000
