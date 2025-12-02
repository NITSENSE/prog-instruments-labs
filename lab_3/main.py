import csv
import json
import os
import re
import sys 
from typing import List, Dict

try:
    from checksum import calculate_checksum
except ImportError:
    print("ОШИБКА: Файл checksum.py не найден в папке со скриптом!")
    sys.exit(1)  


VARIANT_NUMBER = 82
FILENAME_CSV = 'dataset.csv'
FILENAME_JSON = 'result.json'
ENCODING = 'utf-16'

PATTERNS = {
    'telephone': re.compile(r'^\+7-\(\d{3}\)-\d{3}-\d{2}-\d{2}$'),
    'http_status_message': re.compile(r'^\d{3}\s[a-zA-Z0-9_ ]+$'),
    'snils': re.compile(r'^\d{11}$'),
    'identifier': re.compile(r'^\d{2}-\d{2}/\d{2}$'),
    'ip_v4': re.compile(
        r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.){3}'
        r'(25[0-5]|(2[0-4]|1\d|[1-9]|)\d)$'
    ),
    'longitude': re.compile(
        r'^-?(?:180(?:\.0+)?|(?:1[0-7]\d|[1-9]?\d)(?:\.\d+)?)$'
    ),
    'blood_type': re.compile(r'^(A|B|AB|O)[\u2212\-\+]$'),
    'isbn': re.compile(r'^(?:\d+-\d+-\d+-\d+(?:-\d+)?)$'),
    'locale_code': re.compile(r'^[a-z]{2}(?:-[a-z]{2,})?(?:_[a-z0-9]+)?$'),
    'date': re.compile(r'^\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])$')
}


def is_row_valid(row: Dict[str, str]) -> bool:
    """
    Проверяет валидность всех полей в строке CSV.
    Возвращает False, если хотя бы одно поле не соответствует шаблону.
    """
    for key, value in row.items():
        pattern = PATTERNS.get(key)
        if pattern and not pattern.match(value):
            return False
    return True


def get_invalid_indices(filepath: str) -> List[int]:
    """
    Читает файл и возвращает список индексов невалидных строк.
    Индексация данных начинается с 0 (заголовок не считается).
    """
    indices = []
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Файл не найден: {filepath}")

    with open(filepath, mode='r', encoding=ENCODING, newline='') as f:
        reader = csv.DictReader(f, delimiter=';', quotechar='"')

        for i, row in enumerate(reader):
            if not is_row_valid(row):
                indices.append(i)

    return indices


def serialize_result(variant: int, checksum: str, filepath: str) -> None:
    """
    Сохраняет итоговый результат в JSON файл в формате, требуемом заданием.
    """
    data = {
        "variant": variant,
        "checksum": checksum
    }
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def main():
    """
    Точка входа в программу.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, FILENAME_CSV)
    json_path = os.path.join(script_dir, FILENAME_JSON)

    print(f"--- Начало обработки варианта {VARIANT_NUMBER} ---")
    print(f"Чтение файла: {csv_path}")

    try:
        invalid_indices = get_invalid_indices(csv_path)
        print(f"Найдено невалидных строк: {len(invalid_indices)}")

        checksum = calculate_checksum(invalid_indices)
        print(f"Контрольная сумма MD5: {checksum}")

        serialize_result(VARIANT_NUMBER, checksum, json_path)
        print(f"Готово! Результат записан в {FILENAME_JSON}")

    except Exception as e:
        print(f"\nКРИТИЧЕСКАЯ ОШИБКА: {e}")
        print("Проверьте имя файла, кодировку или наличие checksum.py")


if __name__ == "__main__":
    main()