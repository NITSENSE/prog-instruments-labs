from tabulate import tabulate


def print_tasks(tasks, show_completed=False):
    """Выводит список задач в табличном формате.
    
    Args:
        tasks: Список объектов Task для отображения.
        show_completed: Если True, показывает завершенные задачи.
    """
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


def print_stats(dates_and_nums):
    """Выводит статистику завершенных задач по датам.
    
    Args:
        dates_and_nums: Список списков [дата, количество_завершенных_задач].
    """
    print(tabulate(dates_and_nums,
                   headers=["Date", "Tasks finished"]))


def print_matrix(matrix_data):
    """Выводит матрицу Эйзенхауэра для задач.
    
    Матрица отображается в виде таблицы 2x2:
    - Строка "Important": квадранты Urgent и Not Urgent для важных задач
    - Строка "Not Important": квадранты Urgent и Not Urgent для неважных задач
    
    Args:
        matrix_data: Словарь с данными матрицы, содержащий ключ 'quadrants'
            со словарем квадрантов: 'imp_urg', 'imp_not_urg', 
            'not_imp_urg', 'not_imp_not_urg'
    """
    quadrants = matrix_data['quadrants']
    imp_urg = quadrants['imp_urg']
    imp_not_urg = quadrants['imp_not_urg']
    not_imp_urg = quadrants['not_imp_urg']
    not_imp_not_urg = quadrants['not_imp_not_urg']
    
    # Определяем максимальную высоту для выравнивания строк
    max_important_rows = max(len(imp_urg), len(imp_not_urg), 1)  # Минимум 1 для метки
    max_not_important_rows = max(len(not_imp_urg), len(not_imp_not_urg), 1)  # Минимум 1 для метки
    
    # Подготавливаем данные для таблицы
    table_rows = []
    
    # Строки для важных задач
    for i in range(max_important_rows):
        row_label = "Important" if i == 0 else ""
        urgent_task = imp_urg[i] if i < len(imp_urg) else ""
        not_urgent_task = imp_not_urg[i] if i < len(imp_not_urg) else ""
        table_rows.append([row_label, urgent_task, not_urgent_task])
    
    # Разделитель между важными и неважными задачами
    table_rows.append(["", "---", "---"])
    
    # Строки для неважных задач
    for i in range(max_not_important_rows):
        row_label = "Not Important" if i == 0 else ""
        urgent_task = not_imp_urg[i] if i < len(not_imp_urg) else ""
        not_urgent_task = not_imp_not_urg[i] if i < len(not_imp_not_urg) else ""
        table_rows.append([row_label, urgent_task, not_urgent_task])
    
    print(tabulate(table_rows, headers=["", "Urgent", "Not Urgent"]))


def print_error(message):
    """Выводит сообщение об ошибке.
    
    Args:
        message: Текст сообщения об ошибке.
    """
    print(message)

