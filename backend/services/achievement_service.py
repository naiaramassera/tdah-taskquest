from backend.models.task import Task
from backend.models.achievements import Achievement
from backend.models.user_achievement import UserAchievement
from backend.services.xp_service import add_xp
from backend.services.skin_service import unlock_achievement_skins

def check_and_unlock_achievements(user, db):
    unlocked = []

    # Conta tarefas concluídas
    total_completed = db.query(Task).filter(
        Task.owner_id == user.id,
        Task.completed == True
    ).count()

    # 🥇 Primeira tarefa
    if total_completed >= 1:
        achievement = db.query(Achievement).filter_by(name="Primeiro Passo").first()

        if achievement and not user_has_achievement(user, achievement, db):
            unlock(user, achievement, db)
            unlocked.append(achievement)

    # 🔥 7 dias de streak
    if user.streak and user.streak.current_streak >= 7:
        achievement = db.query(Achievement).filter_by(name="Foco 7 Dias").first()

        if achievement and not user_has_achievement(user, achievement, db):
            unlock(user, achievement, db)
            unlocked.append(achievement)

    return unlocked

def user_has_achievement(user, achievement, db):
    return db.query(UserAchievement).filter_by(
        user_id=user.id,
        achievement_id=achievement.id
    ).first()


def unlock(user, achievement, db):
    user_achievement = UserAchievement(
        user_id=user.id,
        achievement_id=achievement.id
    )
    db.add(user_achievement)
    unlock_achievement_skins(user, achievement.id, db)

    # Dá XP bônus
    add_xp(achievement.xp_reward, user)