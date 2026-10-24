"""Configuration contract from Lab 3, including safe credential output."""

import traceback
from pathlib import Path

import pytest
from pydantic import ValidationError

from assistant_core.config import Settings, load_settings
from assistant_core.errors import ConfigError

ENV_NAMES = (
    "ASSISTANT_DATA_DIR",
    "LLM_PROVIDER",
    "LLM_API_KEY",
    "CREDIT_RATE_VND",
    "RETAKE_MULTIPLIER",
    "MAX_CREDITS",
    "LOG_LEVEL",
)


@pytest.fixture(autouse=True)
def isolated_environment(monkeypatch):
    for name in ENV_NAMES:
        # Record every key so dotenv additions are also undone after each test.
        monkeypatch.setenv(name, "")
        monkeypatch.delenv(name)


def test_defaults_work_offline_without_env_file(tmp_path):
    settings = load_settings(str(tmp_path / "missing.env"))

    assert settings.data_dir == Path("data")
    assert settings.llm_provider == "stub"
    assert settings.llm_api_key is None
    assert settings.credit_rate_vnd == 450_000
    assert settings.retake_multiplier == 1.5
    assert settings.max_credits == 30
    assert settings.log_level == "INFO"


def test_environment_values_are_loaded_and_converted(monkeypatch, tmp_path):
    values = {
        "ASSISTANT_DATA_DIR": str(tmp_path / "knowledge"),
        "LLM_PROVIDER": "example-provider",
        "LLM_API_KEY": "test-only-key",
        "CREDIT_RATE_VND": "600000",
        "RETAKE_MULTIPLIER": "2.25",
        "MAX_CREDITS": "24",
        "LOG_LEVEL": "DEBUG",
    }
    for name, value in values.items():
        monkeypatch.setenv(name, value)

    settings = load_settings(None)

    assert settings.data_dir == tmp_path / "knowledge"
    assert settings.llm_provider == "example-provider"
    assert settings.llm_api_key == "test-only-key"
    assert settings.credit_rate_vnd == 600_000
    assert settings.retake_multiplier == 2.25
    assert settings.max_credits == 24
    assert settings.log_level == "DEBUG"


def test_default_dotenv_is_loaded_without_overriding_shell(monkeypatch, tmp_path):
    (tmp_path / ".env").write_text(
        "CREDIT_RATE_VND=500000\nMAX_CREDITS=22\nLLM_PROVIDER=example-provider\nLLM_API_KEY=test-file-key\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("CREDIT_RATE_VND", "700000")

    settings = load_settings()

    assert settings.credit_rate_vnd == 700_000
    assert settings.max_credits == 22
    assert settings.llm_provider == "example-provider"
    assert settings.llm_api_key == "test-file-key"


def test_explicit_dotenv_path_is_used(tmp_path):
    env_file = tmp_path / "custom.env"
    env_file.write_text("MAX_CREDITS=18\n", encoding="utf-8")

    assert load_settings(str(env_file)).max_credits == 18


def test_none_skips_dotenv_loading(monkeypatch, tmp_path):
    (tmp_path / ".env").write_text("MAX_CREDITS=10\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    assert load_settings(None).max_credits == 30


def test_empty_key_is_optional_in_stub_mode(monkeypatch):
    monkeypatch.setenv("LLM_API_KEY", "")

    assert load_settings(None).llm_api_key is None


@pytest.mark.parametrize("key", [None, ""])
def test_other_providers_require_a_key(monkeypatch, key):
    monkeypatch.setenv("LLM_PROVIDER", "example-provider")
    if key is not None:
        monkeypatch.setenv("LLM_API_KEY", key)

    with pytest.raises(ConfigError, match="LLM_API_KEY is required"):
        load_settings(None)


@pytest.mark.parametrize("name", ["CREDIT_RATE_VND", "RETAKE_MULTIPLIER", "MAX_CREDITS"])
def test_invalid_numeric_settings_raise_safe_config_error(monkeypatch, name):
    secret = "test-only-sensitive-value"
    monkeypatch.setenv(name, secret)
    monkeypatch.setenv("LLM_API_KEY", secret)

    with pytest.raises(ConfigError) as caught:
        load_settings(None)

    assert name.lower() in str(caught.value)
    assert secret not in "".join(traceback.format_exception(caught.value))


def test_api_key_is_hidden_from_settings_output(capsys):
    settings = Settings(llm_api_key="test-only-sensitive-value")
    print(settings)

    assert settings.llm_api_key == "test-only-sensitive-value"
    assert "test-only-sensitive-value" not in capsys.readouterr().out
    assert "test-only-sensitive-value" not in repr(settings)


def test_direct_validation_error_hides_input_values():
    with pytest.raises(ValidationError) as caught:
        Settings(llm_api_key=["test-only-sensitive-value"])

    assert "test-only-sensitive-value" not in str(caught.value)


def test_example_env_matches_documented_defaults():
    env_file = Path(__file__).resolve().parents[1] / ".env.example"

    assert load_settings(str(env_file)) == Settings()
