from queue import Queue
from copy import deepcopy
from time import time


DEBUG = False


# debug only
class Logger:
    def __init__(self, filename=None):
        self.filename = filename
        self.file = None
        if filename and DEBUG:
            self.file = open(filename, "w")

    def graph_pretty_print(self, graph: list[list], to_file: bool = False):
        if DEBUG:
            if to_file:
                for line in graph:
                    print(*line, file=file)
            else:
                for line in graph:
                    print(*line)

    def log_print(self, text, to_file: bool = False):
        if DEBUG:
            if to_file:
                print(text, file=self.file)
            else:
                print(text)

    def algorithm_print_new_iteration(self, mark: int, to_file: bool = False):
        if DEBUG:
            if to_file:
                print(f"_________________ iteration _________________",
                      file=self.file)
                print(f"______________ cur mark = {mark} _____________",
                      file=self.file)
            else:
                print(f"_________________ iteration _________________")
                print(f"______________ cur mark = {mark} _____________")

    def algorithm_print_new_way(self, mark: int, way: list,
                                to_file: bool = False):
        if DEBUG:
            if to_file:
                print(f"____________ new way for {mark} is {way}", file=self.file)
            else:
                print(f"____________ new way for {mark} is {way}")

    def algorithm_print_skip(self, to_file: bool = False):
        if DEBUG:
            if to_file:
                print("_____________SKIP____________", file=self.file)
            else:
                print("_____________SKIP____________")

    def algorithm_print_back(self, to_file: bool = False):
        if DEBUG:
            if to_file:
                print("_____________BACK____________", file=self.file)
            else:
                print("_____________BACK____________")

    def algorithm_print_succeed(self, to_file: bool = False):
        if DEBUG:
            if to_file:
                print("*******************HAPPY************************",
                      file=self.file)
            else:
                print("*******************HAPPY************************")

    def print_spaces(self, count: int, to_file: bool = False):
        if DEBUG:
            print("\n" * count)


# поиск возможных направлений для текущей точки относительно матрицы
# роза направлений - вверх, вправо, вниз, влево
def _find_directions(n: int, cur_pos: tuple) -> list[tuple]:
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


# оптимизационная проверка поиска возможных путей, использующаяся, чтобы
# отбросить заведомо "плохие" построенные пути
def _check_points(point1: tuple, point2: tuple, n: int,
                  graph: list[list]) -> bool:
    if DEBUG:
        print(f"CHECK POINTS ENTER: {point1}, {point2}")

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
                    if DEBUG:
                        print(f"CHECK POINTS EXIT WITH TRUE: {point1}, {point2}")
                    return True

                if graph[next_point[0]][next_point[1]] == 0 and used.count(
                        next_point) == 0:
                    used += [next_point]
                    que.put(next_point)

    if DEBUG:
        print(f"CHECK POINTS EXIT WITH FALSE: {point1}, {point2}")
    return False


# основная функция поиска путей, является генератором
def _find_way(graph: list[list], n: int, point1: tuple, point2: tuple) -> list:
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


# для конкретного числа находит в матрице, где они находятся
def _find_point_positions(graph: list[list], point_mark: int):
    point_pos = []
    for idy, line in enumerate(graph):
        for idx, el in enumerate(line):
            if el == point_mark:
                point_pos += [(idy, idx)]

    return point_pos


# наносит полученный путь на копию матрицы и возвращает её
def _markup_graph(cur_graph: list[list], way: list[int], cur: int) -> list[list]:
    deep_graph = deepcopy(cur_graph)
    for point in way:
        deep_graph[point[0]][point[1]] = cur
    return deep_graph


# возвращает очередь из пар точек чисел в соответствии с первоначальным
# алгоритмом поиска пар чисел по наименьшему расстоянию между ними
def _queue_points(points_pos: list[list[tuple]]):
    points = [(idx + 1, ((first[0] - second[0]) ** 2 + (
                first[1] - second[1]) ** 2) ** 0.5) for idx, (first, second) in
              enumerate(points_pos)]
    points = sorted(points, key=lambda x: x[1])
    return [idx for idx, distance in points]


