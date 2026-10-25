"""Deterministic fee and credit tools for the study assistant.

Pure, side-effect-free arithmetic calculations for student tuition and credit parsing.
Never relies on non-deterministic LLM providers or network I/O.
"""

from __future__ import annotations

import re

from assistant_core.errors import InvalidRequest


def parse_credits(text: str) -> tuple[int, int]:
    """Extract (credits, retake_credits) from student queries.

    Args:
        text: Raw user query string (e.g., 'tuition for 18 credits and 2 retake').

    Returns:
        tuple[int, int]: Tuple of (registered_credits, retake_credits).

    Raises:
        InvalidRequest: If no credit count is found or credits count is zero.
    """
    retake_match = re.search(r"(\d+)\s*retake", text, re.IGNORECASE)
    retake_credits = int(retake_match.group(1)) if retake_match else 0

    numbers = [int(n) for n in re.findall(r"\d+", text)]
    if retake_match and retake_credits in numbers:
        numbers.remove(retake_credits)

    if not numbers or numbers[0] == 0:
        raise InvalidRequest("How many credits?")

    return numbers[0], retake_credits


def tuition(
    credits: int,
    retake: int = 0,
    rate: int = 450_000,
    retake_multiplier: float = 1.5,
    max_credits: int = 30,
) -> int:
    """Calculate tuition amount deterministically.

    Args:
        credits: Total enrolled credits.
        retake: Number of credits being retaken.
        rate: Standard tuition cost per credit in VND (default: 450,000 VND).
        retake_multiplier: Fee multiplier for retake credits (default: 1.5x).
        max_credits: Maximum credit limit per semester (default: 30).

    Returns:
        Total calculated tuition in VND as an integer.

    Raises:
        InvalidRequest: If credits is outside [1, max_credits] or retake is negative.
    """
    if not (1 <= credits <= max_credits):
        raise InvalidRequest(f"Credits must be between 1 and {max_credits}.")

    if retake < 0:
        raise InvalidRequest("Retake credits cannot be negative.")

    total = credits * rate + retake * rate * retake_multiplier
    return int(total)
