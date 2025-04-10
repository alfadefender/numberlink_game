"""
Модуль <Solver> считывает головоломку, обрабатывает ее и выводит решение.

Реализована поддержка ввода:
    1). с консоли
    2). с файла

Реализован поддержка вывода:
    1). в консоль
    2). в файл
    3). в виде изображения

Используются дополнительные модули:
    1. PIL (pillow) - невстроенный модуль
"""


from constants import *
from logger import measure_time_console
from puzzle import Puzzle
from algorithm import the_least_distance_method
from PIL import Image, ImageDraw, ImageFont


class Solver:
    def __init__(self):
        self._puzzle = None

    def input_puzzle(self, method: int, filename: str = "input.txt"):
        size = 0
        count_points = 0
        graph = []

        if method == GRAPH_FROM_CONSOLE:
            size = int(input())
            count_points = int(input())
            for i in range(size):
                graph += [list(map(int, input().split()))]

        elif method == GRAPH_FROM_FILE:
            with open(filename) as file:
                size = int(file.readline())
                count_points = int(file.readline())
                for line in file:
                    graph += [list(map(int, line.split()))]

        self._puzzle = Puzzle(size, count_points, graph)

    def output_solution(self, method: int, filename: str = "output.txt"):
        if self._puzzle.is_solved():
            if method == GRAPH_TO_CONSOLE:
                for result_matrix, path in self._puzzle.get_result():
                    for line in result_matrix:
                        print(*line)
                    print("_________________")

            elif method == GRAPH_TO_FILE:
                with open(filename, "w") as file:
                    for result_matrix, path in self._puzzle.get_result():
                        for line in result_matrix:
                            print(*line, file=file)
                        print("_________________", file=file)

            elif method == GRAPH_TO_IMG:
                idx_image = 0
                size = self._puzzle.get_size()
                graph = self._puzzle.get_graph()
                for result_matrix, paths in self._puzzle.get_result():
                    image = Image.new("RGB", (size * 100, size * 100),
                                      "white")
                    draw = ImageDraw.Draw(image)
                    font = ImageFont.load_default(40)

                    for y in range(size):
                        for x in range(size):
                            number = graph[y][x]

                            draw.rectangle(
                                [x * 100, y * 100, x * 100 + 100, y * 100 + 100],
                                fill=COLORS[number])
                            if number:
                                if number // 10 > 0:
                                    draw.text((x * 100 + 25, y * 100 + 25),
                                              str(graph[y][x]), font=font,
                                              fill=(0, 0, 0))
                                else:
                                    draw.text((x * 100 + 37, y * 100 + 25),
                                              str(graph[y][x]), font=font,
                                              fill=(0, 0, 0))

                    for number, path in paths.items():
                        for y, x in path[1:-1]:
                            draw.rectangle(
                                [x * 100, y * 100, x * 100 + 100, y * 100 + 100],
                                fill=COLORS[number])

                    image.show()

                    image.save(f"images/solution_{idx_image}.png")

                    idx_image += 1

    @measure_time_console
    def solve_puzzle(self, count_results: int = 1):
        the_least_distance_method(self._puzzle, count_results)
