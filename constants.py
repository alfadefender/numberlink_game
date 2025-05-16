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

HELP_DESCRIPTION = """
Numberlink-solver - программа решающая головоломку Numberlink.

В первой строке - размер головоломки N.
Во второй строке - количество различных чисел.
В последующих строках головоломка.
Головоломка должна содержать числа идущие по (арифметическому) порядку.
Подробнее можно посмотреть в папке <examples>.
"""

HELP_AUTHOR = """
Принудительные ссылки на преподавателя :)
"""

HELP_RESTART = """
Возобновление работы над предыдущей головоломки.
"""

HELP_METHOD_IN = """
Метод подачи входных данных
    [console_in] -> для ввода с консоли
    [file_in] -> для ввода с файла
"""

HELP_METHOD_OUT = """
Метод выдачи решения
    [console_out] -> для вывода в консоль
    [file_out] -> для вывода в файл
    [img_out] -> для вывода в картинку
"""

HELP_INPUT_FILE = """
Абсолютный или относительный путь входного файла (если есть)
"""

HELP_OUTPUT_FILE = """
Абсолютный или относительный путь выходного файла (если есть)
Для вывода ответа в картинку это поле не будет восприниматься
Каждое решение будет сохраняться в папке images
"""

HELP_COUNT = """
Количество решений (число большее нуля)
"""

HELP_CREATE_PUZZLE = """
Создание головоломки
Вывод головоломки осуществляется согласно аргументам method_out и output_file
"""

HELP_DEBUG = """
Флаг для включения отладки
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
