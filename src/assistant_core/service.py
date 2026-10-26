"""Core service layer for assistant_core.

Implements AssistantService with dependency injection, intent routing,
knowledge retrieval, deterministic fee computation, and fallback handling.
"""

from __future__ import annotations

import csv
import json
import logging
import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from assistant_core.responder import Responder, StubLLMResponder, TemplateResponder
from assistant_core.router import GREETINGS, route
from assistant_core.tools import parse_credits, tuition

log = logging.getLogger("assistant_core")

__all__ = [
    "AssistantService",
    "GREETINGS",
    "route",
    "parse_credits",
    "tuition",
]

# ---------------------------------------------------------------------------
# Contracts & Models (with self-contained fallbacks for unmerged modules)
# ---------------------------------------------------------------------------

try:
    from assistant_core.errors import (
        AssistantError,
        ConfigError,
        DataError,
        InvalidRequest,
        ProviderError,
    )
except ImportError:

    class AssistantError(Exception):
        """Base class for all assistant errors."""

    class ConfigError(AssistantError):
        """Configuration is missing or invalid."""

    class DataError(AssistantError):
        """A knowledge file is missing or malformed."""

    class InvalidRequest(AssistantError):
        """The user's request cannot be processed as given."""

    class ProviderError(AssistantError):
        """The AI provider failed (timeout, outage, bad response)."""


try:
    from assistant_core.config import Settings, load_settings
except ImportError:
    import os

    @dataclass
    class Settings:  # type: ignore[no-redef]
        data_dir: Path = Path("data")
        llm_provider: str = "stub"
        llm_api_key: str | None = None
        credit_rate_vnd: int = 450_000
        retake_multiplier: float = 1.5
        max_credits: int = 30
        log_level: str = "INFO"

    def load_settings(env_file: str | None = ".env") -> Settings:
        if env_file:
            try:
                from dotenv import load_dotenv

                load_dotenv(env_file, override=False)
            except ImportError:
                pass

        return Settings(
            data_dir=Path(os.getenv("ASSISTANT_DATA_DIR", "data")),
            llm_provider=os.getenv("LLM_PROVIDER", "stub"),
            llm_api_key=os.getenv("LLM_API_KEY") or None,
            credit_rate_vnd=int(os.getenv("CREDIT_RATE_VND", "450000")),
            retake_multiplier=float(os.getenv("RETAKE_MULTIPLIER", "1.5")),
            max_credits=int(os.getenv("MAX_CREDITS", "30")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )


try:
    from assistant_core.models import Intent, Message, Response, Source
except ImportError:
    try:
        from pydantic import BaseModel, Field

        class Intent(str, Enum):
            GREETING = "greeting"
            FEE = "fee"
            OFFICE = "office"
            RULE = "rule"
            HELP = "help"
            UNKNOWN = "unknown"

        class Message(BaseModel):
            text: str = Field(min_length=1, max_length=2000)
            session_id: str = "local"

        class Source(BaseModel):
            id: str
            title: str

        class Response(BaseModel):
            answer: str
            intent: Intent
            sources: list[Source] = []
            degraded: bool = False

    except ImportError:
        # Fallback if pydantic is not yet installed in local environment
        class Intent(str, Enum):  # type: ignore[no-redef]
            GREETING = "greeting"
            FEE = "fee"
            OFFICE = "office"
            RULE = "rule"
            HELP = "help"
            UNKNOWN = "unknown"

        @dataclass
        class Message:  # type: ignore[no-redef]
            text: str
            session_id: str = "local"

            def __post_init__(self) -> None:
                if not (1 <= len(self.text) <= 2000):
                    raise ValueError("text length must be between 1 and 2000 characters")

        @dataclass
        class Source:  # type: ignore[no-redef]
            id: str
            title: str

        @dataclass
        class Response:  # type: ignore[no-redef]
            answer: str
            intent: Intent
            sources: list[Source] = None  # type: ignore[assignment]
            degraded: bool = False

            def __post_init__(self) -> None:
                if self.sources is None:
                    self.sources = []


# ---------------------------------------------------------------------------
# Sibling Module Interfaces (Fallback Implementations)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Office:
    name: str
    room: str
    hours: str


class OfficeDirectory:
    def __init__(self, offices: dict[str, Office]) -> None:
        self._offices = offices

    @classmethod
    def from_csv(cls, path: Path) -> OfficeDirectory:
        try:
            with path.open(encoding="utf-8", newline="") as f:
                rows = list(csv.DictReader(f))
        except FileNotFoundError as exc:
            raise DataError(f"office file not found: {path}") from exc
        return cls({r["name"].lower(): Office(r["name"], r["room"], r["hours"]) for r in rows})

    @property
    def names(self) -> set[str]:
        return set(self._offices)

    def find(self, text: str) -> Office | None:
        t = text.lower()
        return next((o for name, o in self._offices.items() if name in t), None)


@dataclass(frozen=True)
class Rule:
    id: str
    title: str
    text: str


class Handbook:
    def __init__(self, rules: list[Rule]) -> None:
        self._rules = rules

    @classmethod
    def from_json(cls, path: Path) -> Handbook:
        try:
            with path.open(encoding="utf-8") as f:
                raw = json.load(f)
        except FileNotFoundError as exc:
            raise DataError(f"handbook file not found: {path}") from exc
        return cls([Rule(r["id"], r.get("title", r["id"]), r["text"]) for r in raw])

    def search(self, query: str) -> Rule | None:
        q_words = {w for w in re.findall(r"\w+", query.lower()) if len(w) > 3}
        best_rule = None
        best_score = 0
        for r in self._rules:
            r_text = (r.title + " " + r.text).lower()
            score = sum(1 for w in q_words if w in r_text)
            if score > best_score:
                best_score = score
                best_rule = r
        return best_rule if best_score > 0 else None


# ---------------------------------------------------------------------------
# AssistantService Class (Member 1 Primary Deliverable)
# ---------------------------------------------------------------------------


class AssistantService:
    """Central orchestrator for the study assistant service.

    Accepts dependencies via constructor injection for testability and loose coupling.
    Exposes handle(Message) -> Response as the single public entry point.
    """

    def __init__(
        self,
        settings: Any,
        offices: Any,
        handbook: Any,
        responder: Responder,
    ) -> None:
        self.settings = settings
        self.offices = offices
        self.handbook = handbook
        self.responder: Responder = responder
        self.fallback = TemplateResponder()

    def handle(self, msg: Message) -> Response:
        """Process incoming student message and return structured response."""
        office_names = getattr(self.offices, "names", set())
        intent = route(msg.text, office_names)

        if intent is Intent.GREETING:
            return Response(
                answer="Hello! I can help with offices, fees and rules.",
                intent=intent,
            )

        if intent is Intent.HELP:
            return Response(
                answer=(
                    "I can help you find campus offices, calculate tuition fees, "
                    "and search academic rules. Try asking 'where is the training office?' "
                    "or 'tuition for 18 credits'."
                ),
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
        """Calculate tuition deterministically, handling user errors gracefully."""
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
        """Search handbook rules and explain via responder with fallback."""
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
    def default(cls, settings: Any = None, data_dir: Path | str | None = None) -> AssistantService:
        """Convenience factory method to instantiate AssistantService with standard components."""
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
