import time
import re
import openpyxl


def get_time_script(fun):
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
    # Удаляем все символы, которые не являются буквами, цифрами или подчеркиванием
    cleaned_url = re.sub(r'[^a-zA-Z0-9_]', '_', url)
    return cleaned_url

def save_data(data_to_save, url):
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
