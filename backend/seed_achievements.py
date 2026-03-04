from backend.database.session import SessionLocal
from backend.models.achievements import Achievement

db = SessionLocal()

achievements = [
    {
        "name": "Primeiro Passo",
        "description": "Concluiu sua primeira tarefa",
        "xp_reward": 20,
        "rarity": "comum"
    },
    {
        "name": "Foco 7 Dias",
        "description": "7 dias consecutivos ativo",
        "xp_reward": 50,
        "rarity": "raro"
    }
]

for ach in achievements:
    exists = db.query(Achievement).filter_by(name=ach["name"]).first()
    if not exists:
        db.add(Achievement(**ach))

db.commit()
db.close()

print("Conquistas criadas com sucesso!")