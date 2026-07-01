from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from backend.core.security import ALGORITHM, SECRET_KEY
from backend.core.security import create_access_token, hash_password, verify_password
from backend.database.session import get_db
from backend.models.mission import Mission
from backend.models.skins import Skin
from backend.models.streak import Streak
from backend.models.user import User
from backend.models.user_mission import UserMission
from backend.models.user_skin import UserSkin
from backend.models.user_wallet import UserWallet
from backend.models.xp import XPProgress
from backend.schemas.user import UserCreate
from backend.services.motivation_service import get_motivation

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
router = APIRouter()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Credenciais invalidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email ja cadastrado")

    new_user = User(
        email=user.email,
        password_hash=hash_password(user.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    db.add(XPProgress(user_id=new_user.id))
    db.add(Streak(user_id=new_user.id))
    db.add(UserWallet(user_id=new_user.id, coins=0))

    catalog_skins = db.query(Skin).all()
    if not catalog_skins:
        catalog_skins = [
            Skin(name="Kiara Classica", price=0),
            Skin(name="Foco Azul", price=120),
            Skin(name="Dourada", price=250),
        ]
        db.add_all(catalog_skins)
        db.flush()

    for index, skin in enumerate(catalog_skins):
        db.add(UserSkin(
            user_id=new_user.id,
            skin_name=skin.name,
            rarity="common" if index == 0 else "rare",
            unlocked=index == 0 or (skin.price or 0) == 0,
            equipped=index == 0,
            price=skin.price or 0,
            unlock_type="coins",
            unlock_value=skin.price or 0,
        ))

    for mission in db.query(Mission).all():
        db.add(UserMission(
            user_id=new_user.id,
            mission_id=mission.id,
            progress=0,
            completed=False,
        ))

    db.commit()

    return {"message": "Usuario criado com sucesso"}


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    db_user = db.query(User).filter(User.email == form_data.username).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Usuario nao encontrado")

    if not verify_password(form_data.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Senha invalida")

    token = create_access_token({"sub": str(db_user.id)})

    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
def read_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "level": current_user.xp.level,
        "xp": current_user.xp.total_xp,
        "xp_next_level": current_user.xp.next_level_xp,
        "motivation": get_motivation(current_user),
    }
