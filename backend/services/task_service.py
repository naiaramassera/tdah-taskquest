from backend.models.task import Task
from backend.services.streak_service import update_streak
from backend.services.xp_service import add_xp
from backend.services.achievement_service import check_and_unlock_achievements
from backend.services.mission_service import update_mission_progress

def complete_task(task: Task, user, db, update_missions_on_task_complete=None):

    # Marca como concluída
    task.completed = True

    # 🎯 XP vem da própria task (modelo Duolingo)
    xp_gain = task.xp_reward
    add_xp(user, xp_gain, db)

    from backend.services.mission_service import update_missions_on_task_complete
    update_missions_on_task_complete(user, db)
    update_mission_progress(user, db,"complete_tasks")

    unlocked = check_and_unlock_achievements(user, db)

    db.commit()
    db.refresh(user)
    db.refresh(task)

    add_xp(user, xp_gain, db)
    update_streak(user, db)
    check_and_unlock_achievements(user, db)

   #conta direto do banco
    total_completed = db.query(Task).filter(
        Task.owner_id == user.id,
        Task.completed == True
    ).count()

    return unlocked

