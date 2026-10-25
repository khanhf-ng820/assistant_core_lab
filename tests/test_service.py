"""Unit tests for AssistantService and CLI in assistant_core."""

from pathlib import Path

import pytest

from assistant_core.__main__ import execute_query, main
from assistant_core.service import (
    AssistantService,
    DataError,
    Handbook,
    Intent,
    Message,
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
            Rule("H26-2.1", "Tuition Deadline", "Tuition must be settled within the first two weeks of semester."),
        ]
    )
    responder = StubLLMResponder()
    return AssistantService(
        settings=settings,
        offices=offices,
        handbook=handbook,
        responder=responder,
    )


def test_greeting():
    service = make_service()
    resp = service.handle(Message(text="hello!"))
    assert resp.intent == Intent.GREETING
    assert "Hello" in resp.answer
    assert resp.sources == []
    assert not resp.degraded


def test_office_lookup():
    service = make_service()
    resp = service.handle(Message(text="Where is the Training Office?"))
    assert resp.intent == Intent.OFFICE
    assert "I.101" in resp.answer
    assert "07:30-16:30" in resp.answer


def test_office_unknown():
    service = make_service()
    resp = service.handle(Message(text="where is the astronomy lab?"))
    # When no office name matches, router classifies as rule; if no rule matches, returns UNKNOWN
    assert resp.intent == Intent.UNKNOWN
    assert "Sorry" in resp.answer


def test_fee_calculation():
    service = make_service()
    resp = service.handle(Message(text="tuition for 18 credits and 2 retake"))
    assert resp.intent == Intent.FEE
    # 18 * 450000 + 2 * 450000 * 1.5 = 8100000 + 1350000 = 9450000
    assert "9,450,000 VND" in resp.answer


def test_fee_invalid_credits():
    service = make_service()
    resp = service.handle(Message(text="fee for 35 credits"))
    assert resp.intent == Intent.FEE
    assert "Credits must be between 1 and 30" in resp.answer


def test_rule_search_success():
    service = make_service()
    resp = service.handle(Message(text="thesis registration requirement"))
    assert resp.intent == Intent.RULE
    assert len(resp.sources) == 1
    assert resp.sources[0].id == "H26-5.3"
    assert not resp.degraded
    assert "Thesis Registration" in resp.answer


def test_rule_search_unknown():
    service = make_service()
    resp = service.handle(Message(text="what is quantum entanglement?"))
    assert resp.intent == Intent.UNKNOWN
    assert "Sorry, I don't know that yet." in resp.answer


def test_fallback_when_provider_fails():
    """Verify that provider failure gracefully switches to TemplateResponder with degraded=True."""
    service = make_service()
    service.responder = StubLLMResponder(fail=True)

    resp = service.handle(Message(text="thesis registration credits"))
    assert resp.intent == Intent.RULE
    assert resp.degraded is True
    assert len(resp.sources) == 1
    assert resp.sources[0].id == "H26-5.3"
    assert "Thesis Registration" in resp.answer


def test_default_factory_with_repo_data():
    repo_data = Path(__file__).resolve().parents[1] / "data"
    service = AssistantService.default(data_dir=repo_data)
    assert service is not None

    resp = service.handle(Message(text="hi"))
    assert resp.intent == Intent.GREETING


def test_cli_execute_query():
    service = make_service()
    ans = execute_query(service, "hi")
    assert "Hello" in ans


def test_cli_main_argument(capsys):
    ret = main(["hi"])
    assert ret == 0
    captured = capsys.readouterr()
    assert "Hello" in captured.out


def test_default_factory_with_environment_credit_rate(monkeypatch):
    """Verify that AssistantService.default() loads environment settings such as CREDIT_RATE_VND."""
    monkeypatch.setenv("CREDIT_RATE_VND", "600000")
    service = AssistantService.default()
    resp = service.handle(Message(text="tuition for 10 credits"))
    assert resp.intent == Intent.FEE
    assert "Your tuition is 6,000,000 VND." in resp.answer


def test_default_factory_missing_offices_raises_data_error(tmp_path):
    """Verify that missing offices.csv raises DataError instead of silent empty directory."""
    with pytest.raises(DataError, match="office file not found"):
        AssistantService.default(data_dir=tmp_path)


def test_default_factory_missing_handbook_raises_data_error(tmp_path):
    """Verify that missing handbook.json raises DataError instead of silent empty handbook."""
    offices_csv = tmp_path / "offices.csv"
    offices_csv.write_text("name,room,hours\nLibrary,B.201,08:00-17:00\n", encoding="utf-8")
    with pytest.raises(DataError, match="handbook file not found"):
        AssistantService.default(data_dir=tmp_path)
