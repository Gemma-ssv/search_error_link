"""Модуль для проверки ссылок на веб-страницах.

Этот модуль содержит класс `LinkChecker`, который использует
Selenium WebDriver для автоматизации браузера
и проверки доступности ссылок на указанных веб-страницах.
Результаты проверки сохраняются в Excel файл.

Основные функции:
- Проверка ссылок на новостях на указанных URL-адресах.
- Сохранение информации о неработающих ссылках в Excel файл.

Пример использования:
```python
urls = ['https://examle.by/']
checker = LinkChecker(urls)
checker.check_links()
```
"""

import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from utils import animate_search, print_slowly, save_data

class LinkChecker:
    """
    Класс для проверки ссылок на веб-страницах.

    Атрибуты:
        urls (list): Список URL-адресов для проверки.
        data_to_save (list): Список для хранения данных о неработающих ссылках.
        options (webdriver.ChromeOptions): Опции для настройки Chrome WebDriver.
    """
    def __init__(self, urls):
        """
        Инициализация объекта LinkChecker.

        Аргументы:
            urls (list): Список URL-адресов для проверки.
        """
        self.urls = urls
        self.data_to_save = []
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_argument('--headless=new')

    def set_logs(self, error: str) -> None:
        """
        Записывает информацию об ошибках в файл error_logs.txt.

        Параметры:
            error (str): Текст ошибки.
        """
        with open('error_logs.txt', 'a', encoding='utf-8') as f:
            f.write(f"Ошибка: {error}\n")

    def check_links(self, url):
        """
        Основной метод для проверки ссылок на указанных URL-адресах.

        Аргументы:
            url(str): Строка содержащая ссылку.
        
        Описание:
        - Инициализирует Chrome WebDriver.
        - Проходит по каждому URL-адресу и вызывает метод _process_page для обработки страницы.
        - Сохраняет данные о неработающих ссылках в Excel файл.
        """

        try:
            with webdriver.Chrome(options=self.options) as browser:
                self.data_to_save = []
                browser.get(url)
                self._process_page(browser)

                if self.data_to_save:
                    save_data(self.data_to_save, url)
                else:
                    self.set_logs("Нет данных для сохранения.")
                    print_slowly("Нет данных для сохранения.")
        except Exception as e: # pylint: disable=broad-exception-caught
            self.set_logs(f"Произошла ошибка: {e}.")
            print_slowly(f"Произошла ошибка: {e}.\nДанные об ошибке в файле error_logs.txt.")

    def _process_page(self, browser):
        """
        Обрабатывает текущую страницу, проверяя ссылки на новостях.

        Аргументы:
            browser (webdriver.Chrome): Экземпляр Chrome WebDriver.
            
        Описание:
            - Находит все ссылки на новости на текущей странице.
            - Для каждой новости вызывает метод _process_news для проверки ссылок внутри новости.
            - Проверяет наличие следующей страницы и переходит на нее, если она существует.
        """
        stop_event = threading.Event()
        animation_thread = threading.Thread(target=animate_search, args=(stop_event,))
        animation_thread.start()

        while True:
            news_list = WebDriverWait(browser, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@class='image']/a"))
            )
            for n_l in news_list:
                try:
                    self._process_news(browser, n_l)
                except Exception as e2: # pylint: disable=broad-exception-caught
                    self.set_logs(f"Ошибка при обработке новости: {e2}\n{n_l.text}")
                    continue

            try:
                pagination = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "pagination"))
                )
                next_page_link = pagination.find_elements(By.TAG_NAME, "a")
                for i in next_page_link:
                    try:
                        if i.text.isdigit():
                            i.click()
                        WebDriverWait(browser, 10).until(EC.staleness_of(news_list[0]))
                    except Exception as e: # pylint: disable=broad-exception-caught
                        self.set_logs(f"Активных страниц нет: {e}")
                else:
                    stop_event.set()
                    animation_thread.join()
                    print_slowly("Следующая страница не найдена, переход к следующей ссылке\n")
                    break
            except Exception as e: # pylint: disable=broad-exception-caught
                stop_event.set()
                animation_thread.join()
                self.set_logs(f"Ошибка: {e}")
                break

    def _process_news(self, browser, news_link):
        """
        Обрабатывает отдельную новость, проверяя ссылки внутри нее.

        Аргументы:
            browser (webdriver.Chrome): Экземпляр Chrome WebDriver.
            news_link (WebElement): Элемент ссылки на новость.

        Описание:
            - Открывает ссылку на новость в новой вкладке.
            - Находит все ссылки внутри новости и проверяет их доступность.
            - Сохраняет информацию о неработающих ссылках.
        """
        href = news_link.get_attribute('href')
        browser.execute_script(f"window.open('{href}', '_blank');")
        window_handles = browser.window_handles
        browser.switch_to.window(window_handles[-1])

        # h1_link_list = WebDriverWait(browser, 10).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, "rt1"))
        # ).text
        h1_link_list = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        ).text

        link_list = browser.find_element(By.ID, "content")
        link_list = link_list.find_elements(By.TAG_NAME, "a")

        for l_l in link_list:
            l_l_text = l_l.text
            href_checklink = l_l.get_attribute('href')

            try:
                response = requests.get(href_checklink, timeout=30)
                if response.status_code != 200:
                    self.data_to_save.append({
                        "Основная статья": h1_link_list,
                        "Ссылка на основную статью": href,
                        "Ошибка": response.status_code,
                        "Текст ссылки в основной статье": l_l_text,
                        "Неработающая ссылка": href_checklink
                    })
            except Exception as e: # pylint: disable=broad-exception-caught
                self.data_to_save.append({
                    "Основная статья": h1_link_list,
                    "Ссылка на основную статью": href,
                    "Ошибка": "Возможно некорректная ссылка",
                    "Текст ссылки в основной статье": l_l_text,
                    "Неработающая ссылка": href_checklink
                })
                self.set_logs(f"Возможно некорректная ссылка - {e}")

        browser.close()
        browser.switch_to.window(window_handles[0])
