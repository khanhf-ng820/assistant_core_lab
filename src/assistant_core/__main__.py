"""Command-line interface for assistant_core.

Supports one-shot question queries and interactive REPL mode.
Directs structured JSON logging to stderr and user answers to stdout.
"""

from __future__ import annotations

import logging
import sys
import time

from assistant_core.logging_setup import setup_cli_logging
from assistant_core.service import AssistantError, AssistantService, Message

logger = logging.getLogger("assistant_core")


def execute_query(service: AssistantService, text: str, session_id: str = "local") -> str:
    """Execute query, emit structured log to stderr, and return answer."""
    clean_text = text.strip()
    if not clean_text:
        return "Please type a question."

    start_time = time.perf_counter()
    msg = Message(text=clean_text, session_id=session_id)
    response = service.handle(msg)
    elapsed_ms = (time.perf_counter() - start_time) * 1000

    intent_val = response.intent.value if hasattr(response.intent, "value") else str(response.intent)

    # Structured log output (no raw student message, no API keys)
    logger.info(
        "handled",
        extra={
            "intent": intent_val,
            "latency_ms": round(elapsed_ms, 2),
            "session": session_id,
            "degraded": response.degraded,
        },
    )
    return response.answer


def main(argv: list[str] | None = None) -> int:
    """Entry point for CLI."""
    argv = sys.argv[1:] if argv is None else argv
    setup_cli_logging()

    try:
        service = AssistantService.default()
    except (AssistantError, OSError, ValueError) as exc:
        logger.error(f"Failed to initialize AssistantService: {exc}")
        print(f"Startup error: {exc}", file=sys.stderr)
        return 1

    if argv:
        query = " ".join(argv)
        answer = execute_query(service, query)
        print(answer)
        return 0

    print("Study assistant core (interactive mode). Type 'quit' or 'exit' to exit.")
    while True:
        try:
            user_input = input("> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        cleaned = user_input.strip()
        if not cleaned:
            continue
        if cleaned.lower() in {"quit", "exit"}:
            break

        answer = execute_query(service, cleaned)
        print(answer)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
