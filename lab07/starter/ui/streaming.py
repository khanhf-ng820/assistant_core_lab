"""Client-side streaming helpers for the Streamlit chat UI."""

from __future__ import annotations

from collections.abc import Iterator


def stream_text(text: str, chunk_size: int = 8) -> Iterator[str]:
    """Yield fixed-size slices of text for st.write_stream."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    for i in range(0, len(text), chunk_size):
        yield text[i : i + chunk_size]


def should_stream_message(index: int, role: str, total_messages: int, streamed_up_to: int) -> bool:
    """Return True only for an unstreamed newest assistant message."""
    return role == "assistant" and index == total_messages - 1 and index > streamed_up_to
