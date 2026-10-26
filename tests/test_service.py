"""Tests for AssistantService, with a focus on responder injection and failure.

Lab 3 / Trần Thành Lợi (AI-Integration). The important scenarios are:

* the service answers through the responder it was given (dependency injection);
* a ``ProviderError`` never reaches the caller -- the template fallback answers
  and ``Response.degraded`` is ``True``;
* the fallback keeps the handbook citation;
* failures are logged without the API key or the user's full message;
* a genuine programming bug is *not* hidden by a blind ``except Exception``.
"""

from __future__ import annotations

import logging
from pathlib import Path

import pytest
from pydantic import ValidationError

from assistant_core.__main__ import execute_query, main
from assistant_core.responder import Responder, StubLLMResponder, TemplateResponder
from assistant_core.service import (
    AssistantService,
    Handbook,
    Intent,
    Message,
    Office,
    OfficeDirectory,
    ProviderError,
    Rule,
)

THESIS_RULE = Rule(
    id="H26-5.3",
    title="Thesis registration",
    text="Students may register a thesis with at least 120 credits.",
)
RETAKE_RULE = Rule(
    id="H26-4.2",
    title="Retaking a course",
    text="Retake credits are charged at 1.5 times the normal rate.",
)
THESIS_QUESTION = "thesis registration credits"


class MockSettings:
    """Minimal settings object; the service only reads these attributes."""

    credit_rate_vnd = 450_000
    retake_multiplier = 1.5
    max_credits = 30
    log_level = "INFO"


def make_service(responder: Responder | None = None) -> AssistantService:
    """Build a service with in-memory knowledge -- no files, network or API key."""
    offices = OfficeDirectory(
        {
            "training office": Office("Training Office", "I.101", "Mon-Fri 07:30-16:30"),
            "library": Office("Library", "B.201", "Mon-Sat 07:00-20:00"),
        }
    )
    handbook = Handbook([THESIS_RULE, RETAKE_RULE])
    return AssistantService(
        settings=MockSettings(),
        offices=offices,
        handbook=handbook,
        responder=responder or StubLLMResponder(),
    )


@pytest.fixture
def service() -> AssistantService:
    return make_service()


# ---------------------------------------------------------------------------
# Responder implementations
# ---------------------------------------------------------------------------


def test_stub_responder_returns_rule_grounded_answer() -> None:
    answer = StubLLMResponder().explain(THESIS_QUESTION, THESIS_RULE)
    assert answer == f"Based on '{THESIS_RULE.title}': {THESIS_RULE.text}"


def test_stub_responder_can_simulate_provider_failure() -> None:
    with pytest.raises(ProviderError, match="unavailable"):
        StubLLMResponder(fail=True).explain(THESIS_QUESTION, THESIS_RULE)


def test_template_responder_is_deterministic_and_needs_no_provider() -> None:
    responder = TemplateResponder()
    first = responder.explain(THESIS_QUESTION, THESIS_RULE)
    second = responder.explain(THESIS_QUESTION, THESIS_RULE)
    assert first == second == f"{THESIS_RULE.title}: {THESIS_RULE.text}"


def test_both_responders_satisfy_the_protocol() -> None:
    assert isinstance(StubLLMResponder(), Responder)
    assert isinstance(TemplateResponder(), Responder)


def test_service_reexports_responders_for_backward_compatibility() -> None:
    from assistant_core.service import StubLLMResponder as ServiceStub
    from assistant_core.service import TemplateResponder as ServiceTemplate

    assert ServiceStub is StubLLMResponder
    assert ServiceTemplate is TemplateResponder


# ---------------------------------------------------------------------------
# Service behaviour while the provider is healthy
# ---------------------------------------------------------------------------


def test_greeting(service: AssistantService) -> None:
    response = service.handle(Message(text="hello!"))
    assert response.intent is Intent.GREETING
    assert "Hello" in response.answer
    assert response.sources == []
    assert response.degraded is False


def test_office_lookup(service: AssistantService) -> None:
    response = service.handle(Message(text="Where is the Training Office?"))
    assert response.intent is Intent.OFFICE
    assert "I.101" in response.answer
    assert response.sources == []
    assert response.degraded is False


def test_fee_calculation(service: AssistantService) -> None:
    response = service.handle(Message(text="tuition for 18 credits and 2 retake"))
    assert response.intent is Intent.FEE
    assert response.answer == "Your tuition is 9,450,000 VND."
    assert response.degraded is False


def test_fee_invalid_credits(service: AssistantService) -> None:
    response = service.handle(Message(text="fee for 35 credits"))
    assert response.intent is Intent.FEE
    assert "between 1 and 30" in response.answer


