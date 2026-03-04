
def get_motivation(user):

    if user.missed_days >= 3:
        return "Recomeçar é força, não fraqueza 💛"

    if user.streak.current_streak >= 7:
        return "Você está criando consistência real 🔥"

    return "Pequenos passos ainda são progresso 🌱"




