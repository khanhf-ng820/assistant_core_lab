"""Smoke tests for the refactored ``assistant_core`` package.

These replace the Lab-2 tests that imported the removed ``assistant.rules``
module. They exercise the public service against the sample data in ``data/``.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from assistant_core.__main__ import execute_query
from assistant_core.service import AssistantService, Intent, Message, OfficeDirectory

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"


@pytest.fixture(scope="module")
def service() -> AssistantService:
    return AssistantService.default(data_dir=DATA_DIR)


def test_greeting(service: AssistantService) -> None:
    response = service.handle(Message(text="hi"))
    assert response.intent is Intent.GREETING
    assert "Hello" in response.answer


def test_office_lookup(service: AssistantService) -> None:
    response = service.handle(Message(text="Where is the Training Office?"))
    assert response.intent is Intent.OFFICE
    assert "I.101" in response.answer

def test_international_office_lookup(extra_offices):
    assert "F.203" in reply("When does the International Office open?", offices=extra_offices)

def test_library_lookup_is_case_insensitive(service: AssistantService) -> None:
    response = service.handle(Message(text="WHERE IS THE LIBRARY?"))
    assert "Library" in response.answer
    assert "B.201" in response.answer
    assert "Mon-Sat 07:00-20:00" in response.answer


def test_office_lookup_with_punctuation(service: AssistantService) -> None:
    response = service.handle(Message(text="Where is Student Affairs?!"))
    assert "Student Affairs" in response.answer
    assert "I.102" in response.answer


def test_unknown_question(service: AssistantService) -> None:
    response = service.handle(Message(text="what is the meaning of life"))
    assert response.intent is Intent.UNKNOWN
    assert "don't know" in response.answer


def test_empty_message_is_rejected_at_the_boundary() -> None:
    with pytest.raises(ValueError):
        Message(text="")


def test_cli_returns_a_friendly_answer_for_empty_input(service: AssistantService) -> None:
    assert execute_query(service, "   ") == "Please type a question."


def test_load_offices_csv() -> None:
    offices = OfficeDirectory.from_csv(DATA_DIR / "offices.csv")

    assert "training office" in offices.names
    office = offices.find("where is the training office?")
    assert office is not None
    assert office.room == "I.101"
    assert office.hours == "Mon-Fri 07:30-16:30"


def test_office_csv_required_fields() -> None:
    offices = OfficeDirectory.from_csv(DATA_DIR / "offices.csv")

    assert offices.names
    for name in offices.names:
        office = offices.find(name)
        assert office is not None
        assert office.name.strip()
        assert office.room.strip()
        assert office.hours.strip()
