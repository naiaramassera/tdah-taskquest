from backend.models.world_boss_progress import WorldBossProgress
from backend.services.economy_service import add_coins
from backend.services.xp_service import add_xp
from backend.models.user_skin import UserSkin

# Estágios do chefão — cada mundo percorre esta sequência infinitamente
BOSS_STAGES = [
    {
        "stage": 1,
        "name": "Chefe Iniciante",
        "emoji": "👹",
        "description": "Um adversário fraco que subestima você.",
        "required_tasks": 10,
        "coin_reward": 50,
        "xp_reward": 100,
        "skin_reward": None,
    },
    {
        "stage": 2,
        "name": "Chefe Desafiador",
        "emoji": "🐲",
        "description": "Mais forte e determinado a te parar.",
        "required_tasks": 25,
        "coin_reward": 120,
        "xp_reward": 250,
        "skin_reward": None,
    },
    {
        "stage": 3,
        "name": "Chefe Poderoso",
        "emoji": "💀",
        "description": "Letal e implacável. Apenas os focados vencem.",
        "required_tasks": 50,
        "coin_reward": 250,
        "xp_reward": 500,
        "skin_reward": "Kiara Guerreira",
    },
    {
        "stage": 4,
        "name": "Chefe Lendário",
        "emoji": "👑",
        "description": "O mais poderoso. Derrotá-lo é um feito épico.",
        "required_tasks": 100,
        "coin_reward": 600,
        "xp_reward": 1200,
        "skin_reward": "Kiara Lendária",
    },
]


def get_stage_data(stage: int) -> dict:
    """Retorna dados do estágio (cicla após o último)."""
    idx = (stage - 1) % len(BOSS_STAGES)
    data = BOSS_STAGES[idx].copy()
    # Aumenta dificuldade em ciclos posteriores
    cycle = (stage - 1) // len(BOSS_STAGES)
    if cycle > 0:
        data["required_tasks"] = int(data["required_tasks"] * (1 + cycle * 0.5))
        data["coin_reward"] = int(data["coin_reward"] * (1 + cycle * 0.3))
        data["xp_reward"] = int(data["xp_reward"] * (1 + cycle * 0.3))
        data["name"] = f"{data['name']} +{cycle}"
    return data


def get_world_boss(user, world_id: int, db) -> dict:
    """Retorna estado atual do chefão de um mundo."""
    progress = db.query(WorldBossProgress).filter_by(
        user_id=user.id, world_id=world_id
    ).first()

    if not progress:
        progress = WorldBossProgress(
            user_id=user.id, world_id=world_id, stage=1, tasks_in_stage=0, total_defeated=0
        )
        db.add(progress)
        db.commit()

    stage_data = get_stage_data(progress.stage)
    hp_percent = 1.0 - (progress.tasks_in_stage / stage_data["required_tasks"])

    return {
        "stage": progress.stage,
        "tasks_in_stage": progress.tasks_in_stage,
        "required_tasks": stage_data["required_tasks"],
        "hp_percent": round(max(0.0, hp_percent), 3),
        "total_defeated": progress.total_defeated,
        "boss": {
            "name": stage_data["name"],
            "emoji": stage_data["emoji"],
            "description": stage_data["description"],
            "coin_reward": stage_data["coin_reward"],
            "xp_reward": stage_data["xp_reward"],
            "skin_reward": stage_data["skin_reward"],
        },
    }


def register_task_for_boss(user, world_id: int, db) -> dict | None:
    """Registra uma tarefa no progresso do chefão. Retorna dados de derrota se venceu."""
    progress = db.query(WorldBossProgress).filter_by(
        user_id=user.id, world_id=world_id
    ).first()

    if not progress:
        progress = WorldBossProgress(
            user_id=user.id, world_id=world_id, stage=1, tasks_in_stage=0, total_defeated=0
        )
        db.add(progress)

    progress.tasks_in_stage += 1
    stage_data = get_stage_data(progress.stage)

    if progress.tasks_in_stage >= stage_data["required_tasks"]:
        # Chefão derrotado!
        progress.total_defeated += 1
        defeated_boss = stage_data.copy()
        progress.stage += 1
        progress.tasks_in_stage = 0
        db.commit()

        # Dar recompensas
        add_coins(user, defeated_boss["coin_reward"], db)
        add_xp(user, defeated_boss["xp_reward"], db)

        # Desbloquear skin de recompensa se tiver
        if defeated_boss["skin_reward"]:
            existing = db.query(UserSkin).filter_by(
                user_id=user.id, skin_name=defeated_boss["skin_reward"]
            ).first()
            if not existing:
                skin = UserSkin(
                    user_id=user.id,
                    skin_name=defeated_boss["skin_reward"],
                    rarity="epic" if "Guerreira" in defeated_boss["skin_reward"] else "legendary",
                    unlocked=True,
                    equipped=False,
                    price=0,
                    unlock_type="boss",
                )
                db.add(skin)
                db.commit()

        return {
            "defeated": True,
            "boss_name": defeated_boss["name"],
            "boss_emoji": defeated_boss["emoji"],
            "coin_reward": defeated_boss["coin_reward"],
            "xp_reward": defeated_boss["xp_reward"],
            "skin_reward": defeated_boss["skin_reward"],
            "next_stage": progress.stage,
        }

    db.commit()
    return None
