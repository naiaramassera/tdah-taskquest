from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.core.dependencies import get_current_user
from backend.models.world import World
from backend.services.boss_service import get_world_boss

router = APIRouter(tags=["Boss"])


@router.get("/worlds/{world_id}/boss")
def get_boss(
    world_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    world = db.query(World).filter_by(id=world_id, user_id=current_user.id).first()
    if not world:
        raise HTTPException(status_code=404, detail="Mundo não encontrado")
    return get_world_boss(current_user, world_id, db)


@router.get("/boss/all")
def get_all_bosses(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    worlds = db.query(World).filter_by(user_id=current_user.id).all()
    return [
        {"world_id": w.id, "world_name": w.name, **get_world_boss(current_user, w.id, db)}
        for w in worlds
    ]
