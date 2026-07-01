from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.core.dependencies import get_current_user
from backend.database.session import get_db
from backend.models.daily_task import DailyTask
from backend.models.energy import Energy
from backend.models.streak import Streak
from backend.models.world import World
from backend.services.daily_generator_service import generate_daily_tasks
from backend.services.economy_service import add_coins
from backend.services.mission_service import update_mission_progress
from backend.services.streak_service import update_streak
from backend.services.xp_service import add_xp, get_streak_multiplier
from backend.services.combo_service import update_combo

router = APIRouter(tags=["Daily Tasks"])


@router.post("/generate")
def generate_tasks(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return generate_daily_tasks(current_user, db)


@router.get("/")
def list_today_tasks(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    today = date.today()

    return (
        db.query(DailyTask)
        .join(World)
        .filter(
            DailyTask.user_id == current_user.id,
            DailyTask.created_date == today,
        )
        .all()
    )


@router.post("/complete/{task_id}")
def complete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    task = db.query(DailyTask).filter(
        DailyTask.id == task_id,
        DailyTask.user_id == current_user.id,
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.completed:
        raise HTTPException(status_code=400, detail="Already completed")

    energy = db.query(Energy).filter_by(user_id=current_user.id).first()
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
        raise HTTPException(status_code=400, detail="Voce esta sem energia hoje")

    task.completed = True
    energy.energy -= 10

    base_xp = task.difficulty * 5
    update_streak(current_user, db)
    streak = db.query(Streak).filter_by(user_id=current_user.id).first()
    streak_mult = get_streak_multiplier(streak.current_streak if streak else 0)

    combo_info = update_combo(current_user, db)
    coin_mult = streak_mult * combo_info["multiplier"]

    final_xp = int(base_xp * streak_mult)
    base_coins = 10 + (task.difficulty - 1) * 5 if hasattr(task, 'difficulty') and task.difficulty else 10
    final_coins = int(base_coins * coin_mult)

    xp_result = add_xp(current_user, final_xp, db)
    coins = add_coins(current_user, final_coins, db)

    update_mission_progress(current_user, db, "daily_tasks")
    db.commit()

    return {
        "message": "Task completed",
        "energy_left": energy.energy,
        "xp_result": xp_result,
        "xp_gained": final_xp,
        "coins": coins,
        "coins_gained": final_coins,
        "combo": combo_info,
    }
