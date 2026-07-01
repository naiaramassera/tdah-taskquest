from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.database.base import Base


class ProfessionMission(Base):
    __tablename__ = "profession_missions"

    id = Column(Integer, primary_key=True, index=True)
    profession_id = Column(Integer, ForeignKey("professions.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    difficulty = Column(Integer, default=1)  # 1=leve, 2=média, 3=difícil
    coin_reward = Column(Integer, default=15)
    xp_reward = Column(Integer, default=20)
    suggested_minutes = Column(Integer, default=30)  # tempo sugerido em minutos

    profession = relationship("Profession", back_populates="missions")
