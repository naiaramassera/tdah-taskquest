from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.core.dependencies import get_current_user
from backend.models.xp import XPProgress
from backend.models.user import User

router = APIRouter()

@router.get("/me/progress")
def get_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    xp = db.query(XPProgress).filter_by(user_id=current_user.id).first()

    if not xp:
        return {
            "level": 1,
            "xp": 0,
            "xp_next_level": 100
        }

    return {
        "level": xp.level,
        "xp": xp.current_level_xp,
        "xp_next_level": xp.next_level_xp
    }