from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.core.dependencies import get_current_user
from backend.models.xp import XPProgress
from backend.models.world import World
from backend.models.user_progress import User, UserProgress

router = APIRouter(tags=["Worlds"])


@router.post("/")
def create_world(name: str, icon: str, color: str,
                 db: Session = Depends(get_db),
                 current_user = Depends(get_current_user)):

    world = World(
        user_id=current_user.id,
        name=name,
        icon=icon,
        color=color
    )

    db.add(world)
    db.commit()
    db.refresh(world)

    return world


@router.get("/")
def get_world_map(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    worlds = db.query(World).all()

    progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id
    ).all()

    progress_dict = {p.world_id: p.current_level for p in progress}

    xp = db.query(XPProgress).filter_by(user_id=current_user.id).first()

    result = []

    for world in worlds:
        result.append({
            'world': world.name,
            'description': world.description,
            'current_level': progress_dict.get(world.id, 1),
            'locked': xp.level < world.required_level
        })
