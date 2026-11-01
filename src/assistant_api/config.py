"""API settings layered on the single root core configuration."""

import os
from pathlib import Path

from pydantic import Field, ValidationError

import assistant_core
from assistant_core.config import Settings, load_settings
from assistant_core.errors import ConfigError

REPO_ROOT = Path(assistant_core.__file__).resolve().parents[2]


class APISettings(Settings):
    api_admin_key: str | None = Field(default=None, repr=False)
    weather_url: str = "https://api.open-meteo.com/v1/forecast"
    weather_timeout_s: float = Field(default=3.0, gt=0)
    campus_lat: float = Field(default=10.7626, ge=-90, le=90)
    campus_lon: float = Field(default=106.6822, ge=-180, le=180)
    rate_limit_per_min: int = Field(default=30, gt=0)


def load_api_settings(env_file: str | None = ".env") -> APISettings:
    base = load_settings(env_file)
    fields = ("api_admin_key", "weather_url", "weather_timeout_s", "campus_lat", "campus_lon", "rate_limit_per_min")
    values = {field: os.environ[field.upper()] for field in fields if field.upper() in os.environ}
    if values.get("api_admin_key") == "":
        values["api_admin_key"] = None
    try:
        return APISettings(**base.model_dump(), **values)
    except ValidationError as exc:
        invalid = sorted({str(e["loc"][0]) for e in exc.errors(include_input=False)})
        raise ConfigError(f"Invalid API configuration for: {', '.join(invalid)}.") from None


def resolve_data_dir(settings: APISettings) -> Path:
    return settings.data_dir if settings.data_dir.is_absolute() else REPO_ROOT / settings.data_dir
