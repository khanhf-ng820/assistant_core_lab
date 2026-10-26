"""Shared pytest fixtures for assistant_core tests."""

from pathlib import Path

import pytest

from assistant_core.models import Message


@pytest.fixture
def data_dir() -> Path:
    """Return the project's sample data directory."""
    return Path(__file__).resolve().parents[1] / "data"


@pytest.fixture
def sample_message() -> Message:
    """Provide a valid user message for testing."""
    return Message(text="Hello", session_id="test-session")


@pytest.fixture
def offices(data_dir: Path):
    """Provide an office directory loaded from sample data."""
    from assistant_core.knowledge import OfficeDirectory

    return OfficeDirectory.from_csv(data_dir / "offices.csv")


@pytest.fixture
def handbook(data_dir: Path):
    """Provide handbook rules loaded from sample data."""
    from assistant_core.knowledge import Handbook

    return Handbook.from_json(data_dir / "handbook.json")


@pytest.fixture
def service(data_dir: Path, offices, handbook):
    """Provide an assistant service with a deterministic stub responder."""
    from assistant_core.config import Settings
    from assistant_core.responder import StubLLMResponder
    from assistant_core.service import AssistantService

    settings = Settings(data_dir=data_dir)
    responder = StubLLMResponder(fail=False)

    return AssistantService(
        settings=settings,
        offices=offices,
        handbook=handbook,
        responder=responder,
    )
