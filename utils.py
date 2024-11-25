import time


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
