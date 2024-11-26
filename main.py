"""
Основной модуль для запуска проверки ссылок на веб-страницах.

Этот модуль содержит функцию `main`, которая 
инициализирует объект `LinkChecker` и запускает процесс проверки ссылок.
Проверка выполняется для указанных URL-адресов, и результаты сохраняются в Excel файл.

Пример использования:
```python
python main.py
```
"""
from checker import LinkChecker
from utils import get_time_script

@get_time_script
def main():
    """
    Основная функция для запуска проверки ссылок.

    Описание:
    - Инициализирует объект `LinkChecker` с указанными URL-адресами.
    - Запускает процесс проверки ссылок.
    - Результаты проверки сохраняются в Excel файл.
    """

    urls = ['https://gemma.by/soveti/']
    checker = LinkChecker(urls)
    checker.check_links()

if __name__ == "__main__":
    main()
