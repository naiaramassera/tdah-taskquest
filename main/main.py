from task_manager import show_tasks, add_task, mark_done, show_status, check_tasks, load_data
from utils.colors import color_text, CYAN, GREEN, YELLOW, RED
from game_engine import intro_animation


def main():
    intro_animation()  # Mostra uma introdução bonita (se quiser deixar simples, posso te mostrar como editar)
    data = load_data()


    while True:
        print(color_text("\n=== MENU PRINCIPAL ===", CYAN))
        print(color_text("1. Ver tarefas", YELLOW))
        print(color_text("2. Adicionar tarefa", YELLOW))
        print(color_text("3. Concluir tarefa", YELLOW))
        print(color_text("4. Ver status", YELLOW))
        print(color_text("5. Sair", RED))

        choice = input(color_text("\nEscolha uma opção: ", GREEN))

        if choice == "1":
            show_tasks(data)
        elif choice == "2":
            add_task(data)
            data = check_tasks()
        elif choice == "3":
            mark_done(data)
            data = check_tasks()
        elif choice == "4":
            show_status(data)
        elif choice == "5":
            print(color_text("\nAté logo! Continue sua jornada de organização! 🌟", CYAN))
            break
        else:
            print(color_text("Opção inválida! Escolha de 1 a 5.", RED))


if __name__ == "__main__":
    main()
    main()
