from pydantic import BaseModel

class AchievementResponse(BaseModel):
    name: str
    description: str
    xp_reward: int