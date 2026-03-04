from datetime import date, timedelta
from backend.models.user_mission import UserMission
from backend.models.mission import Mission

def reset_missions_if_needed(user: object, db: object) -> None:
    """

    :rtype: None
    """
    today = date.today()

    user_missions = (
        db.query(UserMission)
        .join(Mission)
        .filter(UserMission.user_id == user.id)
        .all()
    )

    for um in user_missions:

        # 🟢 Reset diário
        if um.mission.mission_type == "daily_tasks":
            if um.last_reset != today:
                um.progress = 0
                um.completed = False
                um.last_reset = today

        # 🔵 Reset semanal (segunda-feira)
        elif um.mission.mission_type == "weekly_tasks":
            start_of_week = today - timedelta(days=today.weekday())

            if um.last_reset < start_of_week:
                um.progress = 0
                um.completed = False
                um.last_reset = today

        user.streak.shield_available = True

    db.commit()