from sqlalchemy import Column, Integer, ForeignKey, Date
from datetime import date
from backend.database.base import Base


class Energy(Base):
    __tablename__ = "energy"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    energy = Column(Integer, default=100)
    last_reset = Column(Date, default=date.today)

