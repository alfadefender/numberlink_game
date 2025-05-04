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
import os

from constants import *
from logger import measure_time_console
from puzzle import Puzzle
from algorithm import the_least_distance_method
from PIL import Image, ImageDraw, ImageFont
import json


class Solver:
    def __init__(self, settings: dict):
        self._puzzle = None
        self._settings = settings
        self._restarting = settings.get("restart_flag")
        self._method_out = settings.get("method_out")

    def checkup_previous(self) -> bool:
        if not self._restarting:
            return False

        result = True
        try:
            with open("assets/prev.json") as prev_json:
                self._method_out, size, count, graph = json.load(prev_json)
                self._puzzle = Puzzle(size, count, graph)
        except Exception as e:
            result = False

        return result

    # методы для создания головоломки
    def setup_puzzle(self, puzzle: Puzzle):
        self._puzzle = puzzle

    def output_puzzle(self, method: int, filename: str = "output.txt"):
        """
        Вывод головоломки

        :param method:      параметр вывода, указанный в константах
        :param filename:    путь до файла
        """

        if method == GRAPH_TO_CONSOLE:
            for line in self._puzzle.get_graph():
                print(*line)
            print("_________________")

        elif method == GRAPH_TO_FILE:
            with open(filename, "w") as file:
                for line in self._puzzle.get_graph():
                    print(*line, file=file)

        elif method == GRAPH_TO_IMG:
            size = self._puzzle.get_size()
            graph = self._puzzle.get_graph()
            image = Image.new("RGB", (size * 100, size * 100),
                              "white")
            draw = ImageDraw.Draw(image)
            font = ImageFont.load_default(40)

            for y in range(size):
                for x in range(size):
                    number = graph[y][x]

                    draw.rectangle(
                        [x * 100, y * 100, x * 100 + 100,
                         y * 100 + 100],
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

            image.save(f"images/new_graph.png")

    # методы для обычного считывания и решения
    def input_puzzle(self, method: int, filename: str = "input.txt"):
        """
        Ввод данных головоломки

        :param method:      параметр ввода, указанный в константах
        :param filename:    путь до файла
        :return:            присваивает значение полю <self._puzzle>
        """

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
        with open("assets/prev.json", "w") as prev_json:
            json.dump([self._method_out, size, count_points, graph], prev_json)

    def output_solution(self, filename: str = "output.txt"):
        """
        Вывод решений головоломки

        :param filename: путь до файла
        """

        if self._puzzle.is_solved():
            if self._method_out == GRAPH_TO_CONSOLE:
                for result_matrix, path in self._puzzle.get_result():
                    for line in result_matrix:
                        for elem in line:
                            temp = f"{(4 - len(str(elem))) * ' '}{elem}"
                            print(temp, end="|")

                    print("_________________")

            elif self._method_out == GRAPH_TO_FILE:
                with open(filename, "w") as file:
                    for result_matrix, path in self._puzzle.get_result():
                        for line in result_matrix:
                            for elem in line:
                                temp = f"{(4 - len(str(elem))) * ' '}{elem}"
                                print(temp, end="|", file=file)
                        print("_________________", file=file)

            elif self._method_out == GRAPH_TO_IMG:
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
                                [x * 100, y * 100, x * 100 + 100,
                                 y * 100 + 100],
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
                                [x * 100, y * 100, x * 100 + 100,
                                 y * 100 + 100],
                                fill=COLORS[number])

                    image.save(f"images/solution_{idx_image}.png")

                    idx_image += 1

            try:
                os.remove("./assets/prev.json")
            except BaseException:
                pass

    @measure_time_console
    def solve_puzzle(self, count_results: int = 1):
        """
        Запуск метода решения головоломки

        :param count_results: количество решений, которые необходимо получить
        """
        the_least_distance_method(self._puzzle, count_results)
