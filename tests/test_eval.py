import csv
import runpy
from pathlib import Path

import pytest

from assistant_core.rules import reply

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "eval" / "cases.csv"
RUNNER_PATH = ROOT / "eval" / "run.py"

# These Lab 2 assets are not shipped with the Lab 3 starter. If either file is
# added, run the tests so a missing counterpart or malformed benchmark fails.
pytestmark = pytest.mark.skipif(
    not CASES_PATH.exists() and not RUNNER_PATH.exists(),
    reason="Lab 2 benchmark CSV and runner are not included in this Lab 3 repository",
)


def test_cases_csv_exists_and_valid():
    assert CASES_PATH.is_file(), f"Missing benchmark file: {CASES_PATH}"
    with CASES_PATH.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ["question", "expected", "category"]
        rows = list(reader)
        assert len(rows) >= 15


def test_cases_count_and_edge_cases():
    with CASES_PATH.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 15
    edge_cases = [r for r in rows if r["category"] == "edge"]
    assert len(edge_cases) >= 3, f"Expected at least 3 edge cases, got {len(edge_cases)}"


def test_cases_expected_answers_match_reply():
    with CASES_PATH.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            actual = reply(row["question"])
            assert actual == row["expected"], f"Mismatch for {row['question']!r}: {actual!r} != {row['expected']!r}"


def test_benchmark_runner_executes(capsys):
    assert RUNNER_PATH.is_file(), f"Missing runner script: {RUNNER_PATH}"
    runpy.run_path(str(RUNNER_PATH), run_name="__main__")
    captured = capsys.readouterr()
    assert "Accuracy: 15/15 (100.0%)" in captured.out
