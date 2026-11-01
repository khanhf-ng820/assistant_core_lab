"""Fixtures scoped only to the new Week 4 tests."""

import pytest

from assistant_api.config import REPO_ROOT, APISettings
from assistant_core import AssistantService


@pytest.fixture(autouse=True)
def isolated_api_environment(monkeypatch):
    keys = (
        "ASSISTANT_DATA_DIR",
        "LLM_PROVIDER",
        "LLM_API_KEY",
        "CREDIT_RATE_VND",
        "RETAKE_MULTIPLIER",
        "MAX_CREDITS",
        "LOG_LEVEL",
        "API_ADMIN_KEY",
        "WEATHER_URL",
        "WEATHER_TIMEOUT_S",
        "CAMPUS_LAT",
        "CAMPUS_LON",
        "RATE_LIMIT_PER_MIN",
    )
    for key in keys:
        monkeypatch.setenv(key, "")
        monkeypatch.delenv(key)


@pytest.fixture
def settings():
    return APISettings(data_dir=REPO_ROOT / "data")


@pytest.fixture
def service(settings):
    return AssistantService.default(settings=settings)
