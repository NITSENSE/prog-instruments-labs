import argparse
import sys

import tudo.controller as controller
import tudo.store as store
import tudo.view as view


def create_parser():
    """Создает и настраивает парсер аргументов командной строки.
    
    Returns:
        Настроенный объект ArgumentParser.
    """
    parser = argparse.ArgumentParser(
        prog='tudo',
        description='Система управления задачами',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Доступные команды', metavar='КОМАНДА')
    
    # Команда add
    add_parser = subparsers.add_parser('add', help='Добавить новую задачу')
    add_parser.add_argument('descriptions', nargs='+', help='Описания задач для добавления')
    add_parser.add_argument('--prio', action='store_true', 
                           help='Добавить задачи с приоритетами. В этом случае аргументы должны быть кратны 3: описание, важность (0/1), срочность (0/1)')
    
    # Команда list
    list_parser = subparsers.add_parser('list', help='Показать список задач')
    list_parser.add_argument('--all', action='store_true', 
                            help='Показать все задачи, включая завершенные')
    list_parser.add_argument('--prio', nargs=2, metavar=('ВАЖНОСТЬ', 'СРОЧНОСТЬ'), type=int,
                            help='Фильтровать задачи по приоритетам (важность и срочность: 0 или 1)')
    
    # Команда rm
    rm_parser = subparsers.add_parser('rm', help='Удалить задачи')
    rm_parser.add_argument('numbers', nargs='+', type=int, metavar='НОМЕР',
                          help='Номера задач для удаления')
    
    # Команда done
    done_parser = subparsers.add_parser('done', help='Отметить задачи как завершенные')
    done_parser.add_argument('numbers', nargs='+', type=int, metavar='НОМЕР',
                            help='Номера задач для отметки как завершенных')
    
    # Команда stats
    stats_parser = subparsers.add_parser('stats', help='Показать статистику завершенных задач по датам')
    
    # Команда eisenhower
    eisenhower_parser = subparsers.add_parser('eisenhower', 
                                             help='Показать матрицу Эйзенхауэра для задач')
    
    return parser


def handle_add(store, args):
    """Обрабатывает команду добавления задач.
    
    Args:
        store: Экземпляр TasksStore для работы с базой данных.
        args: Объект с аргументами команды add.
    """
    if args.prio:
        if len(args.descriptions) % 3 != 0:
            view.print_error("Ошибка: при использовании --prio количество аргументов должно быть кратно 3")
            return
        tasks = args.descriptions
        for i in range(0, len(tasks) // 3):
            description = tasks[i * 3]
            important = int(tasks[i * 3 + 1])
            urgent = int(tasks[i * 3 + 2])
            controller.add_task_with_priority(store, description, important, urgent)
    else:
        for description in args.descriptions:
            controller.add_task(store, description)


def handle_list(store, args):
    """Обрабатывает команду вывода списка задач.
    
    Args:
        store: Экземпляр TasksStore для работы с базой данных.
        args: Объект с аргументами команды list.
    """
    show_completed = args.all
    important = None
    urgent = None
    
    if args.prio:
        important = args.prio[0]
        urgent = args.prio[1]
    
    tasks = controller.list_tasks(store, show_completed=show_completed, 
                                  important=important, urgent=urgent)
    view.print_tasks(tasks, show_completed=show_completed)


def main(argv=sys.argv):
    """Главная функция приложения.
    
    Args:
        argv: Список аргументов командной строки (по умолчанию sys.argv).
        
    Returns:
        Код возврата: 0 при успехе, 1 при ошибке.
    """
    parser = create_parser()
    args = parser.parse_args(argv[1:])
    
    if args.command is None:
        parser.print_help()
        return 1
    
    task_store = store.TasksStore()
    
    command_handlers = {
        'add': lambda: handle_add(task_store, args),
        'list': lambda: handle_list(task_store, args),
        'rm': lambda: controller.remove_tasks(task_store, args.numbers),
        'done': lambda: controller.finish_tasks(task_store, args.numbers),
        'stats': lambda: view.print_stats(controller.group_tasks_archived(task_store)),
        'eisenhower': lambda: view.print_matrix(controller.eisenhower_matrix(task_store))
    }
    
    command_handlers[args.command]()
    return 0


def init(database_name="database.db"):
    """Инициализирует хранилище задач (устаревшая функция, оставлена для обратной совместимости).
    
    Args:
        database_name: Имя файла базы данных (по умолчанию "database.db").
        
    Returns:
        Экземпляр TasksStore.
    """
    return store.TasksStore(database_name)
