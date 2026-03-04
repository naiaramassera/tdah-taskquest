from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import auth, task, achievements, streak, store, missions, focus, users
from backend.models.user import User
from backend.models.task import Task
from backend.database.base import Base
from backend.database.session import engine
from backend.routes.task import router as task_router
from backend.models.achievements import Achievement
from backend.models.xp import XPProgress
from backend.models.streak import Streak
from backend.models.user_achievement import UserAchievement
from backend.models.skins import Skin
from backend.models.mission import Mission
from backend.models.user_mission import UserMission
from backend.routes import missions
from backend.routes import worlds
from backend.routes import routines
from backend.routes import daily_tasks
from backend.routes import streak
from backend.routes import focus
from backend.routes import home
from backend.routes import skins

Base.metadata.create_all(bind=engine)

print(Base.metadata.tables.keys())

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Root
@app.get("/")
def root():
    return {"message": "TaskQuest API online"}

@app.get("/health")
def health():
    return {"status": "ok"}

# ROUTES
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(task.router, prefix="/tasks", tags=["Tasks"])
app.include_router(achievements.router, prefix="/achievements", tags=["Achievements"])
app.include_router(streak.router, prefix="/streak", tags=["Streak"])
app.include_router(store.router, prefix="/store", tags=["Store"])
app.include_router(missions.router, prefix="/missions", tags=["Missions"])
app.include_router(focus.router, prefix="/focus", tags=["Focus"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(missions.router, prefix="/missions", tags=["Missions"])
app.include_router(worlds.router, prefix="/worlds")
app.include_router(routines.router, prefix="/routines")
app.include_router(daily_tasks.router, prefix="/daily")
app.include_router(streak.router, prefix="/streak")
app.include_router(home.router)
app.include_router(skins.router)