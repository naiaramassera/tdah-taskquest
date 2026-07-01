from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text

from backend.database.base import Base
from backend.database.session import engine
from backend.models.achievements import Achievement
from backend.models.daily_task import DailyTask
from backend.models.energy import Energy
from backend.models.focus_session import FocusSession
from backend.models.mission import Mission
from backend.models.profession import Profession
from backend.models.profession_mission import ProfessionMission
from backend.models.routine_task import RoutineTask
from backend.models.skins import Skin
from backend.models.streak import Streak
from backend.models.task import Task
from backend.models.user import User
from backend.models.user_achievement import UserAchievement
from backend.models.user_mission import UserMission
from backend.models.user_skin import UserSkin
from backend.models.user_wallet import UserWallet
from backend.models.world import World
from backend.models.xp import XPProgress
from backend.routes import achievements, auth, daily_tasks, focus, home
from backend.routes import missions, routines, skins, store, streak, task, users, worlds
from backend.routes import professions
from backend.routes.personal_world import router_personal
from backend.routes import boss as boss_router
from backend.models.user_combo import UserCombo
from backend.models.world_boss_progress import WorldBossProgress

Base.metadata.create_all(bind=engine)


def ensure_sqlite_columns():
    inspector = inspect(engine)
    table_names = inspector.get_table_names()

    with engine.begin() as connection:
        if "user_skins" in table_names:
            columns = {col["name"] for col in inspector.get_columns("user_skins")}
            if "price" not in columns:
                connection.execute(text("ALTER TABLE user_skins ADD COLUMN price INTEGER DEFAULT 0"))
            if "unlock_type" not in columns:
                connection.execute(text("ALTER TABLE user_skins ADD COLUMN unlock_type VARCHAR"))
            if "unlock_value" not in columns:
                connection.execute(text("ALTER TABLE user_skins ADD COLUMN unlock_value INTEGER"))

        if "users" in table_names:
            columns = {col["name"] for col in inspector.get_columns("users")}
            if "profession_id" not in columns:
                connection.execute(text("ALTER TABLE users ADD COLUMN profession_id INTEGER"))
            if "username" not in columns:
                connection.execute(text("ALTER TABLE users ADD COLUMN username VARCHAR"))

        if "worlds" in table_names:
            columns = {col["name"] for col in inspector.get_columns("worlds")}
            if "world_type" not in columns:
                connection.execute(text("ALTER TABLE worlds ADD COLUMN world_type VARCHAR DEFAULT 'custom'"))

        if "routine_tasks" in table_names:
            columns = {col["name"] for col in inspector.get_columns("routine_tasks")}
            if "time_limit_minutes" not in columns:
                connection.execute(text("ALTER TABLE routine_tasks ADD COLUMN time_limit_minutes INTEGER"))
            if "description" not in columns:
                connection.execute(text("ALTER TABLE routine_tasks ADD COLUMN description VARCHAR"))
            if "coin_reward" not in columns:
                connection.execute(text("ALTER TABLE routine_tasks ADD COLUMN coin_reward INTEGER DEFAULT 10"))
            if "xp_reward" not in columns:
                connection.execute(text("ALTER TABLE routine_tasks ADD COLUMN xp_reward INTEGER DEFAULT 15"))


ensure_sqlite_columns()


def run_seeds():
    """Roda seeds apenas se o banco estiver vazio (seguro para rodar sempre)."""
    from backend.database.session import SessionLocal
    from backend.models.profession import Profession as ProfessionModel
    from backend.models.achievements import Achievement as AchievementModel

    db = SessionLocal()
    try:
        if db.query(ProfessionModel).count() == 0:
            from backend.seed_professions import seed_professions
            seed_professions(db)

        if db.query(AchievementModel).count() == 0:
            from backend.seed_achievements import seed_achievements
            seed_achievements(db)
    finally:
        db.close()


run_seeds()

app = FastAPI(title="TaskQuest API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "TaskQuest API online"}


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(task.router, prefix="/tasks", tags=["Tasks"])
app.include_router(achievements.router, prefix="/achievements", tags=["Achievements"])
app.include_router(streak.router, prefix="/streak", tags=["Streak"])
app.include_router(store.router, prefix="/store", tags=["Store"])
app.include_router(focus.router, prefix="/focus", tags=["Focus"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(worlds.router, prefix="/worlds", tags=["Worlds"])
app.include_router(routines.router, prefix="/routines", tags=["Routines"])
app.include_router(daily_tasks.router, prefix="/daily", tags=["Daily Tasks"])
app.include_router(home.router)
app.include_router(missions.router)
app.include_router(skins.router)
app.include_router(professions.router, prefix="/professions", tags=["Professions"])
app.include_router(router_personal, prefix="/personal", tags=["Personal World"])
app.include_router(boss_router.router, tags=["Boss"])
