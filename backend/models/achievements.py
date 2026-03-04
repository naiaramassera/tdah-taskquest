from sqlalchemy import Column, Integer, String, ForeignKey
from backend.database.base import Base

class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    xp_reward = Column(Integer, default=0)
    rarity = Column(String, default="common")  # common, rare, epic, legendary


