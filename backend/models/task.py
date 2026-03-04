from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from backend.database.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    xp_reward = Column(Integer, default=10)
    completed = Column(Boolean, default=False)

    difficulty = Column(String, default="easy")

    owner_id = Column(Integer, ForeignKey("users.id"))