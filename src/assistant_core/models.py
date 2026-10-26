"""Typed data models for the assistant core."""

from enum import Enum

from pydantic import BaseModel, Field


class Intent(str, Enum):
    """Supported user request intents."""

    GREETING = "greeting"
    FEE = "fee"
    OFFICE = "office"
    RULE = "rule"
    HELP = "help"
    UNKNOWN = "unknown"


class Message(BaseModel):
    """Incoming message from a user."""

    text: str = Field(min_length=1, max_length=2000)
    session_id: str = "local"


class Source(BaseModel):
    """Reference to a knowledge source."""

    id: str
    title: str


class Response(BaseModel):
    """Structured response returned by the assistant."""

    answer: str
    intent: Intent
    sources: list[Source] = Field(default_factory=list)
    degraded: bool = False
