from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from backend.database.base import Base


class WorldBossProgress(Base):
    __tablename__ = "world_boss_progress"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    world_id = Column(Integer, ForeignKey("worlds.id"))
    stage = Column(Integer, default=1)           # estágio atual do chefão
    tasks_in_stage = Column(Integer, default=0)  # progresso no estágio atual
    total_defeated = Column(Integer, default=0)  # total de chefões derrotados

    user = relationship("User")
    world = relationship("World")
