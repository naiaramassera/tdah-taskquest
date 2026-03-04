from sqlalchemy import Column, Integer, ForeignKey, Date, Boolean
from datetime import date
from sqlalchemy.orm import relationship
from backend.database.base import Base

class Streak(Base):
    __tablename__ = "streaks"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"),
  unique=True)


    current_streak = Column(Integer, default=0)
    best_streak = Column(Integer, default=0)
    last_active_date = Column(Date, default=date.today)
    shield_available = Column(Boolean, default=True)

    user = relationship ("User", back_populates="streak")
