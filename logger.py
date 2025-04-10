"""
Модуль с декораторами обработки ошибок и подсчета времени работы программы
"""

import time
import traceback


def _format_time(time: float) -> str:
    """
    форматирование времени в виде <..., ? h, ? min, ? sec, ? ms>

    :param time: время <float> типа
    :return: возвращает результирующую строку
    """

    int_time = int(time)
    milliseconds = round((time - int_time) * 1000)
    result = f"{milliseconds} ms"
    if int_time == 0:
        return result

    seconds = int_time % 60
    int_time //= 60
    result = f"{seconds} sec, " + result

    if int_time == 0:
        return result

    minutes = int_time % 60
    int_time //= 60
    result = f"{minutes} min, " + result

    if int_time == 0:
        return result

    hours = int_time % 24
    int_time //= 24
    result = f"{hours} h, " + result

    if int_time == 0:
        return result
    return f"..., " + result


def check_success_for_method(file: open):
    """
    Декоратор для отлова ошибок и замера времени выполнения программы.
    Применяется только для функции solve класса Solution, дабы обобщить результат

    :param file: передается объект типа <open>
    :return: обернутая функция
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            result = None

            try:
                start_time = time.monotonic()
                result = func(*args, **kwargs)
                end_time = time.monotonic()
                time_spent = _format_time(end_time - start_time)

                # в лог-файл
                print(
                    f"[{time.ctime(time.time())}] - INFO - Puzzle is solved successfully",
                    file=file)
                print(f"\tTime spent : {time_spent}", file=file)

            except Exception as e:

                # в лог-файл
                print(
                    f"[{time.ctime(time.time())}] - ERROR - !!! Caught exception !!!",
                    file=file)
                print(f"\tType of exception : {e.__class__.__name__}",
                      file=file)
                print(f"\tText of exception : {str(e)}", file=file)
                traceback.print_exc(file=file)

                # вывод для пользователя
                print(f"!!! Была обработана некорректная ситуация !!!")
                print(f"\tТип ошибки : {e.__class__.__name__}")
                print(f"\tТекст ошибки : {str(e)}")
                print(f"Проверьте файл <logs.txt> для большей информации.")

            return result

        return wrapper

    return decorator


def measure_time_console(func):
    """
    Декоратор для замера времени выполнения алгоритма.
    Применяется только для функции solve_puzzle класса Solver,
    для показа пользователю времени решения головоломки

    :param func: функция
    :return: обернутая функция
    """

    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        print("Потрачено времени на решение : " + _format_time(
            end_time - start_time))

        return result

    wrapper.__name__ = func.__name__
    return wrapper


# Not used
def __measure_time_file(file=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.monotonic()
            result = func(*args, **kwargs)
            end_time = time.monotonic()

            if file is None:
                print(end_time - start_time, "s")
            else:
                print(end_time - start_time, "s", file=file)

            return result

        wrapper.__name__ = func.__name__
        return wrapper

    return decorator
