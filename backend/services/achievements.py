def check_achievements(user):

    if user.level >= 5:
        unlocked.append("Subiu para nível 5!")

    total_completed = db.query(Task).filter(Task.owner_id == user.id, Task.completed == True).count()

    unlocked = []

    if total_completed > 50:

    return unlocked