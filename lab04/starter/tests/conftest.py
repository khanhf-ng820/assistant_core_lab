import pytest
from assistant_api.config import REPO_ROOT, APISettings

from assistant_core import AssistantService


@pytest.fixture
def settings():
    return APISettings(data_dir=REPO_ROOT / "data")


@pytest.fixture
def service(settings):
    return AssistantService.default(settings=settings)
