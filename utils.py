"""
Модуль с утилитами для проверки ссылок на веб-страницах.

Этот модуль содержит функции для измерения времени выполнения скрипта,
очистки URL-адресов для использования в именах файлов
и сохранения данных в Excel файл.

Основные функции:
- `get_time_script`: Декоратор для измерения времени выполнения функции.
- `clean_filename`: Функция для очистки URL-адреса от недопустимых
символов для использования в именах файлов.
- `save_data`: Функция для сохранения данных о неработающих ссылках в Excel файл.

Пример использования:
```python
@get_time_script
def my_function():
    # Ваш код

cleaned_url = clean_filename('https://example.com/path/to/page')
save_data(data_to_save, cleaned_url)
"""
import time
import re
import openpyxl


def get_time_script(fun):
    """
    Декоратор для измерения времени выполнения функции.

    Аргументы:
    fun (function): Функция, время выполнения которой нужно измерить.

    Возвращает:
    function: Обернутая функция с измерением времени выполнения.
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = fun(*args, **kwargs)
        end_time = time.time()
        # Вычисляем время выполнения в минутах и секундах
        elapsed_time = end_time - start_time
        minutes, seconds = divmod(elapsed_time, 60)

        # Выводим время выполнения в консоль
        print(f"Время выполнения скрипта: {int(minutes)} минут {int(seconds)} секунд")
        return result
    return wrapper

def clean_filename(url):
    """
    Очищает URL-адрес от недопустимых символов для использования в именах файлов.

    Аргументы:
    url (str): URL-адрес для очистки.

    Возвращает:
    str: Очищенный URL-адрес.
    """
    # Удаляем все символы, которые не являются буквами, цифрами или подчеркиванием
    cleaned_url = re.sub(r'[^a-zA-Z0-9_]', '_', url)
    return cleaned_url

def save_data(data_to_save, url):
    """
    Сохраняет данные о неработающих ссылках в Excel файл.
    Copy

    Аргументы:
    data_to_save (list): Список словарей с данными о неработающих ссылках.
    url (str): URL-адрес, используемый для формирования имени файла.

    Описание:
    - Создает новый Excel файл.
    - Записывает данные в файл.
    - Сохраняет файл с именем, основанным на очищенном URL-адресе.
    """
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Error"

    # Заголовки столбцов
    headers = [
        "Основная статья",
        "Ссылка на основную статью",
        "Ошибка",
        "Текст ссылки в основной статье",
        "Неработающая ссылка"
        ]
    sheet.append(headers)

    # Запись данных
    for data in data_to_save:
        sheet.append([
            data["Основная статья"],
            data["Ссылка на основную статью"],
            data["Ошибка"],
            data["Текст ссылки в основной статье"],
            data["Неработающая ссылка"]
            ])
    cleaned_url = clean_filename(url)
    # Определение имени файла в зависимости от URL
    filename = f"error{cleaned_url}.xlsx"

    # Сохранение файла
    workbook.save(filename)
    print(f"Данные успешно сохранены в файл {filename}")
