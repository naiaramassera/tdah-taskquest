from sqlalchemy import Column, Integer, String
from backend.database.base import Base


class Guild(Base):
    __tablename__ = "guilds"

    id = Column(Integer, primary_key=True)
    name = Column(String)