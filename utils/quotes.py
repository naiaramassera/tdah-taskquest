import random

QUOTES = [
    "Você não é bagunçado — só está em modo criativo!",
    "Pequenos passos ainda são progresso 🌱",
    "Um check de cada vez, e o mundo se organiza 🧠💫",
    "Você não precisa ser perfeito, só constante.",
    "TDAH não é falha — é superpoder mal calibrado ⚡"
]

def random_quote():
    return random.choice(QUOTES)

