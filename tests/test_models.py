"""Unit tests for assistant_core Pydantic models."""

import pytest
from pydantic import ValidationError

from assistant_core.models import Intent, Message, Response, Source


def test_message_valid():
    msg = Message(text="Hello")

    assert msg.text == "Hello"
    assert msg.session_id == "local"


def test_message_custom_session():
    msg = Message(text="Hello", session_id="test-123")

    assert msg.session_id == "test-123"


def test_message_empty_text():
    with pytest.raises(ValidationError):
        Message(text="")


def test_message_text_length():
    assert len(Message(text="a" * 2000).text) == 2000

    with pytest.raises(ValidationError):
        Message(text="a" * 2001)


def test_response_defaults():
    response = Response(
        answer="Hello!",
        intent=Intent.GREETING,
    )

    assert response.sources == []
    assert response.degraded is False


def test_response_with_source():
    source = Source(id="H26-5.3", title="Thesis registration")

    response = Response(
        answer="You need 120 credits.",
        intent=Intent.RULE,
        sources=[source],
    )

    assert response.sources[0].id == "H26-5.3"


def test_response_sources_are_independent():
    first = Response(answer="First", intent=Intent.RULE)
    second = Response(answer="Second", intent=Intent.RULE)

    first.sources.append(Source(id="1", title="Test"))

    assert second.sources == []
