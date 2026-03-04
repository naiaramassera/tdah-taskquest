from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    xp_reward: int = 10


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    xp_reward: int
    completed: bool

    class Config:
        from_attributes = True
