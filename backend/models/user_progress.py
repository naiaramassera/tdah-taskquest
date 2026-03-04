from sqlalchemy import Column, Integer, ForeignKey
from backend.database.base import Base


class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    world_id = Column(Integer, ForeignKey("worlds.id"))

    current_level = Column(Integer, default=1)


class User:
    pass