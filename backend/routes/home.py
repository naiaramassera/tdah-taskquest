from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.schemas.home import HomeResponse
from backend.database.session import get_db
from backend.routes.auth import get_current_user
from backend.models.user import User
from backend.models.xp import XPProgress
from backend.models.user_mission import UserMission
from backend.models.daily_task import DailyTask
from backend.models.streak import Streak
from backend.services.motivation_service import get_motivation
from backend.models.user_wallet import UserWallet

router = APIRouter(prefix="/home", tags=["Home"])


@router.get("/", response_model=HomeResponse)
def get_home(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    xp = db.query(XPProgress).filter_by(user_id=current_user.id).first()


    missions = db.query(UserMission).filter_by(
        user_id=current_user.id
    ).all()

    daily_tasks = db.query(DailyTask).filter_by(
        user_id=current_user.id
    ).all()

    streak = db.query(Streak).filter_by(
        user_id=current_user.id
    ).first()

    wallet = db.query(UserWallet).filter_by(user_id=current_user.id).first()

    return dict(daily_tasks=[
        {
            "id": task.id,
            "title": task.title,
            "completed": task.completed,
            "xp_reward": task.xp_reward
        }
        for task in daily_tasks
    ], missions=[
        {
            "id": mission.id,
            "progress": mission.progress,
            "completed": mission.completed
        }
        for mission in missions
    ], xp={
        "total_xp": xp.total_xp if xp else 0,
        "level": xp.level if xp else 1,
        "current_level_xp": xp.current_level_xp if xp else 0,
        "next_level_xp": xp.next_level_xp if xp else 100
    }, streak={
        "current_streak": streak.current_streak if streak else 0,
        "shield_available": streak.shield_available if streak else False
    }, motivation=get_motivation(current_user), coins=wallet.coins if wallet else 0)