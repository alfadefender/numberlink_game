from copy import deepcopy
from random import randint, choice, shuffle
from queue import Queue

from puzzle import Puzzle


def _get_next_points(n: int, cur_point: tuple) -> list[tuple]:
    """
    Возвращает следующие точки относительно текущей точки и поля
    (роза направлений)
    """
    next_points = [
        (cur_point[0] - 1, cur_point[1]),
        (cur_point[0], cur_point[1] - 1),
        (cur_point[0] + 1, cur_point[1]),
        (cur_point[0], cur_point[1] + 1)
    ]

    return list(filter(lambda x: 0 <= x[0] < n and 0 <= x[1] < n, next_points))


def _find_new_way(n: int, graph: list[list[int]], start_point: tuple) -> dict:
    """
    Метод поиска нового пути в графе от заданной точки, до случайной,
    с маркировкой поля graph

    :param n:           размер головоломки
    :param graph:       представление головоломки
    :param start_point: заданная точка
    :return:            возвращает dict-объект с полями:
                        "start", "end", "len", "path"
    """
    used = set(start_point)
    que = Queue()
    que.put((start_point,))
    len_path = randint(2, int(n / 1.5))
    path = ()

    while not que.empty() and not path:
        cur_path = que.get()
        cur_point = cur_path[-1]

        next_points = _get_next_points(n, cur_point)
        shuffle(next_points)

        for y, x in next_points:
            if ((start_point[0] - y) ** 2 + (
                    start_point[1] - x) ** 2) ** 0.5 > len_path:
                path = deepcopy(cur_path)

            if not graph[y][x] and (y, x) not in used:
                used.add((y, x))
                que.put((*cur_path, (y, x)))

    for y, x in path:
        graph[y][x] = 1

    return {
        "start": start_point,
        "end": path[-1],
        "path": path,
        "len": len_path
    }


def _get_empty_cell(n: int, graph: list[list[int]]) -> tuple:
    """
    Возвращает случайную ячейку с 0 из graph
    """
    cells = []
    for y in range(n):
        for x in range(n):
            if graph[y][x] == 0:
                cells += [(y, x)]

    return choice(cells)


def generate_puzzle(n: int) -> Puzzle:
    """
    Генерирует головоломку квадратных размеров NxN

    :param n:   размер головоломки
    :return:    головоломка в виде объекта Puzzle
    """
    graph = [[0 for _ in range(n)] for _ in range(n)]

    len_points = randint(n - 1, n + 1)
    marks = dict()
    cur_mark = 1

    for _ in range(len_points):
        start_point = _get_empty_cell(n, graph)

        returned_value = _find_new_way(n, graph, start_point)

        marks[cur_mark] = returned_value
        cur_mark += 1

    returned_graph = [[0 for _ in range(n)] for _ in range(n)]

    for mark, settings in marks.items():
        y0, x0 = settings.get("start")
        y, x = settings.get("end")
        returned_graph[y0][x0] = mark
        returned_graph[y][x] = mark

    return Puzzle(n, len(marks), returned_graph)


if __name__ == "__main__":
    n = 12
    puzzle = generate_puzzle(n)
    for line in puzzle._graph:
        print(*line)