def test_rule_answer_is_not_degraded_and_cites_the_source(service: AssistantService) -> None:
    response = service.handle(Message(text=THESIS_QUESTION))
    assert response.intent is Intent.RULE
    assert response.degraded is False
    assert [source.id for source in response.sources] == ["H26-5.3"]
    assert response.answer.startswith("Based on 'Thesis registration':")


def test_unknown_rule_is_not_sent_to_the_responder() -> None:
    class RecordingResponder:
        def __init__(self) -> None:
            self.calls = 0

        def explain(self, question: str, rule: Rule) -> str:
            self.calls += 1
            return "should not be called"

    responder = RecordingResponder()
    service = make_service(responder)

    response = service.handle(Message(text="quantum entanglement"))

    assert response.intent is Intent.UNKNOWN
    assert "Sorry" in response.answer
    assert responder.calls == 0
    assert response.degraded is False


def test_injected_responder_can_be_swapped_without_editing_the_service(service: AssistantService) -> None:
    class CustomResponder:
        def explain(self, question: str, rule: Rule) -> str:
            return "custom answer"

    service.responder = CustomResponder()

    response = service.handle(Message(text=THESIS_QUESTION))

    assert response.answer == "custom answer"
    assert response.degraded is False
    assert response.sources[0].id == "H26-5.3"


# ---------------------------------------------------------------------------
# AI failure scenarios -- the fallback path
# ---------------------------------------------------------------------------


def test_fallback_when_provider_fails(service: AssistantService) -> None:
    service.responder = StubLLMResponder(fail=True)

    response = service.handle(Message(text=THESIS_QUESTION))

    assert response.intent is Intent.RULE
    assert response.degraded is True
    assert response.answer == f"{THESIS_RULE.title}: {THESIS_RULE.text}"


def test_fallback_preserves_the_handbook_citation(service: AssistantService) -> None:
    service.responder = StubLLMResponder(fail=True)

    response = service.handle(Message(text=THESIS_QUESTION))

    assert len(response.sources) == 1
    assert response.sources[0].id == "H26-5.3"
    assert response.sources[0].title == "Thesis registration"


def test_fallback_uses_the_template_responder(service: AssistantService) -> None:
    assert isinstance(service.fallback, TemplateResponder)

    service.responder = StubLLMResponder(fail=True)
    response = service.handle(Message(text=THESIS_QUESTION))

    assert response.answer == service.fallback.explain(THESIS_QUESTION, THESIS_RULE)


def test_provider_failure_is_logged_without_secrets_or_user_message(
    service: AssistantService,
    caplog: pytest.LogCaptureFixture,
) -> None:
    service.settings.llm_api_key = "sk-do-not-log-this"
    service.responder = StubLLMResponder(fail=True)

    with caplog.at_level(logging.WARNING, logger="assistant_core"):
        service.handle(Message(text=THESIS_QUESTION))

    assert "provider failed; using template fallback" in caplog.text
    assert "sk-do-not-log-this" not in caplog.text
    assert THESIS_QUESTION not in caplog.text


def test_unexpected_programming_errors_are_not_hidden(service: AssistantService) -> None:
    class BuggyResponder:
        def explain(self, question: str, rule: Rule) -> str:
            raise RuntimeError("a real bug")

    service.responder = BuggyResponder()

    # Only ProviderError is a provider outage; other errors must surface.
    with pytest.raises(RuntimeError, match="a real bug"):
        service.handle(Message(text=THESIS_QUESTION))


# ---------------------------------------------------------------------------
# Boundary validation and end-to-end wiring
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("text", ["", "x" * 2001])
def test_message_validation_rejects_empty_or_oversized_text(text: str) -> None:
    with pytest.raises(ValidationError):
        Message(text=text)


def test_default_service_loads_the_repository_data() -> None:
    repo_data = Path(__file__).resolve().parents[1] / "data"
    service = AssistantService.default(data_dir=repo_data)

    office_response = service.handle(Message(text="Where is the Training Office?"))
    rule_response = service.handle(Message(text="exam absence medical evidence deadline"))

    assert "I.101" in office_response.answer
    assert rule_response.intent is Intent.RULE
    assert rule_response.sources[0].id == "H26-7.2"
    assert rule_response.degraded is False


def test_execute_query_returns_the_answer(service: AssistantService) -> None:
    assert "Hello" in execute_query(service, "hi", session_id="test-session")


def test_cli_main_argument(capsys: pytest.CaptureFixture[str]) -> None:
    try:
        assert main(["hi"]) == 0
        assert "Hello" in capsys.readouterr().out
    finally:
        # main() configures a real stderr handler; remove it so later tests
        # (and caplog) are not affected by the global logging state.
        logger = logging.getLogger("assistant_core")
        logger.handlers.clear()
        logger.propagate = True
