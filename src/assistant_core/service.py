"""Core service layer for assistant_core.

Implements AssistantService with dependency injection, intent routing,
knowledge retrieval, deterministic fee computation, and fallback handling.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from assistant_core.config import Settings, load_settings
from assistant_core.errors import (
    AssistantError,
    ConfigError,
    DataError,
    InvalidRequest,
    ProviderError,
)
from assistant_core.knowledge import Handbook, Office, OfficeDirectory, Rule
from assistant_core.models import Intent, Message, Response, Source
from assistant_core.responder import (
    Responder,
    StubLLMResponder,
    TemplateResponder,
)
from assistant_core.router import GREETINGS, route
from assistant_core.tools import parse_credits, tuition

log = logging.getLogger("assistant_core")

__all__ = [
    "AssistantService",
    "AssistantError",
    "ConfigError",
    "DataError",
    "InvalidRequest",
    "ProviderError",
    "Settings",
    "load_settings",
    "Intent",
    "Message",
    "Response",
    "Source",
    "Office",
    "OfficeDirectory",
    "Rule",
    "Handbook",
    "Responder",
    "StubLLMResponder",
    "TemplateResponder",
    "GREETINGS",
    "route",
    "parse_credits",
    "tuition",
]


class AssistantService:
    """Central orchestrator for the study assistant service."""

    def __init__(
        self,
        settings: Any,
        offices: Any,
        handbook: Any,
        responder: Any,
    ) -> None:
        self.settings = settings
        self.offices = offices
        self.handbook = handbook
        self.responder = responder
        self.fallback = TemplateResponder()

    def handle(self, msg: Message) -> Response:
        """Process incoming student message and return structured response."""
        if msg.text.strip().lower().rstrip("?!.,") == "help":
            return Response(
                answer=(
                    "I can help with office locations and hours, tuition calculations, "
                    "and handbook rules. Try 'where is the library?' or 'tuition for 18 credits'."
                ),
                intent=Intent.GREETING,
            )

        office_names = getattr(self.offices, "names", set())
        intent = route(msg.text, office_names)

        if intent is Intent.GREETING:
            return Response(
                answer="Hello! I can help with offices, fees and rules.",
                intent=intent,
            )

        if intent is Intent.FEE:
            return self._fee(msg.text)

        if intent is Intent.OFFICE:
            office = self.offices.find(msg.text)
            if office is not None:
                return Response(
                    answer=f"{office.name}: room {office.room}, open {office.hours}.",
                    intent=intent,
                )
            return Response(
                answer="Sorry, I don't know that office.",
                intent=Intent.UNKNOWN,
            )

        return self._rule(msg.text)

    def _fee(self, text: str) -> Response:
        try:
            credits, retake = parse_credits(text)
            rate = getattr(self.settings, "credit_rate_vnd", 450_000)
            retake_multiplier = getattr(self.settings, "retake_multiplier", 1.5)
            max_credits = getattr(self.settings, "max_credits", 30)
            total = tuition(credits, retake, rate, retake_multiplier, max_credits)
            return Response(
                answer=f"Your tuition is {total:,} VND.",
                intent=Intent.FEE,
            )
        except InvalidRequest as exc:
            return Response(answer=str(exc), intent=Intent.FEE)

    def _rule(self, text: str) -> Response:
        rule = self.handbook.search(text)
        if rule is None:
            return Response(
                answer="Sorry, I don't know that yet.",
                intent=Intent.UNKNOWN,
            )

        sources = [Source(id=rule.id, title=rule.title)]
        try:
            answer = self.responder.explain(text, rule)
            return Response(
                answer=answer,
                intent=Intent.RULE,
                sources=sources,
            )
        except ProviderError:
            log.warning("provider failed; using template fallback")
            answer = self.fallback.explain(text, rule)
            return Response(
                answer=answer,
                intent=Intent.RULE,
                sources=sources,
                degraded=True,
            )

    @classmethod
    def default(cls, settings: Any = None, data_dir: Any = None) -> AssistantService:
        if settings is None:
            settings = load_settings()

        if data_dir is not None:
            settings.data_dir = Path(data_dir)

        base_data = Path(getattr(settings, "data_dir", "data"))
        if not base_data.is_absolute() and not base_data.is_dir():
            repo_root = Path(__file__).resolve().parents[2]
            if (repo_root / base_data).is_dir():
                base_data = repo_root / base_data

        offices_file = base_data / "offices.csv"
        handbook_file = base_data / "handbook.json"

        offices = OfficeDirectory.from_csv(offices_file)
        handbook = Handbook.from_json(handbook_file)
        responder = StubLLMResponder()

        return cls(
            settings=settings,
            offices=offices,
            handbook=handbook,
            responder=responder,
        )
