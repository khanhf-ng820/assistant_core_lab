"""Unit tests for the help feature extension (Lab 3 - H1)."""

from __future__ import annotations

import logging

import pytest

from assistant_core.__main__ import execute_query
from assistant_core.models import Intent, Message
from assistant_core.router import route
from assistant_core.service import (
    AssistantService,
    Handbook,
    Office,
    OfficeDirectory,
    Rule,
    StubLLMResponder,
)


class MockSettings:
    credit_rate_vnd = 450_000
    retake_multiplier = 1.5
    max_credits = 30
    log_level = "INFO"


def make_service() -> AssistantService:
    settings = MockSettings()
    offices = OfficeDirectory(
        {
            "training office": Office("Training Office", "I.101", "Mon-Fri 07:30-16:30"),
            "library": Office("Library", "B.201", "Mon-Sat 07:00-20:00"),
        }
    )
    handbook = Handbook(
        [
            Rule("H26-5.3", "Thesis Registration", "Students must have completed at least 120 credits to register."),
        ]
    )
    responder = StubLLMResponder()
    return AssistantService(
        settings=settings,
        offices=offices,
        handbook=handbook,
        responder=responder,
    )


def test_route_help() -> None:
    """Verify route accurately classifies help keywords and handles punctuation."""
    office_names = {"training office", "library"}
    assert route("help", office_names) == Intent.HELP
    assert route("HELP?!", office_names) == Intent.HELP
    assert route("tro giup", office_names) == Intent.HELP
    assert route("huong dan", office_names) == Intent.HELP
    assert route("support", office_names) == Intent.HELP
    assert route("help me", office_names) == Intent.HELP
    # Compound query with domain keywords should route to specific intent instead of being hijacked
    assert route("help me calculate tuition for 18 credits", office_names) == Intent.FEE


def test_service_handle_help() -> None:
    """Verify AssistantService returns guidance and correct intent for help query."""
    service = make_service()
    resp = service.handle(Message(text="help"))

    assert resp.intent == Intent.HELP
    assert "campus offices" in resp.answer
    assert "tuition fees" in resp.answer
    assert "academic rules" in resp.answer
    assert resp.sources == []
    assert not resp.degraded


def test_service_handle_vietnamese_help() -> None:
    """Verify AssistantService responds to Vietnamese help trigger."""
    service = make_service()
    resp = service.handle(Message(text="tro giup"))

    assert resp.intent == Intent.HELP
    assert resp.answer != ""
    assert not resp.degraded


def test_cli_help_structured_log(caplog: pytest.LogCaptureFixture) -> None:
    """Verify CLI execute_query logs structured JSON extra fields for help."""
    service = make_service()
    caplog.set_level(logging.INFO, logger="assistant_core")

    answer = execute_query(service, "help", session_id="test-help-session")

    assert "campus offices" in answer
    matching_records = [
        record
        for record in caplog.records
        if getattr(record, "intent", None) == "help" and getattr(record, "session", None) == "test-help-session"
    ]
    assert len(matching_records) == 1
    rec = matching_records[0]
    assert rec.msg == "handled"
    assert rec.degraded is False
    assert hasattr(rec, "latency_ms")
