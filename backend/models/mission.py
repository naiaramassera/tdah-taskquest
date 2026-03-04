from sqlalchemy import Column, Integer, String
from backend.database.base import Base

class Mission(Base):
    __tablename__ = "missions"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    mission_type = Column(String)
    goal = Column(Integer)
    xp_reward = Column(Integer)