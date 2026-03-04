from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.core.dependencies import get_current_user
from backend.services.daily_generator_service import generate_daily_tasks
from backend.models.daily_task import DailyTask
from backend.models.world import World
from backend.services.mission_service import update_mission_progress
from backend.services.xp_service import add_xp
from backend.services.streak_service import update_streak
from backend.services.xp_service import get_streak_multiplier
from backend.models.energy import Energy
from datetime import date

router = APIRouter(tags=["Daily Tasks"])


@router.post("/generate")
def generate_tasks(
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    return generate_daily_tasks(current_user, db)


@router.get("/")
def list_today_tasks(
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    from datetime import date

    today = date.today()

    tasks = (
        db.query(DailyTask)
        .join(World)
        .filter(
            DailyTask.user_id == current_user.id,
            DailyTask.created_date == today
        )
        .all()
    )

@router.post("/complete/{task_id}")
def complete_task(
    task_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):

    task = db.query(DailyTask).filter(
        DailyTask.id == task_id,
         DailyTask.user_id == current_user.id
    ).first()

    energy = db.query(Energy).filter_by(user_id=current_user.id).first()

    if not task:
        return {"error": "Task not found"}

    if task.completed:
        return {"message": "Already completed"}

    task.completed = True

    if not energy:
        energy = Energy(user_id=current_user.id)
        db.add(energy)
        db.commit()
        db.refresh(energy)

    if energy.last_reset != date.today():
        energy.energy = 100
        energy.last_reset = date.today()
        db.commit()

    if energy.energy <= 0:
        return {"error": "Você está sem energia hoje 😴"}

    energy.energy -= 10
    db.commit()

    # 🔥 XP base por tarefa
    base_xp = task.difficulty * 5
    add_xp(current_user, base_xp, db)
    streak = update_streak(current_user, db)
    multiplier = get_streak_multiplier(streak)

    base_xp = task.difficulty * 5
    final_xp = int(base_xp * multiplier)
    xp_result = add_xp(current_user, final_xp, db)


    # 🔥 Atualizar missão baseada em tarefas
    update_mission_progress(current_user, db, "daily_tasks")

    db.commit()

    return {"message": "Task completed",
                       "energy_left":energy.energy,
                       "xp_result": xp_result
}

