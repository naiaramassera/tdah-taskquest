from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from backend.database.base import Base


class RoutineTask(Base):
    __tablename__ = "routine_tasks"

    id = Column(Integer, primary_key=True, index=True)

    world_id = Column(Integer, ForeignKey("worlds.id"))
    title = Column(String, nullable=False)

    difficulty = Column(Integer, default=1)  # 1 a 3
    is_active = Column(Boolean, default=True)

    world = relationship("World")
