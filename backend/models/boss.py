from sqlalchemy import Column, Integer, String, Boolean
from backend.database.base import Base


class Boss(Base):
    __tablename__ = "bosses"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    required_tasks = Column(Integer)
    reward_xp = Column(Integer)
    active = Column(Boolean, default=True)