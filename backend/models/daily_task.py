from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from datetime import date
from backend.database.base import Base


class DailyTask(Base):
    __tablename__ = "daily_tasks"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    world_id = Column(Integer, ForeignKey("worlds.id"))

    title = Column(String, nullable=False)
    difficulty = Column(Integer)
    xp_reward = Column(Integer, default=20)
    completed = Column(Boolean, default=False)
    created_date = Column(Date, default=date.today)

    world = relationship("World")
