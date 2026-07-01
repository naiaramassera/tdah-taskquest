from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.core.dependencies import get_current_user
from backend.models.profession import Profession
from backend.models.profession_mission import ProfessionMission
from backend.models.world import World
from backend.models.routine_task import RoutineTask

router = APIRouter(tags=["Professions"])


@router.get("/")
def list_professions(db: Session = Depends(get_db)):
    professions = db.query(Profession).order_by(Profession.category, Profession.name).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "icon": p.icon,
            "category": p.category,
            "description": p.description,
        }
        for p in professions
    ]


@router.get("/{profession_id}/missions")
def get_profession_missions(
    profession_id: int,
    db: Session = Depends(get_db),
):
    profession = db.query(Profession).filter_by(id=profession_id).first()
    if not profession:
        raise HTTPException(status_code=404, detail="Profissão não encontrada")

    missions = db.query(ProfessionMission).filter_by(profession_id=profession_id).all()
    return {
        "profession": {"id": profession.id, "name": profession.name, "icon": profession.icon},
        "missions": [
            {
                "id": m.id,
                "title": m.title,
                "description": m.description,
                "difficulty": m.difficulty,
                "coin_reward": m.coin_reward,
                "xp_reward": m.xp_reward,
                "suggested_minutes": m.suggested_minutes,
            }
            for m in missions
        ],
    }


@router.post("/select/{profession_id}")
def select_profession(
    profession_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    profession = db.query(Profession).filter_by(id=profession_id).first()
    if not profession:
        raise HTTPException(status_code=404, detail="Profissão não encontrada")

    current_user.profession_id = profession_id
    db.commit()

    # Cria o mundo profissional automaticamente se não existir
    prof_world = db.query(World).filter_by(
        user_id=current_user.id, world_type="professional"
    ).first()
    if not prof_world:
        prof_world = World(
            user_id=current_user.id,
            name=f"Trabalho — {profession.name}",
            icon=profession.icon,
            color="#4F46E5",
            description=f"Missões da sua profissão: {profession.name}",
            world_type="professional",
        )
        db.add(prof_world)
        db.commit()
        db.refresh(prof_world)

        # Popula mundo profissional com missões da profissão como rotinas
        missions = db.query(ProfessionMission).filter_by(profession_id=profession_id).all()
        for m in missions:
            routine = RoutineTask(
                world_id=prof_world.id,
                title=m.title,
                description=m.description,
                difficulty=m.difficulty,
                time_limit_minutes=m.suggested_minutes,
                coin_reward=m.coin_reward,
                xp_reward=m.xp_reward,
            )
            db.add(routine)
        db.commit()

    return {
        "message": f"Profissão {profession.name} selecionada!",
        "profession": {"id": profession.id, "name": profession.name, "icon": profession.icon},
        "world_id": prof_world.id,
    }


@router.get("/me")
def my_profession(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if not current_user.profession_id:
        return {"profession": None}

    profession = db.query(Profession).filter_by(id=current_user.profession_id).first()
    if not profession:
        return {"profession": None}

    return {
        "profession": {
            "id": profession.id,
            "name": profession.name,
            "icon": profession.icon,
            "category": profession.category,
        }
    }
