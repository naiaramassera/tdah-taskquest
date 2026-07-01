from datetime import date, timedelta

from backend.models.streak import Streak


def update_streak(user, db):
    today = date.today()

    streak = db.query(Streak).filter_by(user_id=user.id).first()
    if not streak:
        streak = Streak(
            user_id=user.id,
            current_streak=1,
            best_streak=1,
            last_active_date=today,
        )
        db.add(streak)
        db.commit()
        db.refresh(streak)
        return streak

    if streak.last_active_date == today:
        return streak

    if streak.last_active_date == today - timedelta(days=1):
        streak.current_streak += 1
        user.missed_days = 0
    else:
        user.missed_days += 1
        if streak.shield_available:
            streak.shield_available = False
        else:
            streak.current_streak = 1

    streak.last_active_date = today

    if streak.current_streak > streak.best_streak:
        streak.best_streak = streak.current_streak

    db.commit()
    db.refresh(streak)
    return streak


def get_mascot_stage(streak):
    if streak >= 15:
        return "legendary"
    if streak >= 8:
        return "warrior"
    if streak >= 4:
        return "confident"
    return "beginner"


def unlock_skins(user, db, streak_value):
    from backend.models.skins import Skin
    from backend.models.user_skin import UserSkin

    skins = db.query(Skin).all()

    for skin in skins:
        if streak_value >= (skin.required_streak or 0):
            exists = db.query(UserSkin).filter(
                UserSkin.user_id == user.id,
                UserSkin.skin_name == skin.name,
            ).first()

            if not exists:
                db.add(UserSkin(
                    user_id=user.id,
                    skin_name=skin.name,
                    unlocked=True,
                    equipped=False,
                    price=skin.price or 0,
                    unlock_type="streak",
                    unlock_value=skin.required_streak or 0,
                ))

    db.commit()
