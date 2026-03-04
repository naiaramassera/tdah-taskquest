from datetime import date, timedelta
from backend.models.streak import Streak

def update_streak(user, db):
    today = date.today()

    streak = db.query(Streak).filter_by(user_id=user.id).first()

    if not streak:
        streak = Streak(
            user_id=user.id,
            current_streak=1,
            longest_streak=1,
            last_last_active_date=today
        )
        db.add(streak)
        db.commit()
        db.refresh(streak)
        return {"current_streak": 1, "longest_streak": 1}

    if streak.last_completed == today:
        return {"message": "Streak já contabilizado hoje"}

    if streak.last_active_date == today - timedelta(days=1):
        streak.current_streak += 1
        user.missed_days = 0

        streak.last_active_date = today
        streak.completed = True

    elif streak.last_active_date < today - timedelta(days=1):

        user.missed_days += 1

        if streak.shield_available:
            streak.shield_available = False

            # streak mantido
        else:
            streak.current_streak = 1

    streak.last_active_date= today

    if streak.current_streak > streak.best_streak:
        streak.best_streak = streak.current_streak

    db.commit()

def get_mascot_stage(streak):
    if streak >= 15:
        return "legendary"
    elif streak >= 8:
        return "warrior"
    elif streak >= 4:
        return "confident"
    else:
        return "beginner"


def unlock_skins(user, db, streak_value):

    skins = db.query(Skin).all()

    for skin in skins:
        if streak_value >= skin.required_streak:
            exists = db.query(UserSkin).filter(
                UserSkin.user_id == user.id,
                UserSkin.skin_id == skin.id
            ).first()

            if not exists:
                db.add(UserSkin(user_id=user.id, skin_id=skin.id))

    db.commit()

def get_mascot_stage(streak):

      if streak >= 15:
        return "legendary"
      elif streak >= 8:
        return "warrior"
      elif streak >= 4:
        return "confident"
      else:
        return "beginner"

