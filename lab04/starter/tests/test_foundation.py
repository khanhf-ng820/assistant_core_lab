"""Foundation checks deliberately avoid the still-unimplemented T1-T4 routes."""

from pathlib import Path

import pytest
from assistant_api.config import REPO_ROOT, APISettings, load_api_settings
from assistant_api.main import create_app
from fastapi.testclient import TestClient

import assistant_core
from assistant_core.errors import ConfigError


@pytest.mark.parametrize("directory", [".", "lab04/starter"])
def test_default_startup_from_both_directories(monkeypatch, directory):
    monkeypatch.chdir(REPO_ROOT / directory)
    monkeypatch.setenv("ASSISTANT_DATA_DIR", "data")
    client = TestClient(create_app())
    assert client.get("/health").json() == {"status": "ok", "version": "1.0.0"}
    assert client.get("/docs").status_code == 200
    assert "/v1/chat" in client.get("/openapi.json").json()["paths"]
    assert Path(assistant_core.__file__).resolve().parent == REPO_ROOT / "src/assistant_core"


def test_configuration_precedence_and_secret_redaction(monkeypatch, tmp_path):
    dotenv = tmp_path / ".env"
    dotenv.write_text("API_ADMIN_KEY=dotenv-placeholder\nWEATHER_TIMEOUT_S=4\n")
    monkeypatch.setenv("API_ADMIN_KEY", "shell-placeholder")
    monkeypatch.delenv("WEATHER_TIMEOUT_S", raising=False)
    settings = load_api_settings(str(dotenv))
    assert settings.api_admin_key == "shell-placeholder"
    assert settings.weather_timeout_s == 4
    assert "shell-placeholder" not in repr(settings)
    monkeypatch.setenv("WEATHER_TIMEOUT_S", "sensitive-invalid-value")
    with pytest.raises(ConfigError) as exc:
        load_api_settings(None)
    assert "weather_timeout_s" in str(exc.value)
    assert "sensitive-invalid-value" not in str(exc.value)


def test_injected_service_bypasses_data_loading(settings, service):
    settings = settings.model_copy(update={"data_dir": Path("missing-data")})
    assert TestClient(create_app(settings, service)).get("/health").status_code == 200


@pytest.mark.parametrize("key", [None, "wrong-placeholder"])
def test_admin_rejects_missing_or_wrong_key(key):
    client = TestClient(create_app(APISettings(api_admin_key="test-placeholder")))
    response = client.get("/v1/feedback", headers={} if key is None else {"X-API-Key": key})
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "missing_or_invalid_api_key"


def test_validation_and_routing_errors():
    client = TestClient(create_app())
    assert client.post("/v1/chat", json={"message": ""}).json()["error"]["code"] == "invalid_request"
    response = client.get("/v1/nope")
    assert response.status_code == 404
    assert response.json() == {"error": {"code": "not_found", "message": "Not Found"}}


def test_feedback_store_is_per_app():
    first, second = create_app(), create_app()
    first.state.feedback_store.append("sentinel")
    assert second.state.feedback_store == []
