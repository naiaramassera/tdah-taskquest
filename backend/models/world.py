from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.database.base import Base


class World(Base):
    __tablename__ = "worlds"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    name = Column(String, nullable=False)
    icon = Column(String, nullable=True)  # emoji ou nome de ícone
    color = Column(String, nullable=True)
    description = Column(String)
    required_level = Column(Integer, default=1)

    user = relationship("User")