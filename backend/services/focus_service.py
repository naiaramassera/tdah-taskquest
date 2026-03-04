from datetime import datetime
from backend.models.focus_session import FocusSession


def start_focus(user, task_id, db):

    session = FocusSession(
        user_id=user.id,
        task_id=task_id
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def finish_focus(session_id, db):

    session = db.query(FocusSession).filter(
        FocusSession.id == session_id
    ).first()

    if not session:
        return None

    session.finished_at = datetime.utcnow()
    session.completed = True

    db.commit()

    return session