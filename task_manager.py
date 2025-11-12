import json
import os
from utils.colors import color_text, GREEN, RED, YELLOW, CYAN

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

# --------------------------------------------------------
# Funções de manipulação do arquivo JSON
# --------------------------------------------------------
def load_data():
    """Carrega os dados do arquivo JSON ou cria um novo se não existir."""
    if not os.path.exists(DATA_FILE):
        data = {
            "tasks":[],
            "level":  1,
            "xp": 0,
            "focus": 100,
            "motivation": 100,
            "organization": 100
        }
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"tasks": [], "level": 1, "xp": 0}
        save_data(data)
    return data


def save_data(data):
    """Salva os dados no arquivo JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# --------------------------------------------------------
# Funções principais do gerenciador de tarefas
# --------------------------------------------------------
def show_tasks(data):
    """Mostra todas as tarefas."""
    print(color_text("\n=== SUAS TAREFAS ===", CYAN))
    if not data["tasks"]:
        print(color_text("Nenhuma tarefa adicionada ainda.", YELLOW))
        return
    for task in data["tasks"]:
        status = color_text("[✔]" if task["done"] else "[ ]", GREEN if task["done"] else RED)
        print(f"{status} {task['id']}. {task['title']}")


def add_task(data):
    """Adiciona uma nova tarefa."""
    title = input(color_text("\nDigite o nome da nova tarefa: ", YELLOW))
    if not title.strip():
        print(color_text("Tarefa não pode estar vazia!", RED))
        return

    new_task = {
        "id": len(data["tasks"]) + 1,
        "title": title,
        "done": False,
        "xp": 10  # XP padrão por tarefa
    }
    data["tasks"].append(new_task)
    save_data(data)
    print(color_text(f"Tarefa '{title}' adicionada com sucesso!", GREEN))


def mark_done(data):
    from game_engine import level_up_animation
    """Marca uma tarefa como concluída."""
    show_tasks(data)
    try:
        index = int(input("Digite o número da tarefa concluída: ")) - 1
        if 0 <= index < len(data["tasks"]):
            if not data["tasks"][index]["done"]:
                data["tasks"][index]["done"] = True
                print("✅ Tarefa marcada como concluída!")

                # 🎯 Ganha XP por concluir tarefas
                data["xp"] += 50
                print(f"🎉 Você ganhou 50 XP! Total: {data['xp']} XP")

                # 💪 Sobe de nível a cada 200 XP
                if data["xp"] >= data["level"] * 200:
                    data["level"] += 1
                    data["xp"] = 0
                    level_up_animation(data["level"])
                    print("✨ PARABÉNS! Você subiu de nível! ✨")
                    print(f"🌟 Novo nível: {data['level']}")

                save_data(data)
            else:
                print("Essa tarefa já foi concluída!")
        else:
            print("Número inválido!")
    except ValueError:
        print("Entrada inválida!")


def show_status(data):
    """Mostra o status atual do jogador."""
    print("\n=== STATUS ATUAL ===")
    print(f"Nível: {data['level']}")
    print(f"XP: {data['xp']}")
    print(f"Foco: {data['focus']}")
    print(f"Motivação: {data['motivation']}")
    print(f"Organização: {data['organization']}")


def check_tasks():
    """Carrega os dados e confirma o sistema."""
    data = load_data()
    print(color_text("✅ Sistema de tarefas carregado com sucesso!", GREEN))
    return data


if __name__ == "__main__":
    data = check_tasks()
    show_tasks(data)
