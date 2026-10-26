"""Load typed settings from the environment without exposing credentials."""

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from assistant_core.errors import ConfigError


class Settings(BaseModel):
    """Runtime configuration; API keys are hidden from str/repr output."""

    model_config = ConfigDict(hide_input_in_errors=True)

    data_dir: Path = Path("data")
    llm_provider: str = "stub"
    llm_api_key: str | None = Field(default=None, repr=False)
    credit_rate_vnd: int = 450_000
    retake_multiplier: float = 1.5
    max_credits: int = 30
    log_level: str = "INFO"


def load_settings(env_file: str | None = ".env") -> Settings:
    """Read optional dotenv settings; existing shell variables take priority.

    Pass None to read only the process environment. Invalid configuration
    raises ConfigError without echoing environment values or credentials.
    """
    if env_file:
        load_dotenv(env_file, override=False)

    try:
        settings = Settings(
            data_dir=os.getenv("ASSISTANT_DATA_DIR", "data"),
            llm_provider=os.getenv("LLM_PROVIDER", "stub"),
            llm_api_key=os.getenv("LLM_API_KEY") or None,
            credit_rate_vnd=os.getenv("CREDIT_RATE_VND", "450000"),
            retake_multiplier=os.getenv("RETAKE_MULTIPLIER", "1.5"),
            max_credits=os.getenv("MAX_CREDITS", "30"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )
    except ValidationError as exc:
        fields = sorted({str(error["loc"][0]) for error in exc.errors(include_input=False)})
        raise ConfigError(f"Invalid configuration for: {', '.join(fields)}.") from None

    if settings.llm_provider != "stub" and not settings.llm_api_key:
        raise ConfigError("LLM_API_KEY is required when LLM_PROVIDER is not 'stub'.")

    return settings
