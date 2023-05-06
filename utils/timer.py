import time


def timer(func):
    """Декоратор подсчета времени выполнения функции"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Работа программы завершена! Время выполнения': {round(end_time - start_time)} секунд")

        return result

    return wrapper
