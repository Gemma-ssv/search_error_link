from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
from utils import get_time_script, save_data

@get_time_script
def main():
    # Список для хранения данных
    data_to_save = []
    # start_time = time.time()
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--headless=new')

    # Инициализация драйвера
    try:
        with webdriver.Chrome(options=options) as browser:
            urls = ['https://gemma.by/soveti/']
            for url in urls:
                data_to_save = []  # Очищаем список данных для каждой новой страницы
                browser.get(url)
                
                while True:
                    news_list = browser.find_elements(By.XPATH, "//div[@class='image']/a")  # Ссылки новостей
                    for n_l in news_list:
                        try:
                            first_link = n_l
                            
                            # Получить значение атрибута href
                            href = first_link.get_attribute('href')
                            
                            # Открыть ссылку в новой вкладке с помощью JavaScript
                            browser.execute_script(f"window.open('{href}', '_blank');")
                            
                            # Получить список всех открытых вкладок
                            window_handles = browser.window_handles
                            # Переключиться на новую вкладку
                            browser.switch_to.window(window_handles[-1])
                            link_list = browser.find_elements(By.TAG_NAME, "article")  # Основной блок где ищем ссылки на странице новости
                            link_list = link_list[0].find_elements(By.TAG_NAME, "a") # Выбираем ссылки на странице новостей
                            
                            h1_link_list = browser.find_element(By.CLASS_NAME, "rt1")  # Название статьи
                            h1_link_list = h1_link_list.text
                            
                            if link_list:
                                for l_l in link_list:
                                    l_l_text = l_l.text
                                    href_checklink = l_l.get_attribute('href')  # Ссылка для проверки в самой новости

                                    try:
                                        response = requests.get(href_checklink)    
                                        # Получить список всех открытых вкладок
                                        window_handles = browser.window_handles
                                        
                                        time.sleep(1)
                                        if response.status_code != 200:
                                            data_to_save.append({
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

                                        time.sleep(1)  # Пример задержки для демонстрации
                                    except Exception as e:
                                        data_to_save.append({
                                                    "Основная статья": h1_link_list,
                                                    "Ссылка на основную статью": href,
                                                    "Ошибка": "Некорректная ссылка",
                                                    "Текст ссылки в основной статье": l_l_text,
                                                    "Неработающая ссылка": href_checklink
                                                })
                                        print(e)
                            else:
                                print("Ссылки на странице новостей не найдены")
                        except Exception as e2:
                            print(f"Ошибка при обработке новости: {e2}")
                            print(n_l.text)
                            continue
                        
                        # Закрыть вкладку с новостью и вернуться на главную страницу
                        browser.close()
                        browser.switch_to.window(window_handles[0])
                    
                    # Проверка наличия следующей страницы
                    try:
                        str_list = browser.find_element(By.CLASS_NAME, "pagination")
                        str_list = str_list.find_elements(By.TAG_NAME, "a")
                        next_page_link = str_list[-2]  # последняя ссылка в списке - это следующая страница
                        if ">" in next_page_link.text:
                            next_page_link.click()
                            time.sleep(2)  # Дать время для загрузки следующей страницы
                        else:
                            print("Следующая страница не найдена, переход к следующей ссылке")
                            break
                    except Exception:
                        print("Конец парсинга.")
                        break

                # Создание Excel файла и запись данных для текущей страницы
                if data_to_save:
                    save_data(data_to_save, url)

                else:
                    print("Нет данных для сохранения.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
