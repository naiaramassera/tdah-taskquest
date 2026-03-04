from pydantic import BaseModel
from typing import List, Optional


class XPResponse(BaseModel):
    total_xp: int
    level: int
    current_level_xp: int
    next_level_xp: int


class StreakResponse(BaseModel):
    current_streak: int
    shield_available: bool


class MissionResponse(BaseModel):
    id: int
    progress: int
    completed: bool


class DailyTaskResponse(BaseModel):
    id: int
    title: str
    completed: bool


class HomeResponse(BaseModel):
    daily_tasks: List[DailyTaskResponse]
    missions: List[MissionResponse]
    xp: XPResponse
    streak: Optional[StreakResponse]
    motivation: str