"""Benchmark tests for the optional ``eval/`` artifacts.

The Lab-3 refactor branch does not ship the Lab-2 benchmark files. Skip these
tests when the artifacts are absent instead of failing collection; they still
run if a teammate adds ``eval/cases.csv`` and ``eval/run.py`` later.
"""

from __future__ import annotations

import csv
import runpy
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "eval" / "cases.csv"
RUNNER_PATH = ROOT / "eval" / "run.py"

pytestmark = pytest.mark.skipif(
    not (CASES_PATH.is_file() and RUNNER_PATH.is_file()),
    reason="optional eval/ benchmark artifacts are not present",
)


def test_cases_csv_exists_and_valid() -> None:
    assert CASES_PATH.is_file(), f"Missing benchmark file: {CASES_PATH}"
    with CASES_PATH.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ["question", "expected", "category"]
        rows = list(reader)
        assert len(rows) >= 15


def test_cases_count_and_edge_cases() -> None:
    with CASES_PATH.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 15
    edge_cases = [r for r in rows if r["category"] == "edge"]
    assert len(edge_cases) >= 3, f"Expected at least 3 edge cases, got {len(edge_cases)}"


def test_cases_expected_answers_match_reply() -> None:
    from assistant_core.service import AssistantService, Message

    service = AssistantService.default(data_dir=ROOT / "data")
    with CASES_PATH.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            actual = service.handle(Message(text=row["question"])).answer
            assert actual == row["expected"], f"Mismatch for {row['question']!r}: {actual!r} != {row['expected']!r}"


def test_benchmark_runner_executes(capsys: pytest.CaptureFixture[str]) -> None:
    assert RUNNER_PATH.is_file(), f"Missing runner script: {RUNNER_PATH}"
    runpy.run_path(str(RUNNER_PATH), run_name="__main__")
    captured = capsys.readouterr()
    assert "Accuracy: 15/15 (100.0%)" in captured.out
