from typing import Any
from backend.services.skin_service import unlock_level_skins
from backend.models.xp import XPProgress
from sqlalchemy.orm import Session
from datetime import date

def get_streak_multiplier(streak):
    today = date.today().weekday()

    if today in [5,6]:
        return 2
    if streak >= 15:
        return 2
    elif streak >= 8:
        return 1.5
    elif streak >= 4:
        return 1.2
    else:
        return 1

def add_xp(user: object, xp: object, db: object) -> dict[str, int | bool | None | Any]:
    """

    :rtype: dict[str, int | bool | None | Any]
    """
    recovery_bonus = 0

    if user.missed_days >= 1:
        recovery_bonus = 20

    total_xp = xp + recovery_bonus

    user.xp.total_xp+= total_xp
    user.xp.current_level_xp += total_xp

    level_up = False

    if user.xp.current_level_xp>= user.xp.next_level_xp:
        user.xp.level += 1
        user.xp.current_level_xp = 0
        user.xp.next_level_xp += 50
        level_up = True

    unlock_level_skins(user, db)
    new_skins = unlock_level_skins(user, db)

    db.commit()

    return {
        "recovery_bonus": recovery_bonus,
        "level_up": level_up,
        "new_level": user.xp.level if level_up else None,
        "unlocked_skins": new_skins
}

def xp_needed_for_next_level(level: int) -> int:
    # Fórmula simples de progressão
    return 100 + (level * 50)


def get_event_multiplier():
    today = date.today().weekday()

    # 5 = sábado, 6 = domingo
    if today in [5, 6]:
        return 2
    return 1





