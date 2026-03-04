from datetime import date
from backend.models.daily_task import DailyTask
from backend.models.routine_task import RoutineTask
from backend.models.world import World


def generate_daily_tasks(user, db):

    today = date.today()

    # Verifica se já existem tarefas hoje
    existing = db.query(DailyTask).filter(
        DailyTask.user_id == user.id,
        DailyTask.created_date == today
    ).first()

    if existing:
        return "Already generated"

    # Buscar todas rotinas ativas do usuário
    routines = (
        db.query(RoutineTask)
        .join(World)
        .filter(
            World.user_id == user.id,
            RoutineTask.is_active == True
        )
        .all()
    )

    for routine in routines:
        daily = DailyTask(
            user_id=user.id,
            world_id=routine.world_id,
            title=routine.title,
            difficulty=routine.difficulty
        )

        db.add(daily)

    db.commit()

    return "Daily tasks generated"
