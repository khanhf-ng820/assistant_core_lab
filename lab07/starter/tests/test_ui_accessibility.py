"""Streamlit AppTest checks for Lab 7 UI accessibility, error states, and disclosure."""

from __future__ import annotations

from pathlib import Path

from streamlit.testing.v1 import AppTest

from ui.api_client import AssistantClient
from ui.logic import EXAMPLES, WELCOME

APP_PATH = str(Path(__file__).resolve().parents[1] / "ui" / "app.py")


def _run_app(monkeypatch, *, healthy: bool = True) -> AppTest:
    monkeypatch.setattr(AssistantClient, "healthy", lambda self: healthy)
    return AppTest.from_file(APP_PATH).run(timeout=10)


def test_initial_screen_shows_ai_notice_welcome_and_examples(monkeypatch):
    at = _run_app(monkeypatch, healthy=True)
    assert not at.error
    assert any("AI assistant" in c.value for c in at.caption)
    assert WELCOME in [m.value for m in at.markdown]
    sidebar_labels = [b.label for b in at.sidebar.button]
    for example in EXAMPLES:
        assert example in sidebar_labels


def test_backend_down_shows_friendly_error_banner(monkeypatch):
    at = _run_app(monkeypatch, healthy=False)
    assert len(at.error) == 1
    assert "not reachable" in at.error[0].value


def test_overlong_input_warns_without_calling_api(monkeypatch):
    def fail_ask(self, message: str, session_id: str):
        raise AssertionError("API should not be called for invalid input")

    monkeypatch.setattr(AssistantClient, "ask", fail_ask)
    at = _run_app(monkeypatch, healthy=True)
    at.chat_input[0].set_value("x" * 2001).run(timeout=10)
    assert len(at.warning) == 1
    assert "too long" in at.warning[0].value


def test_helpful_button_includes_text_tooltip(monkeypatch):
    monkeypatch.setattr(AssistantClient, "healthy", lambda self: True)
    at = AppTest.from_file(APP_PATH)
    at.session_state["messages"] = [
        {"role": "assistant", "content": WELCOME},
        {"role": "assistant", "content": "Room I.101", "request_id": "req-1"},
    ]
    at.session_state["streamed_up_to"] = 1
    at.run(timeout=10)
    thumbs_up = [b for b in at.button if b.label == "👍"]
    assert len(thumbs_up) == 1
    assert thumbs_up[0].help == "Helpful"
