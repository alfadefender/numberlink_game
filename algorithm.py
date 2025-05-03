"""
Модуль реализующий алгоритм нахождения решения по заданной головоломке.

На текущий момент только одна функция решает поставленную задачу:
    <the_least_distance_method>

Для решения задачи используется полный перебор с оптимизациями:
    1). Для начала выбираются пары чисел, расстояние между которыми наименьшее
    2). Прежде чем искать новые пути на построенном текущем, идет проверка
        есть ли пути у всех оставшихся пар чисел

Использованы дополнительные встроенные модули:
    1). queue
    2). copy
    3). time

Для дебаг-режима имеется контекстный менеджер <Logger>.
Он используется только тут.
"""

from queue import Queue
from copy import deepcopy
import time
from puzzle import Puzzle
from dbm import DEBUG
import json


class Logger:
    """
    Используется только в этом файле для отладки шагов алгоритма
    """

    def __init__(self, filename=None):
        self.filename = filename
        self.file = None
        self.temp_paths = {}
        self.tempfile = "assets/temp_logs.json"

    def __enter__(self):
        if self.filename and DEBUG.get_flag():
            self.file = open(self.filename, "w")
            self.file.write(f"Current session {time.ctime(time.time())}\n\n")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.filename and DEBUG.get_flag():
            self.file.close()

    def graph_pretty_print(self, graph: list[list]):
        if DEBUG.get_flag():
            for line in graph:
                print(*line, file=self.file)

    def log_print(self, text):
        if DEBUG.get_flag():
            print(text, file=self.file)

    def algorithm_print_new_iteration(self, mark: int):
        if DEBUG.get_flag():
            print(f"_________________ iteration _________________",
                  file=self.file)
            print(f"______________ cur mark = {mark} _____________",
                  file=self.file)

    def algorithm_print_new_way(self, mark: int, way: list):
        if DEBUG.get_flag():
            print(f"____________ new way for {mark} is {way}", file=self.file)

    def algorithm_print_skip(self):
        if DEBUG.get_flag():
            print("_____________SKIP____________", file=self.file)

    def algorithm_print_back(self):
        if DEBUG.get_flag():
            print("_____________BACK____________", file=self.file)

    def algorithm_print_succeed(self):
        if DEBUG.get_flag():
            print("*******************HAPPY************************",
                  file=self.file)

    def print_spaces(self, count: int):
        if DEBUG.get_flag():
            print("\n" * count, file=self.file)

    def save_path_local(self, mark : int, path : list):
        self.temp_paths[mark] = path

    @staticmethod
    def checkpoint(self):
        with open(self.temp_paths, "w") as file:
            json.dump(self.temp_paths, file)

    @staticmethod
    def get_checkpoint(self) -> dict:
        with open(self.temp_paths) as file:
            self.temp_paths = json.load(file)

        return self.temp_paths


def _find_directions(n: int, cur_pos: tuple) -> list[tuple]:
    """
    поиск возможных направлений для текущей точки относительно матрицы
    роза направлений - вверх, вправо, вниз, влево

    :param n: размер поля
    :param cur_pos: текущая точка
    :return: возвращает список направлений
    """

    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    if cur_pos[0] == 0:  # строка idx=0 => вверх нельзя
        directions[0] = 0
    if cur_pos[1] == n - 1:  # столбец idx=n-1 => вправо нельзя
        directions[1] = 0
    if cur_pos[0] == n - 1:  # строка idx=n-1 => вниз нельзя
        directions[2] = 0
    if cur_pos[1] == 0:  # столбец idx=0 => влево нельзя
        directions[3] = 0

    return directions


def _check_points(point1: tuple, point2: tuple, n: int,
                  graph: list[list], logger: Logger) -> bool:
    """
    оптимизационная проверка поиска возможных путей, использующаяся, чтобы
    отбросить заведомо "плохие" построенные пути

    :param point1: начальная точка
    :param point2: конечная точка
    :param n: размер поля
    :param graph: матрица поля
    :param logger: логгер для отладки
    :return: возвращает true если путь между двумя точками есть, иначе - false
    """

    logger.log_print(f"CHECK POINTS ENTER: {point1}, {point2}")

    que = Queue()
    used = [point1]
    que.put(point1)

    while not que.empty():
        cur_point = que.get()
        directions = _find_directions(n, cur_point)

        for direction in directions:
            if direction:
                next_point = (
                    direction[0] + cur_point[0], direction[1] + cur_point[1])
                if next_point == point2:
                    logger.log_print(
                        f"CHECK POINTS EXIT WITH TRUE: {point1}, {point2}")
                    return True

                if graph[next_point[0]][next_point[1]] == 0 and used.count(
                        next_point) == 0:
                    used += [next_point]
                    que.put(next_point)

    logger.log_print(f"CHECK POINTS EXIT WITH FALSE: {point1}, {point2}")
    return False


