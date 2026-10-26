"""Unit tests for office directory and handbook."""

from pathlib import Path

import pytest

from assistant_core.errors import DataError
from assistant_core.knowledge import Handbook, OfficeDirectory


def test_load_offices(data_dir: Path):
    offices = OfficeDirectory.from_csv(data_dir / "offices.csv")

    assert len(offices.names) == 4
    assert "library" in offices.names


def test_find_office_case_insensitive(data_dir: Path):
    offices = OfficeDirectory.from_csv(data_dir / "offices.csv")

    result = offices.find("WHERE IS THE LIBRARY?")

    assert result is not None
    assert result.name == "Library"
    assert result.room == "B.201"


def test_find_unknown_office(data_dir: Path):
    offices = OfficeDirectory.from_csv(data_dir / "offices.csv")

    assert offices.find("Where is the cafeteria?") is None


def test_missing_office_file(tmp_path: Path):
    with pytest.raises(DataError):
        OfficeDirectory.from_csv(tmp_path / "missing.csv")


def test_invalid_office_header(tmp_path: Path):
    path = tmp_path / "invalid.csv"
    path.write_text("name,room\nLibrary,B.201\n", encoding="utf-8")

    with pytest.raises(DataError):
        OfficeDirectory.from_csv(path)


def test_incomplete_office_data(tmp_path: Path):
    path = tmp_path / "incomplete.csv"
    path.write_text("name,room,hours\nLibrary,B.201,\n", encoding="utf-8")

    with pytest.raises(DataError):
        OfficeDirectory.from_csv(path)


def test_load_handbook(data_dir: Path):
    handbook = Handbook.from_json(data_dir / "handbook.json")

    assert handbook.search("thesis registration") is not None


def test_search_handbook(data_dir: Path):
    handbook = Handbook.from_json(data_dir / "handbook.json")

    result = handbook.search("thesis registration credits")

    assert result is not None
    assert result.id == "H26-5.3"


def test_empty_handbook_query(data_dir: Path):
    handbook = Handbook.from_json(data_dir / "handbook.json")

    assert handbook.search("") is None


def test_missing_handbook_file(tmp_path: Path):
    with pytest.raises(DataError):
        Handbook.from_json(tmp_path / "missing.json")


def test_invalid_handbook_json(tmp_path: Path):
    path = tmp_path / "invalid.json"
    path.write_text("{invalid json}", encoding="utf-8")

    with pytest.raises(DataError):
        Handbook.from_json(path)


def test_invalid_handbook_structure(tmp_path: Path):
    path = tmp_path / "handbook.json"
    path.write_text('{"id": "H26-1"}', encoding="utf-8")

    with pytest.raises(DataError):
        Handbook.from_json(path)
