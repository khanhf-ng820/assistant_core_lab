"""Verify that Lab 5 interaction data survives reopening SQLite."""

from sqlmodel import Session, select

from assistant_api.db import (
    ChatSession,
    Feedback,
    Interaction,
    Repository,
    hash_session,
    init_db,
    make_engine,
)


def test_interaction_survives_database_reopen(tmp_path):
    db_path = tmp_path / "persistence_test.db"
    database_url = f"sqlite:///{db_path}"
    session_salt = "qa-test-salt"

    # First application/database lifecycle.
    engine1 = make_engine(database_url)
    init_db(engine1)

    repo1 = Repository(engine1, session_salt)
    repo1.record_interaction(
        raw_session="qa-student-01",
        request_id="qa-request-001",
        intent="fee",
        topic=None,
        resolved=True,
        degraded=False,
        latency_ms=12.5,
    )
    engine1.dispose()

    # Simulate an application restart using a new engine.
    engine2 = make_engine(database_url)
    init_db(engine2)

    with Session(engine2) as db:
        interactions = db.exec(select(Interaction)).all()
        sessions = db.exec(select(ChatSession)).all()

    assert len(interactions) == 1
    assert interactions[0].request_id == "qa-request-001"
    assert interactions[0].intent == "fee"
    assert interactions[0].latency_ms == 12.5

    assert len(sessions) == 1
    assert sessions[0].id == hash_session("qa-student-01", session_salt)
    assert sessions[0].id != "qa-student-01"

    engine2.dispose()


def test_feedback_survives_database_reopen(tmp_path):
    db_path = tmp_path / "feedback_restart.db"
    database_url = f"sqlite:///{db_path}"

    engine1 = make_engine(database_url)
    init_db(engine1)

    repo1 = Repository(engine1, "qa-test-salt")
    repo1.record_interaction(
        raw_session="qa-student-02",
        request_id="qa-feedback-001",
        intent="fee",
        topic=None,
        resolved=True,
        degraded=False,
        latency_ms=10.0,
    )

    feedback = repo1.add_feedback("qa-feedback-001", -1, "Incorrect answer")

    assert feedback is not None
    assert feedback.id is not None

    engine1.dispose()

    engine2 = make_engine(database_url)

    with Session(engine2) as db:
        stored = db.exec(select(Feedback).where(Feedback.request_id == "qa-feedback-001")).one()

    assert stored.rating == -1
    assert stored.comment == "Incorrect answer"

    engine2.dispose()
