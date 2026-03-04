from backend.database.session import SessionLocal
from backend.models.achievements import Achievement
from backend.models.skins import Skin
from backend.models.mission import Mission
from backend.database.base import Base
from backend.database.session import engine

Base.metadata.create_all(engine)

db = SessionLocal()

def seed_achievements():
    achievements = [
        {"name": "Primeiro Passo", "description": "Complete sua primeira tarefa"},
        {"name": "Foco 7 Dias", "description": "Mantenha streak de 7 dias"},
        {"name": "Produtividade Ninja", "description": "Complete 50 tarefas"},
        {"name": "Mestre do Foco", "description": "Alcance nível 5"},
        {"name": "Lenda TDAH", "description": "Alcance nível 10"},
    ]

    for data in achievements:
        exists = db.query(Achievement).filter_by(name=data["name"]).first()
        if not exists:
            db.add(Achievement(**data))

    db.commit()


def seed_skins():
    skins = [
        {"name": "Modo Dark Gamer", "price": 200},
        {"name": "Dourado Supremo", "price": 500},
        {"name": "Foco Azul Neon", "price": 350},
        {"name": "Minimalista Clean", "price": 150},
        {"name": "Lendário Roxo XP", "price": 800},
    ]

    for data in skins:
        exists = db.query(Skin).filter_by(name=data["name"]).first()
        if not exists:
            db.add(Skin(**data))

    db.commit()


def seed_missions():
    missions = [

        # 🟢 DIÁRIA
        {
            "name": "Produtividade Diária",
            "description": "Complete 5 tarefas hoje",
            "mission_type": "daily_tasks",
            "goal": 5,
            "xp_reward": 50
        },

        # 🔵 SEMANAL
        {
            "name": "Foco da Semana",
            "description": "Complete 20 tarefas na semana",
            "mission_type": "weekly_tasks",
            "goal": 20,
            "xp_reward": 150
        },

        # 🟣 CONQUISTA
        {
            "name": "Primeiros Passos",
            "description": "Complete 10 tarefas no total",
            "mission_type": "achievement_tasks",
            "goal": 10,
            "xp_reward": 100
        }
    ]

    for data in missions:
        exists = db.query(Mission).filter_by(name=data["name"]).first()
        if not exists:
            db.add(Mission(**data))

    db.commit()


def run_seed():
    print("🌱 Iniciando Seed...")
    seed_achievements()
    seed_skins()
    seed_missions()
    print("✅ Seed finalizado com sucesso!")


if __name__ == "__main__":
    run_seed()
    db.close()

missions = [
    {
        "name": "Organize sua mente",
        "description": "Complete 3 tarefas hoje",
        "mission_type": "tasks_completed",
        "goal": 3,
        "xp_reward": 20,
    },
]
