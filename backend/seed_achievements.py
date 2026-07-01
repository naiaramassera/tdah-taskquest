"""
Seed de conquistas.
Execute: python -m backend.seed_achievements
"""
from backend.database.base import Base
from backend.database.session import SessionLocal, engine
from backend.models.achievements import Achievement

Base.metadata.create_all(bind=engine)

ACHIEVEMENTS = [
    # Common
    ("Primeiro Passo", "Complete sua primeira tarefa", 50, "common"),
    ("Habito Formado", "Complete 10 tarefas", 100, "common"),
    ("Em Ritmo", "Complete 50 tarefas", 200, "common"),
    ("Foco no Dia", "Complete todas as tarefas de um dia", 75, "common"),
    # Rare
    ("Foco 7 Dias", "Mantenha uma sequencia de 7 dias", 300, "rare"),
    ("Centuriao", "Complete 100 tarefas", 500, "rare"),
    ("Subindo de Nivel", "Alcance o nivel 5", 250, "rare"),
    ("Rotineiro", "Conclua 20 rotinas", 200, "rare"),
    # Epic
    ("30 Dias de Fogo", "Mantenha uma sequencia de 30 dias", 1000, "epic"),
    ("Mestre das Tarefas", "Complete 200 tarefas", 800, "epic"),
    ("Nivel 10", "Alcance o nivel 10", 600, "epic"),
    ("Guerreiro do Foco", "Complete 50 sessoes de foco", 700, "epic"),
    # Legendary
    ("Lendario", "Mantenha uma sequencia de 100 dias", 3000, "legendary"),
    ("Imparavel", "Complete 500 tarefas", 2000, "legendary"),
    ("Nivel Maximo", "Alcance o nivel 20", 2500, "legendary"),
]


def seed_achievements(db=None):
    own_db = db is None
    if own_db:
        db = SessionLocal()
    try:
        existing = db.query(Achievement).count()
        if existing > 0:
            print(f"Conquistas ja existem ({existing}). Pulando seed.")
            return

        for name, desc, xp, rarity in ACHIEVEMENTS:
            db.add(Achievement(name=name, description=desc, xp_reward=xp, rarity=rarity))

        db.commit()
        print(f"OK: {len(ACHIEVEMENTS)} conquistas criadas.")
    finally:
        if own_db:
            db.close()


def seed():
    seed_achievements()


if __name__ == "__main__":
    seed()
