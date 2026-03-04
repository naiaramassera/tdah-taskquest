from fastapi import APIRouter
from backend.models.skins import Skin
from backend.database.session import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

router = APIRouter()

@router.get("/skins")
def list_skins(db: Session = Depends(get_db)):
    return db.query(Skin).all()