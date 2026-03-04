from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.database.session import get_db
from backend.models.user import User
from backend.schemas.user import UserCreate
from backend.core.security import hash_password, verify_password, create_access_token
from jose import JWTError, jwt
from fastapi import Depends
from backend.database.session import get_db
from backend.core.security import SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer
from backend.services.motivation_service import get_motivation

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=401,
        detail="Credenciais inválidas",
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

router = APIRouter()

from backend.models.xp import XPProgress

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    new_user = User(
        email=user.email,
        password_hash=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    xp_progress = XPProgress(user_id=new_user.id)
    db.add(xp_progress)
    db.commit()

    from backend.models.streak import Streak

    streak = Streak(user_id=new_user.id)
    db.add(streak)
    db.commit()

    from backend.services.mission_service import (
    assign_missions_to_user)

    return {"message": "Usuário criado com sucesso"}


from fastapi.security import OAuth2PasswordRequestForm

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.email == form_data.username).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")

    if not verify_password(form_data.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Senha inválida")

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
        "motivation": get_motivation(current_user)
    }