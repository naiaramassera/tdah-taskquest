from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.core.dependencies import get_current_user
from backend.models.streak import Streak
from backend.services.xp_service import get_streak_multiplier
from backend.services.streak_service import get_mascot_stage


router = APIRouter(tags=["Streak"])


@router.get("/")
def get_streak(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    streak = db.query(Streak).filter(
        Streak.user_id == current_user.id
    ).first()

    if not streak:
        return {
            "current_streak": 0,
            "best_streak": 0,
            "multiplier": 1,
            "next_bonus_in": 4,
            "level_badge": "🌱 Começando"
        }

    mascot_stage = get_mascot_stage(streak.current_streak)
    multiplier = get_streak_multiplier(streak.current_streak)

    # calcular próxima meta
    if streak.current_streak < 4:
        next_bonus = 4 - streak.current_streak
    elif streak.current_streak < 8:
        next_bonus = 8 - streak.current_streak
    elif streak.current_streak < 15:
        next_bonus = 15 - streak.current_streak
    else:
        next_bonus = 0

    # badge emocional
    if streak.current_streak >= 15:
        badge = "👑 Mestre do Foco"
    elif streak.current_streak >= 8:
        badge = "🔥 Foco Avançado"
    elif streak.current_streak >= 4:
        badge = "💪 Consistente"
    else:
        badge = "🌱 Começando"

    return dict(current_streak=streak.current_streak, best_streak=streak.best_streak, multiplier=multiplier,
                next_bonus_in=next_bonus, level_badge=badge, mascot_stage=mascot_stage)