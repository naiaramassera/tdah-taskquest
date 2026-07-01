from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.database.base import Base


class Profession(Base):
    __tablename__ = "professions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    icon = Column(String, nullable=False)
    category = Column(String, nullable=False)  # saude, negocios, tecnologia, educacao, outros
    description = Column(String)

    missions = relationship("ProfessionMission", back_populates="profession")
