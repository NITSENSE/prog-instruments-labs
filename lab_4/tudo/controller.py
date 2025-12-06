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


def add_task(store, description):
    """Добавляет задачу в базу данных.
    
    Args:
        store: Экземпляр TasksStore для работы с базой данных.
        description: Описание задачи.
    """
    store.add_task(description)


def add_task_with_priority(store, description, important, urgent):
    """Добавляет задачу с приоритетами в базу данных.
    
    Args:
        store: Экземпляр TasksStore для работы с базой данных.
        description: Описание задачи.
        important: Флаг важности (0 или 1).
        urgent: Флаг срочности (0 или 1).
    """
    store.add_task_p([description, important, urgent])


def list_tasks(store, show_completed=False, important=None, urgent=None):
    """Возвращает список задач из базы данных.
    
    Args:
        store: Экземпляр TasksStore для работы с базой данных.
        show_completed: Если True, включает завершенные задачи в результат.
        important: Фильтр по важности (0 или 1). Используется только вместе с urgent.
        urgent: Фильтр по срочности (0 или 1). Используется только вместе с important.
        
    Returns:
        Список объектов Task.
    """
    if important is not None and urgent is not None:
        tasks = store.list_tasks_p(important, urgent)
    else:
        tasks = store.list_tasks()
    
    if not show_completed:
        tasks = [task for task in tasks if not task.is_finished()]
    
    return tasks


# TODO: Be able to set time range for grouping
def group_tasks_archived(store):
    """Группирует завершенные задачи по датам.
    
    Args:
        store: Экземпляр TasksStore для работы с базой данных.
        
    Returns:
        Список списков [дата, количество_завершенных_задач].
    """
    return store.group_tasks_archived()


def eisenhower_matrix(store):
    """Возвращает данные для матрицы Эйзенхауэра.
    
    Args:
        store: Экземпляр TasksStore для работы с базой данных.
        
    Returns:
        Словарь с данными матрицы, содержащий ключи:
            - imp_urg: список строк задач (важные и срочные)
            - imp_not_urg: список строк задач (важные, но не срочные)
            - not_imp_urg: список строк задач (не важные, но срочные)
            - not_imp_not_urg: список строк задач (не важные и не срочные)
    """
    imp_urg = list(map(lambda task: str(task.number) + ": "+task.description, store.list_tasks_p(1, 1)))
    imp_not_urg = list(map(lambda task: str(task.number) + ": "+task.description, store.list_tasks_p(1, 0)))
    not_imp_urg = list(map(lambda task: str(task.number) + ": "+task.description, store.list_tasks_p(0, 1)))
    not_imp_not_urg = list(map(lambda task: str(task.number) + ": "+task.description, store.list_tasks_p(0, 0)))
    
    return {
        'imp_urg': imp_urg,
        'imp_not_urg': imp_not_urg,
        'not_imp_urg': not_imp_urg,
        'not_imp_not_urg': not_imp_not_urg
    }