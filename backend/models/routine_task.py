from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from backend.database.base import Base


class RoutineTask(Base):
    __tablename__ = "routine_tasks"

    id = Column(Integer, primary_key=True, index=True)

    world_id = Column(Integer, ForeignKey("worlds.id"))
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    difficulty = Column(Integer, default=1)  # 1=leve, 2=média, 3=difícil
    is_active = Column(Boolean, default=True)
    time_limit_minutes = Column(Integer, nullable=True)  # tempo limite em minutos
    coin_reward = Column(Integer, default=10)
    xp_reward = Column(Integer, default=15)

    world = relationship("World")
