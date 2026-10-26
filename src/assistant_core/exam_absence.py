"""Answer questions about final exam absence."""

import json
from pathlib import Path

HANDBOOK_PATH = Path(__file__).resolve().parents[2] / "data" / "handbook.json"


class ExamAbsenceDataError(Exception):
    """Raised when handbook data cannot be loaded or validated."""


def answer_exam_absence(
    message: str,
    handbook_path: Path = HANDBOOK_PATH,
) -> str | None:
    """Find the exam absence rule in the handbook."""
    text = message.casefold()

    exam_keywords = ("exam", "thi")
    absence_keywords = (
        "miss",
        "absen",
        "vắng",
        "bỏ lỡ",
        "không thể dự",
    )

    has_exam = any(word in text for word in exam_keywords)
    has_absence = any(word in text for word in absence_keywords)

    if not (has_exam and has_absence):
        return None

    try:
        with handbook_path.open(encoding="utf-8") as file:
            rules = json.load(file)
    except OSError as exc:
        raise ExamAbsenceDataError("Cannot read handbook file") from exc
    except json.JSONDecodeError as exc:
        raise ExamAbsenceDataError("Invalid handbook JSON") from exc

    if not isinstance(rules, list):
        raise ExamAbsenceDataError("Handbook must contain a list")

    for rule in rules:
        if not isinstance(rule, dict):
            raise ExamAbsenceDataError("Invalid handbook rule")

        if not isinstance(rule.get("id"), str) or not isinstance(rule.get("text"), str):
            raise ExamAbsenceDataError("Missing or invalid rule fields")

        if rule["id"] == "H26-7.2":
            return rule["text"]

    return None
