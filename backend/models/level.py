from sqlalchemy import Column, Integer, ForeignKey
from backend.database.base import Base


class Level(Base):
    __tablename__ = "levels"

    id = Column(Integer, primary_key=True)
    world_id = Column(Integer, ForeignKey("worlds.id"))

    level_number = Column(Integer)
    required_xp = Column(Integer)