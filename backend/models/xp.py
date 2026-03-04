from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from backend.database.base import Base

class XPProgress(Base):
    __tablename__ = "xp_progress"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    total_xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    current_level_xp = Column(Integer, default=0)
    next_level_xp = Column(Integer, default=100)

    user = relationship("User", back_populates="xp")