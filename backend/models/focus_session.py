from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime
from datetime import datetime
from backend.database.base import Base


class FocusSession(Base):
    __tablename__ = "focus_sessions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    task_id = Column(Integer, ForeignKey("daily_tasks.id"))

    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)

    completed = Column(Boolean, default=False)