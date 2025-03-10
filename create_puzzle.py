from queue import Queue
import random
from copy import deepcopy


def pretty_print(graph: list[list]) -> None:
    for line in graph:
        print(*line)

def find_directions(n: int, cur_pos: tuple) -> list[tuple]:
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

# point = tuple(y, x)
def marking(graph: list[list], n: int, point1: tuple) -> list[list]:
    que = Queue()
    que.put((point1,))
    cur_mark = -1

    while not que.empty():
        positions = que.get()
        new_positions = []
        for cur_pos in positions:
            # up | right | down | left
            directions = find_directions(n, cur_pos)

            for direction in directions:
                if direction:
                    next_pos = (direction[0] + cur_pos[0], direction[1] + cur_pos[1])
                    if graph[next_pos[0]][next_pos[1]] == 0:
                        graph[next_pos[0]][next_pos[1]] = cur_mark
                        new_positions += [next_pos]

        if new_positions:
            que.put(tuple(new_positions))
        cur_mark -= 1

    return graph

# retuns all ways reaching from point1 to point2
def find_way(graph: list[list], n: int, point1: tuple, point2: tuple) -> list[list]:
    cur_graph = marking(deepcopy(graph), n, point1)
    all_ways = []
    pretty_print(cur_graph)

    def wrapper_find_way(cur_pos: tuple, used: list, way: list):
        nonlocal all_ways
        directions = find_directions(n, cur_pos)
        is_end = False

        for direction in directions:
            if direction:
                next_pos = (
                direction[0] + cur_pos[0], direction[1] + cur_pos[1])
                if next_pos == point2:
                    is_end = True
                if cur_graph[next_pos[0]][next_pos[1]] < 0 and used.count(next_pos) == 0:
                    wrapper_find_way(next_pos, used + [next_pos], way + [next_pos])

        if is_end:
            way += [point2]
            all_ways += [way]

    wrapper_find_way(point1, [point1], [point1])

    return all_ways

def find_point_positions(graph: list[list], point_mark: int):
    point_pos = []
    for idy, line in enumerate(graph):
        for idx, el in enumerate(line):
            if el == point_mark:
                point_pos += [(idy, idx)]

    return point_pos

def checkup_bruteforce(graph: list[list], n, cur, points_pos: list[list[tuple]]) -> list[list]:
    cur_graph = deepcopy(graph)
    for i in range(cur, n+1):
        paths = find_way(cur_graph, n, *points_pos[i-1])
        print(f"_________________ paths amount for {i} mark = {len(paths)}")
        if len(paths) == 0:
            return None
        for way in paths:
            markup_graph(cur_graph, way) # TODO
            checkup_bruteforce(cur_graph, n, cur+1, points_pos)

    return cur_graph



if __name__ == "__main__":
    graph = [[2, 0, 1, 6, 5, 0],
             [1, 0, 0, 0, 0, 0],
             [0, 0, 0, 4, 6, 0],
             [0, 2, 0, 0, 0, 0],
             [0, 0, 0, 3, 0, 5],
             [3, 0, 0, 0, 0, 4]]

    point_pos = []
    for i in range(1, 7):
        point_pos += [find_point_positions(graph, i)]

    checkup_bruteforce(graph, 6, 1, point_pos)

"""
test true
1 0 0 4 5
0 4 0 2 0
0 0 1 0 0
0 3 0 2 0
3 0 5 0 0
"""