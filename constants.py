"""
Файл со всеми использующимися константами
"""
from random import randint

GRAPH_FROM_CONSOLE = 1
GRAPH_FROM_FILE = 2

GRAPH_TO_CONSOLE = 1
GRAPH_TO_FILE = 2
GRAPH_TO_IMG = 3

INPUT_METHODS = {
    "console_in": GRAPH_FROM_CONSOLE,
    "file_in": GRAPH_FROM_FILE
}

OUTPUT_METHODS = {
    "console_out": GRAPH_TO_CONSOLE,
    "file_out": GRAPH_TO_FILE,
    "img_out": GRAPH_TO_IMG
}

HELP_USAGE = """
Использование: main.py [-h] [--author] [--restart] [--method_in METHOD_IN]
                       [--method_out METHOD_OUT] [--input_file FILENAME]
                       [--output_file FILENAME] [--count COUNT_SOLUTIONS]
                       [--create_puzzle SIZE] [--debug]
"""

HELP_DESCRIPTION = """
Numberlink-solver - программа решающая головоломку Numberlink.

В первой строке - размер головоломки N.
Во второй строке - количество различных чисел.
В последующих строках головоломка.
Головоломка должна содержать числа идущие по (арифметическому) порядку.
Подробнее можно посмотреть в папке <examples>.

"""

HELP_HELP = """
\tВывод справки по программе.

"""

HELP_AUTHOR = """
\tПринудительные ссылки на преподавателя :)

"""

HELP_RESTART = """
\tВозобновление работы над предыдущей головоломки.

"""

HELP_METHOD_IN = """
\tМетод подачи входных данных
\t    [console_in] -> для ввода с консоли
\t    [file_in] -> для ввода с файла

"""

HELP_METHOD_OUT = """
\tМетод выдачи решения
\t    [console_out] -> для вывода в консоль
\t    [file_out] -> для вывода в файл
\t    [img_out] -> для вывода в картинку

"""

HELP_INPUT_FILE = """
\tАбсолютный или относительный путь входного файла (если есть)

"""

HELP_OUTPUT_FILE = """
\tАбсолютный или относительный путь выходного файла (если есть)
\tДля вывода ответа в картинку это поле не будет восприниматься
\tКаждое решение будет сохраняться в папке images

"""

HELP_COUNT = """
\tКоличество решений (число большее нуля)

"""

HELP_CREATE_PUZZLE = """
\tСоздание головоломки
\tВывод головоломки осуществляется согласно аргументам method_out и output_file

"""

HELP_DEBUG = """
\tФлаг для включения отладки

"""

EXCEPTION_INPUT_METHOD = """Произошло исключение: некорректный метод ввода
Возможные методы:
\t1. console_in
\t2. file_in
"""
EXCEPTION_OUTPUT_METHOD = """Произошло исключение: некорректный метод вывода
Возможные методы:
\t1. console_out
\t2. file_out
\t3. img_out
"""
EXCEPTION_COUNT_SOLUTIONS = """Произошло исключение: некорректное число решений
Число решений обязано быть числом большим нуля
"""

EXCEPTION_GENERATOR_SIZE = """Произошло исключение: некорректный размер
головоломки. Размер головоломки обязан быть числом большим нуля
"""

COLORS = {
    0: (255, 255, 255)
}

for idx in range(1, 30):
    COLORS[idx] = tuple(randint(25, 230) for _ in range(3))

LOG_FILENAME = "assets/logs.txt"
