"""Tests for R2 — `Repository.list_feedback` (newest first, limited).

These tests insert feedback rows with explicit timestamps through the ORM so they
do not depend on R1 (`add_feedback`), which lives on its own branch.
"""

from datetime import datetime, timedelta, timezone

from sqlmodel import Session

from assistant_api.db import Feedback, Repository, init_db, make_engine

BASE = datetime(2026, 11, 1, 9, 0, tzinfo=timezone.utc)


def make_repo():
    engine = make_engine("sqlite://")
    init_db(engine)
    return Repository(engine, "salt"), engine


def add_feedback(repo, engine, request_id: str, rating: int, minutes: int) -> None:
    """Create an interaction and one feedback row dated BASE + `minutes`."""
    repo.record_interaction("student-1", request_id, "fee", None, True, False, 1.0)
    with Session(engine) as db:
        db.add(Feedback(request_id=request_id, rating=rating, created_at=BASE + timedelta(minutes=minutes)))
        db.commit()


def test_list_feedback_returns_newest_first():
    repo, engine = make_repo()
    # inserted out of chronological order on purpose
    add_feedback(repo, engine, "r30", 1, minutes=30)
    add_feedback(repo, engine, "r0", 1, minutes=0)
    add_feedback(repo, engine, "r60", -1, minutes=60)

    listed = repo.list_feedback()

    assert [f.request_id for f in listed] == ["r60", "r30", "r0"]


def test_list_feedback_respects_limit():
    repo, engine = make_repo()
    for i in range(5):
        add_feedback(repo, engine, f"r{i}", -1, minutes=i)

    assert [f.request_id for f in repo.list_feedback(limit=2)] == ["r4", "r3"]


def test_list_feedback_default_limit_keeps_all_when_few_rows():
    repo, engine = make_repo()
    add_feedback(repo, engine, "only", 0, minutes=0)

    listed = repo.list_feedback()

    assert [f.request_id for f in listed] == ["only"]


def test_list_feedback_empty_database():
    repo, _ = make_repo()

    assert repo.list_feedback() == []
