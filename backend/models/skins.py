from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from backend.database.base import Base


class Skin(Base):
    __tablename__ = "skins"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    required_streak = Column(Integer)
    is_special = Column(Boolean, default=False)
    price = Column(Integer, default=0)