import logging
import sqlite3

from tudo.task import Task

logger = logging.getLogger(__name__)


class TasksStore:
    """Хранилище задач в базе данных SQLite."""
    
    def __init__(self, db_name="database.db"):
        """Инициализирует хранилище задач.
        
        Args:
            db_name: Имя файла базы данных (по умолчанию "database.db").
        """
        logger.debug("Initializing TasksStore with database: %s", db_name)
        self.conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES)
        self.conn_cursor = self.conn.cursor()
        self.init()

    def add_task(self, description):
        """Добавляет задачу в базу данных.
        
        Args:
            description: Описание задачи.
        """
        self.conn_cursor.execute("""INSERT INTO tasks (description, important, urgent) VALUES(?, ?, ?)""",
                                 [description, 0, 0])
        self.conn.commit()
        logger.info("Successfully added new task: %s", description)

    def add_task_p(self, values):
        """Добавляет задачу с приоритетом в базу данных.
        
        Args:
            values: Список из трех элементов: [описание, важность, срочность].
        """
        self.conn_cursor.execute("""INSERT INTO tasks (description, important, urgent) VALUES(?, ?, ?)""",
                                 [values[0], int(values[1]), int(values[2])])
        self.conn.commit()
        logger.info("Successfully added new task with priority: %s (important=%s, urgent=%s)", 
                   values[0], values[1], values[2])

    def list_tasks(self):
        """Возвращает список всех задач из базы данных.
        
        Returns:
            Список объектов Task.
        """
        self.conn_cursor.execute("SELECT * FROM tasks")
        # print(str(self.conn_cursor.fetchall()))
        return [Task(task[0], task[1], task[2], task[3], task[4], task[5]) for task in self.conn_cursor.fetchall()]

    def list_tasks_p(self, important, urgent):
        """Возвращает список задач с заданными приоритетами.
        
        Args:
            important: Флаг важности (0 или 1).
            urgent: Флаг срочности (0 или 1).
            
        Returns:
            Список объектов Task с указанными приоритетами.
        """
        self.conn_cursor.execute("SELECT * FROM tasks WHERE urgent = ? AND important = ?", [urgent, important])
        # print(str(self.conn_cursor.fetchall()))
        return [Task(task[0], task[1], task[2], task[3], task[4], task[5]) for task in self.conn_cursor.fetchall()]

    def group_tasks_archived(self): # FIXME: Localize group date
        """Группирует завершенные задачи по датам.
        
        Returns:
            Список списков [дата, количество_завершенных_задач].
        """
        self.conn_cursor.execute('''
        SELECT DATE(finished) AS finished_date,
        COUNT(*) AS num_finished
        FROM tasks
        WHERE finished IS NOT NULL
        GROUP BY DATE(finished)
        ORDER BY finished_date
        ''')
        return [[row[0], row[1]] for row in self.conn_cursor.fetchall()]

    def init(self):
        """Инициализирует таблицу задач в базе данных, если она не существует."""
        self.conn_cursor.execute("""CREATE TABLE IF NOT EXISTS tasks
                            (number INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT, started TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            , finished TIMESTAMP, important INTEGER, urgent INTEGER)""")
        self.conn.commit()

    def remove(self, numbers):
        """Удаляет задачи по номерам.
        
        Args:
            numbers: Список номеров задач для удаления.
        """
        for number in numbers:
            self.conn_cursor.execute("""DELETE FROM tasks WHERE number=?""", number)
        self.conn.commit()

    def set_done(self, numbers):
        """Отмечает задачи как завершенные по номерам.
        
        Args:
            numbers: Список номеров задач для отметки как завершенных.
        """
        for number in numbers:
            self.conn_cursor.execute("""UPDATE tasks SET finished = CURRENT_TIMESTAMP WHERE number=?""", number)
        self.conn.commit()

    def reset(self):
        """Сбрасывает базу данных, удаляя все задачи."""
        logger.warning("Resetting database: dropping all tables")
        self.conn_cursor.execute("""DROP TABLE tasks""")
        self.init()
