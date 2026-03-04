from sqlalchemy import Column, Integer, ForeignKey
from backend.database.base import Base


class UserBossProgress(Base):
    __tablename__ = "user_boss_progress"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    boss_id = Column(Integer, ForeignKey("bosses.id"))

    tasks_completed = Column(Integer, default=0)
    completed = Column(Boolean, default=False)