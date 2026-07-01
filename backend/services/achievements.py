from backend.models.task import Task


def check_achievements(user, db):
    unlocked = []

    if user.xp and user.xp.level >= 5:
        unlocked.append("Subiu para nivel 5!")

    total_completed = db.query(Task).filter(
        Task.owner_id == user.id,
        Task.completed == True,
    ).count()

    if total_completed > 50:
        unlocked.append("Concluiu mais de 50 tarefas!")

    return unlocked
