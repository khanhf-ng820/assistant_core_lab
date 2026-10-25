"""Unit tests for the AI-generated exam absence extension."""

from pathlib import Path

import pytest

from assistant_core.exam_absence import (
    ExamAbsenceDataError,
    answer_exam_absence,
)


def test_exam_absence_answer():
    result = answer_exam_absence(
        "What should I do if I miss my final exam?"
    )

    assert result is not None
    assert "3 working days" in result
    assert "Training Office" in result


def test_vietnamese_question():
    result = answer_exam_absence("Em vắng thi thì sao?")

    assert result is not None
    assert "3 working days" in result


def test_unrelated_exam_question():
    assert answer_exam_absence("When is the exam?") is None


def test_unrelated_message():
    assert answer_exam_absence("Where is the library?") is None


def test_works_from_different_directory(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
):
    monkeypatch.chdir(tmp_path)

    result = answer_exam_absence("I missed my exam")

    assert result is not None
    assert "3 working days" in result


def test_missing_handbook_file(tmp_path: Path):
    missing = tmp_path / "missing.json"

    with pytest.raises(ExamAbsenceDataError):
        answer_exam_absence(
            "I missed my exam",
            handbook_path=missing,
        )


def test_invalid_json(tmp_path: Path):
    path = tmp_path / "handbook.json"
    path.write_text("{invalid json}", encoding="utf-8")

    with pytest.raises(ExamAbsenceDataError):
        answer_exam_absence(
            "I missed my exam",
            handbook_path=path,
        )


def test_invalid_handbook_structure(tmp_path: Path):
    path = tmp_path / "handbook.json"
    path.write_text('{"id": "H26-7.2"}', encoding="utf-8")

    with pytest.raises(ExamAbsenceDataError):
        answer_exam_absence(
            "I missed my exam",
            handbook_path=path,
        )


def test_invalid_rule_fields(tmp_path: Path):
    path = tmp_path / "handbook.json"
    path.write_text('[{"id": "H26-7.2"}]', encoding="utf-8")

    with pytest.raises(ExamAbsenceDataError):
        answer_exam_absence(
            "I missed my exam",
            handbook_path=path,
        )


def test_unrelated_question_skips_data_loading(tmp_path: Path):
    missing = tmp_path / "missing.json"

    result = answer_exam_absence(
        "When is the exam?",
        handbook_path=missing,
    )

    assert result is None