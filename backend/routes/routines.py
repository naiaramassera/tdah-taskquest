from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.core.dependencies import get_current_user
from backend.models.routine_task import RoutineTask
from backend.models.world import World

router = APIRouter(tags=["Routines"])


@router.post("/{world_id}")
def create_routine_task(
    world_id: int,
    title: str,
    difficulty: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    world = db.query(World).filter(
        World.id == world_id,
        World.user_id == current_user.id
    ).first()

    if not world:
        return {"error": "World not found"}

    routine = RoutineTask(
        world_id=world_id,
        title=title,
        difficulty=difficulty
    )

    db.add(routine)
    db.commit()
    db.refresh(routine)

    return routine


@router.get("/{world_id}")
def list_routines(
    world_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(RoutineTask).join(World).filter(
        World.user_id == current_user.id,
        RoutineTask.world_id == world_id
    ).all()
