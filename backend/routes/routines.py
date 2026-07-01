from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.core.dependencies import get_current_user
from backend.models.routine_task import RoutineTask
from backend.models.world import World
from backend.services.economy_service import add_coins
from backend.services.xp_service import add_xp, get_streak_multiplier
from backend.models.streak import Streak
from backend.services.streak_service import update_streak
from backend.services.combo_service import update_combo
from backend.services.boss_service import register_task_for_boss

router = APIRouter(tags=["Routines"])


@router.post("/{world_id}")
def create_routine_task(
    world_id: int,
    title: str,
    difficulty: int = 1,
    time_limit_minutes: int = None,
    description: str = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    world = db.query(World).filter(
        World.id == world_id,
        World.user_id == current_user.id,
    ).first()

    if not world:
        raise HTTPException(status_code=404, detail="Mundo não encontrado")

    coin_reward = 10 + (difficulty - 1) * 5   # 10, 15, 20
    xp_reward = 15 + (difficulty - 1) * 10    # 15, 25, 35

    routine = RoutineTask(
        world_id=world_id,
        title=title,
        description=description,
        difficulty=difficulty,
        time_limit_minutes=time_limit_minutes,
        coin_reward=coin_reward,
        xp_reward=xp_reward,
    )

    db.add(routine)
    db.commit()
    db.refresh(routine)
    return routine


@router.get("/{world_id}")
def list_routines(
    world_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return db.query(RoutineTask).join(World).filter(
        World.user_id == current_user.id,
        RoutineTask.world_id == world_id,
    ).all()


@router.get("/")
def list_all_routines(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return db.query(RoutineTask).join(World).filter(
        World.user_id == current_user.id,
    ).all()


@router.post("/{routine_id}/complete")
def complete_routine(
    routine_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    routine = db.query(RoutineTask).join(World).filter(
        RoutineTask.id == routine_id,
        World.user_id == current_user.id,
    ).first()

    if not routine:
        raise HTTPException(status_code=404, detail="Rotina não encontrada")

    update_streak(current_user, db)
    streak = db.query(Streak).filter_by(user_id=current_user.id).first()
    streak_mult = get_streak_multiplier(streak.current_streak if streak else 0)

    combo_info = update_combo(current_user, db)
    coin_mult = streak_mult * combo_info["multiplier"]

    final_xp = int(routine.xp_reward * streak_mult)
    final_coins = int(routine.coin_reward * coin_mult)

    xp_result = add_xp(current_user, final_xp, db)
    coins_result = add_coins(current_user, final_coins, db)

    boss_defeat = register_task_for_boss(current_user, routine.world_id, db)

    db.commit()

    return {
        "message": "Rotina concluída!",
        "xp_gained": final_xp,
        "coins_gained": final_coins,
        "xp_result": xp_result,
        "coins_total": coins_result,
        "streak_multiplier": streak_mult,
        "combo": combo_info,
        "boss_defeat": boss_defeat,
    }


@router.patch("/{routine_id}/toggle")
def toggle_routine(
    routine_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    routine = db.query(RoutineTask).join(World).filter(
        RoutineTask.id == routine_id,
        World.user_id == current_user.id,
    ).first()

    if not routine:
        raise HTTPException(status_code=404, detail="Rotina não encontrada")

    routine.is_active = not routine.is_active
    db.commit()
    db.refresh(routine)
    return routine


@router.delete("/{routine_id}")
def delete_routine(
    routine_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    routine = db.query(RoutineTask).join(World).filter(
        RoutineTask.id == routine_id,
        World.user_id == current_user.id,
    ).first()

    if not routine:
        raise HTTPException(status_code=404, detail="Rotina não encontrada")

    db.delete(routine)
    db.commit()
    return {"message": "Rotina removida"}
