from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.models.user_skin import UserSkin
from backend.routes.auth import get_current_user
from backend.models.user_wallet import UserWallet
from fastapi import HTTPException


router = APIRouter(prefix="/skins", tags=["Skins"])

@router.get("/")
def list_skins(db: Session = Depends(get_db),
               current_user = Depends(get_current_user)):
    skins = db.query(UserSkin).filter_by(user_id=current_user.id).all()
    return skins

@router.post("/buy/{skin_id}")
def buy_skin(skin_id: int,
             db: Session = Depends(get_db),
             current_user = Depends(get_current_user)):

    skin = db.query(UserSkin).filter_by(
        id=skin_id,
        user_id=current_user.id
    ).first()

    if not skin:
        raise HTTPException(status_code=404, detail="Skin não encontrada")

    if skin.unlocked:
        return {"message": "Skin já desbloqueada"}

    if skin.unlock_type != "coins":
        raise HTTPException(status_code=400, detail="Essa skin não é comprável")

    wallet = db.query(UserWallet).filter_by(
        user_id=current_user.id
    ).first()

    if not wallet or wallet.coins < skin.price:
        raise HTTPException(status_code=400, detail="Moedas insuficientes")

    wallet.coins -= skin.price
    skin.unlocked = True

    db.commit()

    return {
        "message": "Skin desbloqueada",
        "remaining_coins": wallet.coins
    }

@router.post("/equip/{skin_id}")
def equip_skin(skin_id: int,
               db: Session = Depends(get_db),
               current_user = Depends(get_current_user)):

    skins = db.query(UserSkin).filter_by(
        user_id=current_user.id
    ).all()

    for skin in skins:
        skin.equipped = False

    selected_skin = db.query(UserSkin).filter_by(
        id=skin_id,
        user_id=current_user.id
    ).first()

    if not selected_skin or not selected_skin.unlocked:
        raise HTTPException(status_code=400, detail="Skin não desbloqueada")

    selected_skin.equipped = True

    db.commit()

    return {"message": "Skin equipada com sucesso"}