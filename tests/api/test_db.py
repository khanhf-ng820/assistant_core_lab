from datetime import datetime, timedelta, timezone

from sqlmodel import Session, select

from assistant_api.db import ChatSession, Feedback, Interaction, Repository, hash_session, init_db, make_engine


def make_repo():
    engine = make_engine("sqlite://")
    init_db(engine)
    return Repository(engine, "salt"), engine


def test_session_id_is_hashed():
    repo, engine = make_repo()
    repo.record_interaction("student-42", "r1", "fee", None, True, False, 3.0)
    with Session(engine) as db:
        s = db.exec(select(ChatSession)).one()
    assert s.id == hash_session("student-42", "salt") and "student-42" not in s.id


def test_one_session_many_interactions():
    repo, engine = make_repo()
    for i in range(3):
        repo.record_interaction("s", f"r{i}", "rule", "H26-5.3", True, False, 10.0)
    with Session(engine) as db:
        assert len(db.exec(select(ChatSession)).all()) == 1
        assert len(db.exec(select(Interaction)).all()) == 3


def test_feedback_requires_existing_interaction():
    repo, _ = make_repo()
    assert repo.add_feedback("missing", 1, None) is None
    repo.record_interaction("s", "r1", "fee", None, True, False, 1.0)
    assert repo.add_feedback("r1", -1, "wrong fee").id == 1


def test_feedback_comment_and_multiple_entries():
    repo, engine = make_repo()
    repo.record_interaction("student-1", "req-123", "rule", "H26-5.3", True, False, 12.5)

    fb1 = repo.add_feedback("req-123", 1, "Rất hữu ích, cảm ơn bot!")
    assert fb1 is not None
    assert fb1.id == 1
    assert fb1.rating == 1
    assert fb1.comment == "Rất hữu ích, cảm ơn bot!"
    assert fb1.created_at is not None

    fb2 = repo.add_feedback("req-123", 0, "Cần bổ sung thêm ví dụ")
    assert fb2 is not None
    assert fb2.id == 2

    with Session(engine) as db:
        feedbacks = db.exec(select(Feedback).where(Feedback.request_id == "req-123")).all()
        assert len(feedbacks) == 2


BASE_TIME = datetime(2026, 11, 1, 9, 0, tzinfo=timezone.utc)


def _seed_feedback(repo, engine, request_id: str, rating: int, minutes: int) -> None:
    repo.record_interaction("student-1", request_id, "fee", None, True, False, 1.0)
    with Session(engine) as db:
        db.add(Feedback(request_id=request_id, rating=rating, created_at=BASE_TIME + timedelta(minutes=minutes)))
        db.commit()


def test_list_feedback_returns_newest_first():
    repo, engine = make_repo()
    _seed_feedback(repo, engine, "r30", 1, minutes=30)
    _seed_feedback(repo, engine, "r0", 1, minutes=0)
    _seed_feedback(repo, engine, "r60", -1, minutes=60)

    listed = repo.list_feedback()
    assert [f.request_id for f in listed] == ["r60", "r30", "r0"]


def test_list_feedback_respects_limit():
    repo, engine = make_repo()
    for i in range(5):
        _seed_feedback(repo, engine, f"r{i}", -1, minutes=i)

    assert [f.request_id for f in repo.list_feedback(limit=2)] == ["r4", "r3"]


def test_list_feedback_default_limit_keeps_all_when_few_rows():
    repo, engine = make_repo()
    _seed_feedback(repo, engine, "only", 0, minutes=0)

    listed = repo.list_feedback()
    assert [f.request_id for f in listed] == ["only"]


def test_list_feedback_empty_database():
    repo, _ = make_repo()
    assert repo.list_feedback() == []
