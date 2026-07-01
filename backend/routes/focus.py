from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.core.dependencies import get_current_user
from backend.services.focus_service import start_focus, finish_focus
from backend.services.xp_service import add_xp
from backend.models.daily_task import DailyTask
from backend.models.focus_session import FocusSession

router = APIRouter(tags=["Focus"])


@router.post("/start/{task_id}")
def start_focus_session(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    task = db.query(DailyTask).filter(
        DailyTask.id == task_id,
        DailyTask.user_id == current_user.id,
        DailyTask.completed == False
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Tarefa de hoje não encontrada")

    return start_focus(current_user, task_id, db)


@router.post("/finish/{session_id}")
def finish_focus_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    session_owner = db.query(FocusSession).filter(
        FocusSession.id == session_id,
        FocusSession.user_id == current_user.id
    ).first()

    if not session_owner:
        raise HTTPException(status_code=404, detail="Sessão de foco não encontrada")

    session = finish_focus(session_id, db)

    if session:
        add_xp(current_user, 15, db)  # bônus foco

    return {"message": "Foco concluído! +15 XP"}
