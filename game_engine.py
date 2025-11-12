import time
from utils.colors import color_text, CYAN, GREEN, YELLOW

def intro_animation():
    print(color_text("\n✨ Iniciando TDAH TaskQuest... ✨", CYAN))
    time.sleep(0.5)
    print(color_text("Carregando foco...", YELLOW))
    time.sleep(0.5)
    print(color_text("Carregando motivação...", YELLOW))
    time.sleep(0.5)
    print(color_text("Carregando organização...", YELLOW))
    time.sleep(0.5)
    print(color_text("\n🧠 Bem-vindo(a) ao TDAH TaskQuest! 🧩", GREEN))
    time.sleep(1)

import time
from utils.colors import color_text, YELLOW, CYAN, GREEN

def level_up_animation(level):
    """Mostra uma animação ao subir de nível."""
    print()
    print(color_text("✨ Subindo de nível", YELLOW), end="")
    for _ in range(3):
        time.sleep(0.4)
    print(color_text(".", CYAN), end="", flush=True)
    time.sleep(0.4)
    print()
    print(color_text("🌟 PARABÉNS! 🌟", GREEN))
    time.sleep(0.4)
    print(color_text(f"Você alcançou o nível {level}!", CYAN))
    print(color_text("Continue progredindo, aventureiro(a) do foco e da organização! 🧭", YELLOW))
    print()

import time
from utils.colors import color_text, CYAN, GREEN, YELLOW

def intro_animation():
    """Animação de introdução ao iniciar o jogo."""
    print(color_text("\n🧠 Bem-vindo(a) ao TDAH TaskQuest! 🧩", YELLOW))
    time.sleep(0.5)
    print(color_text("Organize suas tarefas, ganhe XP e evolua seu foco!", CYAN))
    time.sleep(0.5)
    print(color_text("Preparado(a) para começar sua jornada? 🚀\n", GREEN))
    time.sleep(0.5)