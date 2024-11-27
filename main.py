"""
Основной модуль для запуска проверки ссылок на веб-страницах.

Этот модуль содержит функцию `main`, которая инициализирует объект `LinkChecker`
и запускает процесс проверки ссылок. Проверка выполняется для указанных URL-адресов,
и результаты сохраняются в Excel файл.

Пример использования:
```bash
python main.py

"""

from concurrent.futures import ThreadPoolExecutor
from checker import LinkChecker
from utils import print_choice, get_time_script


@get_time_script
def main():
    """
    Запускает процесс проверки ссылок на веб-страницах.
    Copy

    Эта функция инициализирует объект `LinkChecker` с указанными URL-адресами,
    запрашивает выбор пользователя через функцию `print_choice`, и затем
    использует `ThreadPoolExecutor` для параллельной обработки ссылок.
    Результаты проверки сохраняются в Excel файл.

    Возвращает:
        None: Функция ничего не возвращает, она только запускает процесс проверки.
    """
    urls = set()
    urls = print_choice(urls)
    checker = LinkChecker(urls)

    # Используем ThreadPoolExecutor для параллельной обработки ссылок
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(checker.check_links, urls)

if __name__ == "__main__":
    main()
