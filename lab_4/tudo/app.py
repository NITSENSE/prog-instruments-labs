import sys

import tudo.controller as controller
import tudo.store as store


# TODO: Call our app via "tudo <command>", not with "app.py"
def main(argv=sys.argv):
    """Главная функция приложения.
    
    Args:
        argv: Список аргументов командной строки (по умолчанию sys.argv).
        
    Returns:
        Код возврата: 0 при успехе, 1 при ошибке.
    """
    task_store = store.TasksStore()

    if len(argv) == 1:
        # TODO print help
        return 1

    switch = {
        "add": controller.add,
        "list": list,
        "rm": controller.remove_tasks,
        "done": controller.finish_tasks,
        "stats": controller.group_tasks_archived,
        "eisenhower": controller.eisenhower_matrix
    }

    switch[argv[1]](task_store, argv[2:])
    return 0


def list(store, args):
    """Обрабатывает команду list с различными опциями.
    
    Args:
        store: Экземпляр TasksStore для работы с базой данных.
        args: Список аргументов команды list.
    """
    if len(args) == 0:
        controller.list_tasks(store)
    elif args[0] == "all":
        if len(args) > 1:
            if len(args) == 4 and args[1] == "--prio":
                controller.list_tasks(store, show_completed=True, important=int(args[2]), urgent=int(args[3]))
            else:
                controller.list_tasks(store, show_completed=True)
        else:
            controller.list_tasks(store, show_completed=True)
    else:
        if len(args) == 3 and args[0] == "--prio":
            controller.list_tasks(store, important=int(args[1]), urgent=int(args[2]))
        else:
            controller.list_tasks(store)


def init(database_name = "database.db"):
    """Инициализирует хранилище задач (устаревшая функция, оставлена для обратной совместимости).
    
    Args:
        database_name: Имя файла базы данных (по умолчанию "database.db").
        
    Returns:
        Экземпляр TasksStore.
    """
    return store.TasksStore(database_name)
