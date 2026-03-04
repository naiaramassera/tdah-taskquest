from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from backend.database.base import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    missed_days = Column(Integer, default=0)

    wallet = relationship("UserWallet", back_populates="user", uselist=False)
    xp = relationship("XPProgress", back_populates="user", uselist=False)
    streak = relationship("Streak", back_populates="user", uselist=False)
    skins = relationship("UserSkin", back_populates="user")