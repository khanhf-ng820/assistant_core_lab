"""A tiny rule-based responder. No AI yet — that comes in Week 4."""

from __future__ import annotations

import csv
from pathlib import Path

from assistant_core.exam_absence import answer_exam_absence

DATA_DIR = Path(__file__).resolve().parents[2] / "data"

GREETINGS = {"hi", "hello", "hey", "xin chao", "chao", "good morning"}


def load_offices(path: Path = DATA_DIR / "offices.csv") -> dict[str, dict[str, str]]:
    """Return {office_name_lower: row} from the offices CSV."""
    with path.open(encoding="utf-8", newline="") as f:
        return {row["name"].lower(): row for row in csv.DictReader(f)}


def reply(message: str, offices: dict[str, dict[str, str]] | None = None) -> str:
    """Answer a message with simple rules."""
    text = message.strip().lower().rstrip("?!.")
    if not text:
        return "Please type a question."
    if text == "help":
        return "I can help you find offices and their opening hours. Try 'where is the library?'"
    if text in GREETINGS:
        return "Hello! Ask me where an office is, or when it opens."
    exam_answer = answer_exam_absence(message)
    if exam_answer is not None:
        return f"{exam_answer} (source: H26-7.2)"
    offices = offices if offices is not None else load_offices()
    # 1. Exact full name match (e.g. "where is the training office?")
    for name, row in offices.items():
        if name in text:
            return f"{row['name']}: room {row['room']}, open {row['hours']}."

    # 2. Partial name match (e.g. "training", "where is training?", "health")
    generic_words = {"office", "center"}
    for name, row in offices.items():
        clean_name = name.removesuffix(" office").removesuffix(" center").strip()
        if (clean_name and clean_name in text) or (len(text) >= 3 and text not in generic_words and text in name):
            return f"{row['name']}: room {row['room']}, open {row['hours']}."

    return "I don't know that yet. Try asking about an office, e.g. 'training office'."
