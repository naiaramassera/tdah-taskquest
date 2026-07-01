from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database.base import Base


class UserCombo(Base):
    __tablename__ = "user_combos"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    combo_count = Column(Integer, default=0)
    last_task_at = Column(DateTime, nullable=True)

    user = relationship("User")
