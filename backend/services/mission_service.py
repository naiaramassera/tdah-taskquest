from backend.models.mission import Mission
from backend.models.user_mission import UserMission
from backend.services.xp_service import add_xp

def update_mission_progress(user: object, db: object, mission_type: object) -> None:

    missions = (
        db.query(UserMission)
        .join(Mission)
        .filter(
            UserMission.user_id == user.id,
            Mission.mission_type == mission_type,
            UserMission.completed == False
        )
        .all()
    )

    for user_mission in missions:
        user_mission.progress += 1

        if user_mission.progress >= user_mission.mission.goal:
            user_mission.completed = True
            add_xp(user, user_mission.mission.xp_reward, db)

    db.commit()


def update_missions_on_task_complete(user,db):

    user_missions = db.query(UserMission).filter_by(
        user_id=user.id,
        completed=False
    ).all()

    for mission in user_missions:
        mission.progress += 1

        if mission.progress >= mission.mission.goal:
            mission.completed = True

    db.commit()

