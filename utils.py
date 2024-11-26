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
import threading
import re
import openpyxl


# Добавляем блокировку для синхронизации вывода в консоль
console_lock = threading.Lock()

def print_slowly(text, delay=0.05):
    with console_lock:
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

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
        time_script_text = f"Время выполнения скрипта: {int(minutes)} минут {int(seconds)} секунд"
        print_slowly(time_script_text)
        # Выводим сообщения о закрытии программы через 5, 4, 3, 2, 1 секунд
        for i in range(5, 0, -1):
            end_time_script_text = f"Закрытие через {i}..."
            print_slowly(end_time_script_text)
            time.sleep(1)
        end_script_text = "Закрытие программы."
        print_slowly(end_script_text)
        by_text = "by \\SSV/"
        print_slowly(by_text)

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
    save_data_text = f"Данные успешно сохранены в файл {filename}"
    print_slowly(save_data_text)

def is_valid_url(url_input):
    """
    Проверяет валидность ссылки. 
    Аргументы:
        url_input (str): Ссылка, которую пользователь ввел через консоль.

    Возвращает:
        bool: Правильный формат или неправильный формат ссылки.
    """
    # Регулярное выражение для проверки URL
    pattern = r'^https://[\w\-\.]+/[\w\-]+/$'

    # Проверка соответствия URL регулярному выражению
    if re.match(pattern, url_input):
        return True
    else:
        return False

def print_choice(urls: list) -> list:
    """
    Выводит информацию о программе. Запрашивает у пользователя ссылки.

    Args:
        urls (list): Получает пустой список, в который будут записаны ссылки.

    Returns:
        list: Возвращает список ссылок, которые ввёл пользователь.
    """
    while True:
        example_text = ("Введите ссылку в формате - https://домен/путь/\n"
            "Например - https://gemma.by/news/\n"
            "Нажмите - Enter.")
        print_slowly(example_text)
        url_input = input()

        if is_valid_url(url_input):
            urls.append(url_input)
            while True:
                choice_text = ("Выполнить поиск? Введите `да` или `нет`.\n"
                    "Если `нет`, то можно будет добавить еще ссылку.")
                print_slowly(choice_text)
                next_input = input().lower()

                if next_input == 'да':
                    break
                if next_input == 'нет':
                    break
                else:
                    wrong_answer_text = "Неправильные ответ. Требуется ввести `да` или `нет`."
                    print_slowly(wrong_answer_text)
                    continue

            if next_input == 'да':
                answer_yes_text = "Дождитесь окончания выполнения программы."
                print_slowly(answer_yes_text)
                break
        else:
            wrong_link_text = "Вы ввели неправильный формат ссылки. Попробуйте еще раз."
            print_slowly(wrong_link_text)
            continue
    return urls

def animate_search(stop_event):
    dots = 0
    while not stop_event.is_set():
        with console_lock:
            if dots == 0:
                print("\rВеду поиск", end='', flush=True)
            elif dots == 1:
                print("\rВеду поиск.", end='', flush=True)
            elif dots == 2:
                print("\rВеду поиск..", end='', flush=True)
            elif dots == 3:
                print("\rВеду поиск...", end='', flush=True)
        dots = (dots + 1) % 4
        time.sleep(0.5)
