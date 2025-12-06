from itertools import zip_longest
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
    
    Args:
        matrix_data: Словарь с данными матрицы, содержащий ключи:
            - imp_urg: список задач (важные и срочные)
            - imp_not_urg: список задач (важные, но не срочные)
            - not_imp_urg: список задач (не важные, но срочные)
            - not_imp_not_urg: список задач (не важные и не срочные)
    """
    imp_urg = matrix_data['imp_urg']
    imp_not_urg = matrix_data['imp_not_urg']
    not_imp_urg = matrix_data['not_imp_urg']
    not_imp_not_urg = matrix_data['not_imp_not_urg']
    
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


def print_error(message):
    """Выводит сообщение об ошибке.
    
    Args:
        message: Текст сообщения об ошибке.
    """
    print(message)

