from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.services.economy_service import add_coins

from backend.database.session import get_db
from backend.core.dependencies import get_current_user
from backend.models.user import User
from backend.models.task import Task
from backend.schemas.task import TaskCreate, TaskResponse
from backend.services.task_service import complete_task


router = APIRouter(
    tags=["Tasks"]
)

# ======================================================
# CRIAR TAREFA
# ======================================================

@router.post("/", response_model=TaskResponse)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        xp_reward=task_data.xp_reward,
        owner_id=current_user.id,
        completed=False,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# ======================================================
# LISTAR TAREFAS DO USUÁRIO LOGADO
# ======================================================

@router.get("/", response_model=List[TaskResponse])
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tasks = (
        db.query(Task)
        .filter(Task.owner_id == current_user.id)
        .all()
    )

    return tasks


# ======================================================
# COMPLETAR TAREFA
# ======================================================

@router.patch("/{task_id}/complete")
def complete_task_endpoint(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.owner_id == current_user.id,
        )
        .first()
    )

    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    if task.completed:
        raise HTTPException(status_code=400, detail="Tarefa já concluída")

    unlocked = complete_task(task, current_user, db)
    add_coins(current_user, 10, db)

    db.commit()

    return {
        "message": "Tarefa concluída!",
        "new_achievements": [
            {
                "name": a.name,
                "rarity": a.rarity,
                "xp_bonus": a.xp_reward,
            }
            for a in unlocked
        ],
    }