def _find_way(graph: list[list], n: int, point1: tuple, point2: tuple) -> list:
    """
    основная функция поиска путей, является генератором

    :param graph: матрица поля
    :param n: размер поля
    :param point1: начальная точка
    :param point2: конечная точка
    :return: генерирует следующий путь между двумя точками
    """

    que = Queue()
    que.put([point1])

    while not que.empty():
        cur_way = que.get()
        cur_point = cur_way[-1]
        directions = _find_directions(n, cur_point)

        for direction in directions:
            if direction:
                next_point = (
                    direction[0] + cur_point[0], direction[1] + cur_point[1])
                if next_point == point2:
                    yield cur_way + [next_point]

                if graph[next_point[0]][next_point[1]] == 0 and cur_way.count(
                        next_point) == 0:
                    que.put(deepcopy(cur_way + [next_point]))


def _find_point_positions(graph: list[list], point_mark: int) -> list[tuple]:
    """
    для конкретного числа находит в матрице, где они находятся

    :param graph: матрица поля
    :param point_mark: метка пары чисел
    :return: возвращает список позиций пары чисел для данной метки
    """

    point_pos = []
    for idy, line in enumerate(graph):
        for idx, el in enumerate(line):
            if el == point_mark:
                point_pos += [(idy, idx)]

    return point_pos


def _markup_graph(cur_graph: list[list], way: list[int], cur: int) -> \
        list[list]:
    """
    наносит полученный путь на копию матрицы и возвращает её

    :param cur_graph: матрица поля
    :param way: путь
    :param cur: метка пары чисел
    :return: возвращает копию матрицы поля с наложенным на нее путем
    """

    deep_graph = deepcopy(cur_graph)
    for point in way:
        deep_graph[point[0]][point[1]] = cur
    return deep_graph


def _queue_points(points_pos: list[list[tuple]]) -> list[list[tuple]]:
    """
    возвращает очередь из пар точек чисел в соответствии с первоначальным
    алгоритмом поиска пар чисел по наименьшему расстоянию между ними

    :param points_pos: список списков пар точек
    :return: возвращает упорядоченный список
    """

    points = [(idx + 1, ((first[0] - second[0]) ** 2 + (
            first[1] - second[1]) ** 2) ** 0.5) for idx, (first, second) in
              enumerate(points_pos)]
    points = sorted(points, key=lambda x: x[1])
    return [idx for idx, distance in points]


def the_least_distance_method(puzzle: Puzzle, count_results: int = 1) -> None:
    """
    основной метод поиска возможных решений
    используется необоснованная оптимизация с меньшим расстоянием между парами
    чисел и полный перебор с оптимизацией: предварительная проверка пути на
    помеху другим парам чисел
    переменная puzzle обязана быть типа "Puzzle"

    :param puzzle: внутреннее представление головоломки <Puzzle>
    :param count_results: количество решений
    :return: результаты складываются во внутреннее представление
    """

    if puzzle.is_empty():
        return []

    cur_time = time.localtime()
    format_time = time.strftime("%Y_%m_%d--%H_%M_%S", cur_time)

    with Logger(f"assets/algorithm_logs_{format_time}.txt") as logger:
        graph = puzzle.get_graph()
        n = puzzle.get_size()
        count_points = puzzle.get_count_points()

        points_pos = []
        results = []
        current_path = {}
        all_paths = []

        for i in range(1, count_points + 1):
            points_pos += [_find_point_positions(graph, i)]

        t1 = round(time.time() * 1000)

        def _the_least_distance(graph: list[list],
                                n: int,
                                points_queue: list[int]):

            nonlocal results, current_path, all_paths

            if len(results) >= count_results:
                logger.algorithm_print_skip()
                return None

            if len(points_queue) == 0:
                results += [deepcopy(graph)]
                all_paths += [deepcopy(current_path)]
                logger.algorithm_print_succeed()
                return None

            cur_graph = deepcopy(graph)

            for point in points_queue:
                if not _check_points(*points_pos[point - 1], n, cur_graph,
                                     logger):
                    logger.algorithm_print_back()
                    return

            paths = _find_way(cur_graph, n, *points_pos[points_queue[0] - 1])
            logger.algorithm_print_new_iteration(points_queue[0])
            logger.graph_pretty_print(cur_graph)

            for way in paths:
                if len(results) >= count_results:
                    break

                logger.algorithm_print_new_way(points_queue[0], way)
                logger.temp_paths[points_queue[0]] = way

                current_path[points_queue[0]] = way

                temp_mark = points_queue.pop(0)
                _the_least_distance(_markup_graph(cur_graph, way, temp_mark),
                                    n,
                                    points_queue)
                points_queue.insert(0, temp_mark)

            logger.algorithm_print_back()

        _the_least_distance(graph, n, _queue_points(points_pos))

        for g in results:
            logger.print_spaces(2)
            logger.log_print("New solution")
            logger.graph_pretty_print(g)
        logger.log_print(f"{round(time.time() * 1000) - t1} ms")

        puzzle.set_is_solved()
        puzzle.set_result(results)
        puzzle.set_paths(all_paths)
