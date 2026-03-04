from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.models.streak import Streak

router = APIRouter(tags=["Leaderboard"])


@router.get("/")
def global_ranking(db: Session = Depends(get_db)):

    ranking = db.query(Streak).order_by(
        Streak.current_streak.desc()
    ).limit(10).all()

    return [
        {
            "user_id": r.user_id,
            "streak": r.current_streak
        }
        for r in ranking
    ]