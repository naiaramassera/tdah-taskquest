from sqlalchemy import Column, Integer, ForeignKey
from backend.database.base import Base


class GuildMember(Base):
    __tablename__ = "guild_members"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    guild_id = Column(Integer, ForeignKey("guilds.id"))