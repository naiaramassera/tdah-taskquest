from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from backend.database.base import Base

class UserWallet(Base):
    __tablename__ = "user_wallets"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    coins = Column(Integer, default=0)

    user = relationship("User", back_populates="wallet")