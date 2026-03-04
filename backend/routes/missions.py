from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.core.dependencies import get_current_user
from backend.models.mission import Mission
from backend.models.user_mission import UserMission
from backend.services.mission_reset_service import reset_missions_if_needed

router = APIRouter(prefix="/missions", tags=["Missions"])


@router.post("/assign")
def assign_missions(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    missions = db.query(Mission).all()

    assigned = []

    for mission in missions:
        exists = db.query(UserMission).filter_by(
            user_id=current_user.id,
            mission_id=mission.id
        ).first()

        if not exists:
            new_user_mission = UserMission(
                user_id=current_user.id,
                mission_id=mission.id,
                progress=0,
                completed=False
            )

            db.add(new_user_mission)
            assigned.append(mission.name)

    db.commit()

    return {"assigned_missions": assigned}

@router.get("/")
def get_user_missions(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    user_missions = (
        db.query(UserMission)
        .join(Mission)
        .filter(UserMission.user_id == current_user.id)
        .all()
    )

    result = []

    reset_missions_if_needed(current_user, db)

    for um in user_missions:
        percentage = 0

        if um.mission.goal and um.mission.goal > 0:
            percentage = int((um.progress / um.mission.goal) * 100)

        result.append({
            "id": um.id,
            "name": um.mission.name,
            "description": um.mission.description,
            "progress": um.progress,
            "goal": um.mission.goal,
            "percentage": percentage,
            "xp_reward": um.mission.xp_reward,
            "completed": um.completed
        })

    result = {
        "daily": [],
        "weekly": [],
        "achievements": []
    }

    for um in user_missions:
        percentage = 0

        if um.mission.goal and um.mission.goal > 0:
            percentage = int((um.progress / um.mission.goal) * 100)

        mission_data = {
            "id": um.id,
            "name": um.mission.name,
            "description": um.mission.description,
            "progress": um.progress,
            "goal": um.mission.goal,
            "percentage": percentage,
            "xp_reward": um.mission.xp_reward,
            "completed": um.completed
        }

        if um.mission.mission_type == "daily_tasks":
            result["daily"].append(mission_data)

        elif um.mission.mission_type == "weekly_tasks":
            result["weekly"].append(mission_data)

        else:
            result["achievements"].append(mission_data)



    return result