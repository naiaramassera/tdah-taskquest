from sqlalchemy import Column, Integer, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from backend.database.base import Base
from datetime import date

class UserMission(Base):
    __tablename__ = "user_missions"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    mission_id = Column(Integer, ForeignKey("missions.id"))

    progress = Column(Integer, default=0)
    goal = Column(Integer, default=1)
    completed = Column(Boolean, default=False)

    last_reset = Column(Date, default=date.today)

    mission = relationship("Mission")