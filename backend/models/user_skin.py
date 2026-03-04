from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from backend.database.base import Base

class UserSkin(Base):
    __tablename__ = "user_skins"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    skin_name = Column(String, nullable=False)
    rarity = Column(String, default="common")
    unlocked = Column(Boolean, default=False)
    equipped = Column(Boolean, default=False)
    price = Column(Integer, default=0)
    unlock_type = Column(String)  # coins | level | achievement
    unlock_value = Column(Integer)

    user = relationship("User", back_populates="skins")