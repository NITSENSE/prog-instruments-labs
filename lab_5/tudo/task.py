import datetime
import logging

logger = logging.getLogger(__name__)


def get_local_timezone():
    """Возвращает локальный часовой пояс системы.
    
    Returns:
        Объект timezone, представляющий локальный часовой пояс системы.
    """
    return datetime.datetime.now().astimezone().tzinfo


def ensure_timezone_aware(dt, tz=None):
    """Преобразует datetime в aware (с часовым поясом), если он naive.
    
    Если datetime уже имеет часовой пояс, возвращает его без изменений.
    Если datetime naive (без часового пояса), считает его локальным временем системы.
    
    Args:
        dt: Объект datetime (может быть naive или aware).
        tz: Часовой пояс для использования (по умолчанию локальный системный).
        
    Returns:
        Объект datetime с часовым поясом (aware).
    """
    if dt is None:
        return None
    
    if tz is None:
        tz = get_local_timezone()
    
    if dt.tzinfo is None:
        # Naive datetime - считаем его локальным временем
        logger.debug("Converting naive datetime to timezone-aware: %s -> %s", dt, tz)
        return dt.replace(tzinfo=tz)
    else:
        # Уже aware datetime - возвращаем как есть
        return dt


class Task:
    """Класс, представляющий задачу в системе управления задачами."""
    
    def __init__(self, number, description, started, finished=None, important=0, urgent=0):
        """Создает новую задачу.
        
        Args:
            number: Уникальный номер задачи.
            description: Описание задачи.
            started: Время начала задачи (datetime, может быть naive или aware).
            finished: Время завершения задачи (datetime, может быть naive или aware, опционально).
            important: Флаг важности (0 или 1).
            urgent: Флаг срочности (0 или 1).
        """
        self.number = number
        self.description = description
        # Преобразуем timestamps в aware datetime с локальным часовым поясом
        self.started = ensure_timezone_aware(started)
        self.finished = ensure_timezone_aware(finished) if finished else None
        self.important = important
        self.urgent = urgent

    def is_finished(self):
        """Проверяет, завершена ли задача.
        
        Returns:
            True, если задача завершена, False в противном случае.
        """
        return self.finished is not None

    def date_from_timestamp(self, timestamp):
        """Преобразует timestamp в datetime с локальным часовым поясом.
        
        Args:
            timestamp: Unix timestamp (число секунд с эпохи).
            
        Returns:
            Объект datetime с локальным часовым поясом или None, если timestamp не задан.
        """
        if timestamp is None:
            return None
        local_tz = get_local_timezone()
        return datetime.datetime.fromtimestamp(timestamp, tz=local_tz)