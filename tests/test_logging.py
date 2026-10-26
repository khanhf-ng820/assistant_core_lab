"""Unit tests for structured JSON logging in assistant_core."""

from __future__ import annotations

import io
import json
import logging
import sys

from assistant_core.logging_setup import JsonFormatter, setup_cli_logging, setup_logging


def test_json_formatter_standard_fields() -> None:
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="assistant_core",
        level=logging.INFO,
        pathname="service.py",
        lineno=10,
        msg="Service started",
        args=(),
        exc_info=None,
    )

    output = formatter.format(record)
    data = json.loads(output)

    assert data["level"] == "INFO"
    assert data["logger"] == "assistant_core"
    assert data["msg"] == "Service started"
    assert "intent" not in data
    assert "latency_ms" not in data


def test_json_formatter_structured_extras() -> None:
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="assistant_core",
        level=logging.INFO,
        pathname="service.py",
        lineno=25,
        msg="handled",
        args=(),
        exc_info=None,
    )
    record.intent = "fee"
    record.latency_ms = 4.25
    record.session = "test-session-123"
    record.degraded = False

    output = formatter.format(record)
    data = json.loads(output)

    assert data["level"] == "INFO"
    assert data["logger"] == "assistant_core"
    assert data["msg"] == "handled"
    assert data["intent"] == "fee"
    assert data["latency_ms"] == 4.25
    assert data["session"] == "test-session-123"
    assert data["degraded"] is False


def test_json_formatter_sanitizes_sensitive_keys() -> None:
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="assistant_core",
        level=logging.INFO,
        pathname="service.py",
        lineno=30,
        msg="request received",
        args=(),
        exc_info=None,
    )
    # Simulate accidental inclusion of sensitive attributes
    record.api_key = "sk-test-super-secret-key"
    record.secret = "my-secret"
    record.token = "bearer-token"
    record.intent = "office"

    output = formatter.format(record)
    data = json.loads(output)

    assert "api_key" not in data
    assert "secret" not in data
    assert "token" not in data
    assert data["intent"] == "office"


def test_setup_logging_custom_stream() -> None:
    buffer = io.StringIO()
    logger = setup_logging(level="DEBUG", stream=buffer)

    logger.debug("Debug event triggered", extra={"intent": "greeting", "session": "s1"})

    buffer.seek(0)
    lines = buffer.getvalue().strip().splitlines()
    assert len(lines) == 1

    data = json.loads(lines[0])
    assert data["level"] == "DEBUG"
    assert data["msg"] == "Debug event triggered"
    assert data["intent"] == "greeting"
    assert data["session"] == "s1"


def test_setup_cli_logging_defaults_to_stderr() -> None:
    setup_cli_logging(level="INFO")
    logger = logging.getLogger("assistant_core")

    assert len(logger.handlers) == 1
    handler = logger.handlers[0]
    assert isinstance(handler, logging.StreamHandler)
    assert handler.stream is sys.stderr
    assert isinstance(handler.formatter, JsonFormatter)
