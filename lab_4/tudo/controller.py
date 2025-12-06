from itertools import zip_longest
from tabulate import tabulate


def finish_tasks(store, numbers):
    """Отмечает задачи как завершенные.
    
    Args:
        store: Экземпляр TasksStore для работы с базой данных.
        numbers: Список номеров задач для отметки как завершенных.
    """
    store.set_done(numbers)
    return


def remove_tasks(store, numbers):
    """Удаляет задачи по номерам.
    
    Args:
        store: Экземпляр TasksStore для работы с базой данных.
        numbers: Список номеров задач для удаления.
    """
    store.remove(numbers)
    return


def add(store, args):
    """Добавляет задачи в базу данных.
    
    Args:
        store: Экземпляр TasksStore для работы с базой данных.
        args: Список аргументов. Если первый аргумент "--prio", то следующие аргументы
              должны быть кратны 3 (описание, важность, срочность для каждой задачи).
              Иначе все аргументы считаются описаниями задач.
    """
    if args[0] == "--prio" and len(args[1:]) % 3 == 0:
        tasks = args[1:]
        for i in range(0, len(tasks) // 3):
            store.add_task_p([tasks[i * 3], tasks[i * 3 + 1], tasks[i * 3 + 2]])
    else:
        # TODO Behaviour for no Tasks to add
        for description in args:
            store.add_task(description)
    return


def list_tasks(store, show_completed=False, important = None, urgent = None):
    """Выводит список задач в табличном формате.
    
    Args:
        store: Экземпляр TasksStore для работы с базой данных.
        show_completed: Если True, показывает завершенные задачи.
        important: Фильтр по важности (0 или 1). Используется только вместе с urgent.
        urgent: Фильтр по срочности (0 или 1). Используется только вместе с important.
        
    Returns:
        Список объектов Task.
    """
    if important and urgent:
        tasks = store.list_tasks_p(important, urgent)
    else:
        tasks = store.list_tasks()

    if show_completed:
        print(tabulate([[
                            task.number,
                            task.description,
                            task.started.strftime("%Y-%m-%d %H:%M"),
                            "No" if task.important == 0 else "Yes",
                            "No" if task.urgent == 0 else "Yes",
                            task.finished.strftime("%Y-%m-%d %H:%M") if task.finished else "No"
                         ] for task in tasks],
                       headers=["#", "Description", "Started", "Important", "Urgent", "Finished"]))
    else:
        print(tabulate([[
                            task.number,
                            task.description,
                            task.started.strftime("%Y-%m-%d %H:%M"),
                            "No" if task.important == 0 else "Yes",
                            "No" if task.urgent == 0 else "Yes",
                        ] for task in tasks if not task.is_finished()],
                       headers=["#", "Description", "Started", "Important", "Urgent"]))
    return tasks


# TODO: Be able to set time range for grouping
def group_tasks_archived(store, *args):
    """Группирует завершенные задачи по датам и выводит статистику.
    
    Args:
        store: Экземпляр TasksStore для работы с базой данных.
        *args: Дополнительные аргументы (не используются).
        
    Returns:
        Список списков [дата, количество_завершенных_задач].
    """
    dates_and_nums = store.group_tasks_archived()
    print(tabulate(dates_and_nums,
                   headers=["Date", "Tasks finished"]))
    return dates_and_nums


def eisenhower_matrix(store, *args):
    """Выводит матрицу Эйзенхауэра для задач.
    
    Args:
        store: Экземпляр TasksStore для работы с базой данных.
        *args: Дополнительные аргументы (не используются).
    """
    col0 = col1 = col2 = col3 = []

    imp_urg = list(map(lambda task: str(task.number) + ": "+task.description, store.list_tasks_p(1, 1)))
    imp_not_urg = list(map(lambda task: str(task.number) + ": "+task.description, store.list_tasks_p(1, 0)))
    not_imp_urg = list(map(lambda task: str(task.number) + ": "+task.description, store.list_tasks_p(0, 1)))
    not_imp_not_urg = list(map(lambda task: str(task.number) + ": "+task.description, store.list_tasks_p(0, 0)))

    if len(imp_urg) < len(imp_not_urg):
        diff = len(imp_not_urg) - len(imp_urg)
        imp_urg.extend([" "] * diff)
    elif len(imp_not_urg) < len(imp_urg):
        diff = len(imp_urg) - len(imp_not_urg)
        imp_not_urg.extend([" "] * diff)

    col0 = ["Important"] + [" "] * (len(imp_urg) - 1) + ["---", "Not Important"]
    col1 = imp_urg + ["---"] + not_imp_urg
    col2 = ["---"] * (len(imp_urg) + 1 + max(len(not_imp_urg), len(not_imp_not_urg)))
    col3 = imp_not_urg + ["---"] + not_imp_not_urg

    zipped = zip_longest(col0, col1, col2, col3, fillvalue=" ")
    print(tabulate(list(zipped),
                   headers=[" ", "Urgent", "---", "Not Urgent"]))