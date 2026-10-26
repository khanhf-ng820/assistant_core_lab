"""Knowledge base for offices and university handbook rules."""

import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path

from assistant_core.errors import DataError


@dataclass(frozen=True)
class Office:
    """Information about a university office."""

    name: str
    room: str
    hours: str


class OfficeDirectory:
    """Load and search university office information."""

    def __init__(self, offices: dict[str, Office]) -> None:
        self._offices = offices

    @classmethod
    def from_csv(cls, path: Path) -> "OfficeDirectory":
        """Load office information from a CSV file."""
        try:
            with Path(path).open(encoding="utf-8", newline="") as file:
                reader = csv.DictReader(file)

                required = {"name", "room", "hours"}
                if not required.issubset(reader.fieldnames or []):
                    raise DataError("Office CSV is missing required columns.")

                offices = {}

                for row in reader:
                    if not all(row.get(field) for field in required):
                        raise DataError("Office CSV contains incomplete data.")

                    office = Office(
                        name=row["name"],
                        room=row["room"],
                        hours=row["hours"],
                    )
                    offices[office.name.lower()] = office

        except OSError as exc:
            raise DataError(f"Cannot read office file: {path}") from exc

        return cls(offices)

    @property
    def names(self) -> set[str]:
        """Return the names of available offices."""
        return set(self._offices)

    def find(self, text: str) -> Office | None:
        """Find an office mentioned in the user's message."""
        query = text.lower()

        for name, office in self._offices.items():
            if name in query:
                return office

        return None
@dataclass(frozen=True)
class Rule:
    """A university handbook rule."""

    id: str
    title: str
    text: str


class Handbook:
    """Load and search university handbook rules."""

    def __init__(self, rules: list[Rule]) -> None:
        self._rules = list(rules)

    @classmethod
    def from_json(cls, path: Path) -> "Handbook":
        """Load handbook rules from a JSON file."""
        try:
            with Path(path).open(encoding="utf-8") as file:
                data = json.load(file)

        except OSError as exc:
            raise DataError(f"Cannot read handbook file: {path}") from exc

        except json.JSONDecodeError as exc:
            raise DataError(f"Invalid handbook JSON: {path}") from exc

        if not isinstance(data, list):
            raise DataError("Handbook must contain a list of rules.")

        rules: list[Rule] = []

        for index, item in enumerate(data, start=1):
            if not isinstance(item, dict):
                raise DataError(f"Invalid rule at position {index}.")

            required = ("id", "title", "text")

            if not all(
                isinstance(item.get(field), str) and item[field].strip()
                for field in required
            ):
                raise DataError(f"Invalid rule data at position {index}.")

            rules.append(
                Rule(
                    id=item["id"],
                    title=item["title"],
                    text=item["text"],
                )
            )

        return cls(rules)

    def search(self, query: str) -> Rule | None:
        """Find the most relevant rule using keyword overlap."""
        keywords = set(re.findall(r"[a-z0-9]+", query.lower()))

        if not keywords:
            return None

        best_rule: Rule | None = None
        best_score = 0

        for rule in self._rules:
            title_words = set(
                re.findall(r"[a-z0-9]+", rule.title.lower())
            )
            text_words = set(
                re.findall(r"[a-z0-9]+", rule.text.lower())
            )

            score = (
                2 * len(keywords & title_words)
                + len(keywords & text_words)
            )

            if score > best_score:
                best_score = score
                best_rule = rule

        return best_rule