"""Tests for the help command."""

from assistant_core.models import Message
from assistant_core.service import AssistantService, Intent


def test_help_exact_match(service: AssistantService) -> None:
    response = service.handle(Message(text="help"))
    assert response.intent is Intent.GREETING
    assert "office locations" in response.answer


def test_help_with_punctuation(service: AssistantService) -> None:
    response = service.handle(Message(text="Help?!"))
    assert response.intent is Intent.GREETING
    assert "office locations" in response.answer


def test_help_does_not_hijack_questions(service: AssistantService) -> None:
    response = service.handle(Message(text="I need help with fees"))
    assert response.intent is not Intent.GREETING or "office locations" not in response.answer
