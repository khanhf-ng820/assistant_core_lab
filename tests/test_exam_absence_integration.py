"""Integration tests for exam absence support in the assistant."""

from assistant_core.rules import reply


def test_exam_absence_integration():
    result = reply("What if I miss my final exam?")

    assert "3 working days" in result
    assert "Training Office" in result
    assert "H26-7.2" in result


def test_unrelated_exam_question():
    result = reply("When is the exam?")

    assert "H26-7.2" not in result


def test_office_lookup_still_works():
    result = reply("Where is the library?")

    assert "Library" in result
    assert "B.201" in result


def test_greeting_still_works():
    result = reply("hi")

    assert "Hello!" in result