# основной метод поиска возможных решений
# используется необоснованная оптимизация с меньшим расстоянием между парами
# чисел и полный перебор с оптимизацией: предварительная проверка пути на
# помеху другим парам чисел
# переменная puzzle обязана быть типа "Puzzle"
def the_least_distance_method(puzzle, count_results: int = 1):
    if puzzle.is_empty():
        return []

    graph = puzzle.get_graph()
    n = puzzle.get_size()
    count_points = puzzle.get_count_points()
    logger = Logger("output.txt")

    points_pos = []
    results = []

    for i in range(1, count_points + 1):
        points_pos += [_find_point_positions(graph, i)]

    t1 = round(time() * 1000)

    def _the_least_distance(graph: list[list],
                            n: int,
                            points_queue: list[int]):

        nonlocal results

        if len(results) >= count_results:
            logger.algorithm_print_skip()
            return None

        if len(points_queue) == 0:
            results += [deepcopy(graph)]
            logger.algorithm_print_succeed()
            return None

        cur_graph = deepcopy(graph)

        for point in points_queue:
            if not _check_points(*points_pos[point - 1], n, cur_graph):
                logger.algorithm_print_back()
                return

        paths = _find_way(cur_graph, n, *points_pos[points_queue[0] - 1])
        logger.algorithm_print_new_iteration(points_queue[0])
        logger.graph_pretty_print(cur_graph)

        for way in paths:
            if len(results) >= count_results:
                break

            logger.algorithm_print_new_way(points_queue[0], way)
            puzzle.set_new_path(points_queue[0], way)

            temp_mark = points_queue.pop(0)
            _the_least_distance(_markup_graph(cur_graph, way, temp_mark),
                                n,
                                points_queue)
            points_queue.insert(0, temp_mark)

        logger.algorithm_print_back()

    _the_least_distance(graph, n, _queue_points(points_pos))

    for g in results:
        logger.print_spaces(2)
        logger.graph_pretty_print(g)
    logger.log_print(f"{round(time() * 1000) - t1} ms")

    return results


if __name__ == "__main__":

    graph5 = [[1, 0, 0, 5, 4],
              [0, 5, 0, 2, 0],
              [0, 0, 1, 0, 0],
              [0, 3, 0, 2, 0],
              [3, 0, 4, 0, 0]]

    graph6 = [[2, 0, 1, 6, 5, 0],
              [1, 0, 0, 0, 0, 0],
              [0, 0, 0, 4, 6, 0],
              [0, 2, 0, 0, 0, 0],
              [0, 0, 0, 3, 0, 5],
              [3, 0, 0, 0, 0, 4]]

    graph7 = [[1, 0, 0, 3, 0, 0, 4],
              [0, 0, 0, 0, 0, 6, 7],
              [0, 5, 0, 2, 0, 0, 0],
              [0, 0, 3, 0, 0, 0, 0],
              [0, 0, 0, 0, 4, 0, 7],
              [0, 0, 0, 0, 0, 6, 2],
              [0, 1, 0, 5, 0, 0, 0]]

    graph8 = [[1, 0, 0, 8, 0, 0, 0, 3],
              [0, 0, 3, 0, 0, 0, 0, 7],
              [0, 0, 0, 7, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 4, 0, 6, 0],
              [0, 0, 0, 0, 0, 6, 5, 0],
              [0, 8, 0, 2, 0, 0, 0, 0],
              [0, 0, 1, 0, 4, 5, 0, 2]]

    graph10 = [[6, 0, 0, 0, 0, 8, 0, 0, 4, 10],
             [1, 0, 0, 0, 6, 7, 0, 4, 10, 0],
             [0, 0, 0, 0, 7, 0, 0, 0, 0, 8],
             [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 5, 0, 0, 3, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 9, 5, 9, 0, 0, 0, 2, 0],
             [2, 0, 0, 0, 0, 0, 3, 0, 0, 0]]

    graph11 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [8, 11, 0, 0, 0, 11, 8, 0, 0, 7, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 4],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
               [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
               [0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 6, 5, 0],
               [0, 0, 0, 0, 0, 0, 5, 10, 0, 10, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 3],
               [4, 7, 0, 0, 0, 1, 3, 0, 0, 0, 0]]

    graph14 = [[8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
               [16, 0, 0, 0, 0, 6, 4, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 15, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0],
               [0, 0, 0, 0, 0, 7, 0, 0, 4, 0, 0, 0, 0, 0],
               [0, 13, 0, 9, 7, 5, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 12, 0, 0, 3],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
               [0, 0, 0, 0, 0, 0, 10, 0, 11, 0, 0, 0, 2, 0],
               [9, 10, 11, 0, 0, 0, 0, 0, 12, 0, 3, 2, 1, 0]]

    graph15 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 0, 0, 13],
               [0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 13, 0],
               [0, 0, 0, 0, 3, 6, 0, 8, 7, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0],
               [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0],
               [0, 0, 0, 0, 0, 0, 3, 1, 6, 0, 0, 0, 0, 0, 0],
               [0, 12, 0, 0, 1, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 0],
               [0, 0, 0, 0, 0, 0, 5, 12, 10, 0, 0, 0, 0, 15, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 0, 4]]
