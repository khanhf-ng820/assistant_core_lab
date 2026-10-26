"""Tests for the help command."""

from pathlib import Path

import pytest

from assistant_core.service import AssistantService, Intent, Message

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


@pytest.fixture(scope="module")
def service() -> AssistantService:
    return AssistantService.default(data_dir=DATA_DIR)


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
    assert "office locations" not in response.answer
