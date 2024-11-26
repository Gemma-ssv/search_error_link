from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from utils import save_data


class LinkChecker:
    def __init__(self, urls):
        self.urls = urls
        self.data_to_save = []
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_argument('--headless=new')

    def check_links(self):
        try:
            with webdriver.Chrome(options=self.options) as browser:
                for url in self.urls:
                    self.data_to_save = []  # Очищаем список данных для каждой новой страницы
                    browser.get(url)
                    self._process_page(browser)

                    # Создание Excel файла и запись данных для текущей страницы
                    if self.data_to_save:
                        save_data(self.data_to_save, url)
                    else:
                        print("Нет данных для сохранения.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    def _process_page(self, browser):
        while True:
            news_list = WebDriverWait(browser, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@class='image']/a"))
            )
            for n_l in news_list:
                try:
                    self._process_news(browser, n_l)
                except Exception as e2:
                    print(f"Ошибка при обработке новости: {e2}")
                    print(n_l.text)
                    continue

            # Проверка наличия следующей страницы
            try:
                pagination = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "pagination"))
                )
                next_page_link = pagination.find_elements(By.TAG_NAME, "a")[-2]
                if ">" in next_page_link.text:
                    next_page_link.click()
                    WebDriverWait(browser, 10).until(EC.staleness_of(news_list[0]))
                else:
                    print("Следующая страница не найдена, переход к следующей ссылке")
                    break
            except Exception:
                print("Конец парсинга.")
                break

    def _process_news(self, browser, news_link):
        href = news_link.get_attribute('href')
        browser.execute_script(f"window.open('{href}', '_blank');")
        window_handles = browser.window_handles
        browser.switch_to.window(window_handles[-1])

        h1_link_list = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "rt1"))
        ).text

        link_list = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
        )

        for l_l in link_list:
            l_l_text = l_l.text
            href_checklink = l_l.get_attribute('href')

            try:
                response = requests.get(href_checklink, timeout=10)
                if response.status_code != 200:
                    self.data_to_save.append({
                        "Основная статья": h1_link_list,
                        "Ссылка на основную статью": href,
                        "Ошибка": response.status_code,
                        "Текст ссылки в основной статье": l_l_text,
                        "Неработающая ссылка": href_checklink
                    })
                    print(f"Основная статья: {h1_link_list},\n"
                          f"Ссылка на основную статью: {href},\n"
                          f"Ошибка: {response.status_code},\n"
                          f"Текст ссылки в основной статье: {l_l_text},\n"
                          f"Неработающая ссылка: {href_checklink}")
                else:
                    print('Элемент не найден - Всё хорошо')
            except Exception as e:
                self.data_to_save.append({
                    "Основная статья": h1_link_list,
                    "Ссылка на основную статью": href,
                    "Ошибка": "Некорректная ссылка",
                    "Текст ссылки в основной статье": l_l_text,
                    "Неработающая ссылка": href_checklink
                })
                print(e)

        browser.close()
        browser.switch_to.window(window_handles[0])
