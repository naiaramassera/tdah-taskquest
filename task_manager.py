import json
import os
from datetime import date, timedelta

from game_engine import level_up_animation
from utils.colors import color_text, GREEN, RED, YELLOW, CYAN

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")
TASK_COMPLETION_XP = 50
POMODORO_TARGET = 3


# --------------------------------------------------------
# Modelo e serviços de progresso
# --------------------------------------------------------
def default_user_progress():
    return {
        "xp": 0,
        "streak_days": 0,
        "badges": [],
        "last_active_date": None,
        "daily_pomodoros": {},
        "daily_completed_tasks": {},
    }


def ensure_data_schema(data):
    """Garante compatibilidade de schema antigo e novo."""
    data.setdefault("tasks", [])
    data.setdefault("level", 1)
    data.setdefault("xp", 0)
    data.setdefault("focus", 100)
    data.setdefault("motivation", 100)
    data.setdefault("organization", 100)

    progress = data.setdefault("user_progress", default_user_progress())
    progress.setdefault("xp", data.get("xp", 0))
    progress.setdefault("streak_days", 0)
    progress.setdefault("badges", [])
    progress.setdefault("last_active_date", None)
    progress.setdefault("daily_pomodoros", {})
    progress.setdefault("daily_completed_tasks", {})

    data["xp"] = progress["xp"]
    return data


def update_streak(data, reference_date=None):
    """Endpoint/serviço: atualiza streak de uso diário."""
    progress = data["user_progress"]
    today = reference_date or date.today()
    today_iso = today.isoformat()

    last_active = progress.get("last_active_date")
    if last_active == today_iso:
        return

    if last_active:
        last_date = date.fromisoformat(last_active)
        if last_date == today - timedelta(days=1):
            progress["streak_days"] += 1
        elif last_date != today:
            progress["streak_days"] = 1
    else:
        progress["streak_days"] = 1

    progress["last_active_date"] = today_iso


def add_xp_for_completed_task(data):
    """Endpoint/serviço: incrementa XP ao concluir tarefa."""
    progress = data["user_progress"]
    progress["xp"] += TASK_COMPLETION_XP
    data["xp"] = progress["xp"]

    today = date.today().isoformat()
    daily_tasks = progress["daily_completed_tasks"]
    daily_tasks[today] = daily_tasks.get(today, 0) + 1

    print(f"🎉 Você ganhou {TASK_COMPLETION_XP} XP! Total: {progress['xp']} XP")


def register_pomodoro(data):
    """Endpoint/serviço: registra pomodoro diário e tenta conceder badge."""
    progress = data["user_progress"]
    today = date.today().isoformat()
    daily_pomodoros = progress["daily_pomodoros"]
    daily_pomodoros[today] = daily_pomodoros.get(today, 0) + 1

    update_streak(data)
    grant_badges(data)
    save_data(data)

    print(color_text(f"🍅 Pomodoro registrado! Total de hoje: {daily_pomodoros[today]}", GREEN))


def grant_badges(data):
    """Endpoint/serviço: concede badges por marcos de progresso."""
    progress = data["user_progress"]
    today = date.today().isoformat()
    badges = progress["badges"]

    if progress["daily_pomodoros"].get(today, 0) >= POMODORO_TARGET and "Foco em Dia" not in badges:
        badges.append("Foco em Dia")
        print(color_text("🏅 Badge desbloqueada: Foco em Dia (3 pomodoros no dia)", CYAN))

    if progress["streak_days"] >= 7 and "Constância 7 dias" not in badges:
        badges.append("Constância 7 dias")
        print(color_text("🏅 Badge desbloqueada: Constância 7 dias", CYAN))

    if progress["xp"] >= 500 and "XP 500" not in badges:
        badges.append("XP 500")
        print(color_text("🏅 Badge desbloqueada: XP 500", CYAN))


def daily_summary(data):
    """Retorna resumo diário para UI."""
    progress = data["user_progress"]
    today = date.today().isoformat()
    tasks_today = progress["daily_completed_tasks"].get(today, 0)
    pomodoros_today = progress["daily_pomodoros"].get(today, 0)

    return {
        "date": today,
        "tasks_completed": tasks_today,
        "pomodoros": pomodoros_today,
        "xp": progress["xp"],
        "streak_days": progress["streak_days"],
    }


# --------------------------------------------------------
# Funções de manipulação do arquivo JSON
# --------------------------------------------------------
def load_data():
    """Carrega os dados do arquivo JSON ou cria um novo se não existir."""
    if not os.path.exists(DATA_FILE):
        data = ensure_data_schema({})
        save_data(data)
        return data

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = ensure_data_schema({})
        save_data(data)
        return data

    data = ensure_data_schema(data)
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
        "xp": 10,
    }
    data["tasks"].append(new_task)
    save_data(data)
    print(color_text(f"Tarefa '{title}' adicionada com sucesso!", GREEN))


def mark_done(data):
    """Marca uma tarefa como concluída."""
    show_tasks(data)
    try:
        index = int(input("Digite o número da tarefa concluída: ")) - 1
        if 0 <= index < len(data["tasks"]):
            if not data["tasks"][index]["done"]:
                data["tasks"][index]["done"] = True
                print("✅ Tarefa marcada como concluída!")

                update_streak(data)
                add_xp_for_completed_task(data)
                grant_badges(data)

                if data["user_progress"]["xp"] >= data["level"] * 200:
                    data["level"] += 1
                    data["user_progress"]["xp"] = 0
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


def render_progress_bar(current_xp, level):
    target = max(level * 200, 1)
    ratio = min(current_xp / target, 1)
    filled = int(ratio * 20)
    bar = "█" * filled + "-" * (20 - filled)
    return f"[{bar}] {current_xp}/{target} XP"


def show_status(data):
    """Mostra status com barra de progresso, streak/badges e resumo diário."""
    progress = data["user_progress"]
    summary = daily_summary(data)

    print(color_text("\n=== STATUS ATUAL ===", CYAN))
    print(f"Nível: {data['level']}")
    print(f"Progresso: {render_progress_bar(progress['xp'], data['level'])}")
    print(f"Foco: {data['focus']}")
    print(f"Motivação: {data['motivation']}")
    print(f"Organização: {data['organization']}")

    print(color_text("\n=== PAINEL DE STREAK & BADGES ===", CYAN))
    print(f"🔥 Streak atual: {progress['streak_days']} dia(s)")
    badges = ", ".join(progress["badges"]) if progress["badges"] else "Nenhuma badge ainda"
    print(f"🏅 Badges: {badges}")

    print(color_text("\n=== RESUMO DIÁRIO ===", CYAN))
    print(f"📅 Data: {summary['date']}")
    print(f"✅ Tarefas concluídas hoje: {summary['tasks_completed']}")
    print(f"🍅 Pomodoros hoje: {summary['pomodoros']}")
    print(f"⭐ XP total: {summary['xp']}")


def check_tasks():
    """Carrega os dados e confirma o sistema."""
    data = load_data()
    print(color_text("✅ Sistema de tarefas carregado com sucesso!", GREEN))
    return data


if __name__ == "__main__":
    data = check_tasks()
    show_tasks(data)
