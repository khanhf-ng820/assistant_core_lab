"""Structured logging setup for assistant_core.

Provides JsonFormatter to emit machine-readable JSON logs to stderr,
ensuring application logs can be analyzed while preventing leakage of
API keys or sensitive raw user messages.
"""

from __future__ import annotations

import json
import logging
import sys
from typing import TextIO

STRUCTURED_FIELDS = ("intent", "latency_ms", "session", "degraded")
SENSITIVE_KEYS = ("api_key", "llm_api_key", "secret", "password", "token")


class JsonFormatter(logging.Formatter):
    """Formats log records as structured JSON strings."""

    def format(self, record: logging.LogRecord) -> str:
        data: dict[str, object] = {
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }

        # Include recognized structured context attributes
        for key in STRUCTURED_FIELDS:
            if hasattr(record, key):
                data[key] = getattr(record, key)

        # Sanitize any accidental sensitive fields
        for sensitive in SENSITIVE_KEYS:
            data.pop(sensitive, None)

        return json.dumps(data, ensure_ascii=False)


def setup_logging(level: str = "INFO", stream: TextIO | None = None) -> logging.Logger:
    """Configure structured JSON logging for the assistant_core logger.

    Args:
        level: Logging severity level (e.g., 'DEBUG', 'INFO', 'WARNING').
        stream: Output stream, defaults to sys.stderr.

    Returns:
        The configured assistant_core logger instance.
    """
    out_stream = sys.stderr if stream is None else stream
    handler = logging.StreamHandler(out_stream)
    handler.setFormatter(JsonFormatter())

    core_logger = logging.getLogger("assistant_core")
    core_logger.handlers.clear()
    core_logger.addHandler(handler)
    core_logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    core_logger.propagate = True

    return core_logger


def setup_cli_logging(level: str = "INFO") -> None:
    """Convenience alias to configure structured logging to stderr for CLI."""
    setup_logging(level=level, stream=sys.stderr)
