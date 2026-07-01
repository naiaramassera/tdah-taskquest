from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.core.dependencies import get_current_user
from backend.models.xp import XPProgress
from backend.models.user import User
from backend.models.achievements import Achievement
from backend.models.user_achievement import UserAchievement
from backend.models.streak import Streak
from backend.models.daily_task import DailyTask

router = APIRouter()


@router.get("/me/progress")
def get_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    xp = db.query(XPProgress).filter_by(user_id=current_user.id).first()
    if not xp:
        return {"level": 1, "xp": 0, "xp_next_level": 100}
    return {"level": xp.level, "xp": xp.current_level_xp, "xp_next_level": xp.next_level_xp}


@router.get("/me")
def get_my_achievements(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    all_achievements = db.query(Achievement).all()
    unlocked_ids = {
        ua.achievement_id
        for ua in db.query(UserAchievement).filter_by(user_id=current_user.id).all()
    }

    streak = db.query(Streak).filter_by(user_id=current_user.id).first()
    current_streak = streak.current_streak if streak else 0
    tasks_done = db.query(DailyTask).filter_by(user_id=current_user.id, completed=True).count()
    xp = db.query(XPProgress).filter_by(user_id=current_user.id).first()
    current_level = xp.level if xp else 1

    result = []
    for ach in all_achievements:
        unlocked = ach.id in unlocked_ids
        progress_value, progress_goal = _get_progress(ach, current_streak, tasks_done, current_level)

        result.append({
            "id": ach.id,
            "name": ach.name,
            "description": ach.description,
            "xp_reward": ach.xp_reward,
            "rarity": ach.rarity,
            "unlocked": unlocked,
            "progress": min(progress_value, progress_goal),
            "goal": progress_goal,
        })

    # Ordenar: desbloqueadas primeiro, depois por raridade
    rarity_order = {"legendary": 0, "epic": 1, "rare": 2, "common": 3}
    result.sort(key=lambda a: (not a["unlocked"], rarity_order.get(a["rarity"], 3)))
    return result


def _get_progress(achievement: Achievement, streak: int, tasks: int, level: int):
    name = achievement.name.lower()
    if "primeiro" in name or "first" in name or "1" in name:
        return tasks, 1
    if "7" in name and ("streak" in name or "foco" in name or "dias" in name):
        return streak, 7
    if "30" in name and "dias" in name:
        return streak, 30
    if "streak" in name or "sequencia" in name or "dias" in name:
        return streak, 7
    if "nivel" in name or "level" in name or "5" in name:
        return level, 5
    if "10" in name and ("tarefa" in name or "task" in name):
        return tasks, 10
    if "50" in name and ("tarefa" in name or "task" in name):
        return tasks, 50
    if "100" in name and ("tarefa" in name or "task" in name):
        return tasks, 100
    return tasks, max(tasks + 1, 1)
