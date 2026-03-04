from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.core.dependencies import get_current_user
from backend.services.focus_service import start_focus, finish_focus
from backend.services.xp_service import add_xp

router = APIRouter(tags=["Focus"])


@router.post("/start/{task_id}")
def start_focus_session(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return start_focus(current_user, task_id, db)


@router.post("/finish/{session_id}")
def finish_focus_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    session = finish_focus(session_id, db)

    if session:
        add_xp(current_user, 15, db)  # bônus foco

    return {"message": "Foco concluído! +15 XP"}