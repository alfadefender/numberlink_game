from constants import *
from algorithm import the_least_distance_method
from PIL import Image, ImageDraw, ImageFont


class Puzzle:
    def __init__(self, method_in: int, method_out: int):
        self._size = 0
        self._graph = []
        self._count_points = 0

        self._input_method = method_in
        self._output_method = method_out
        self._filename = None

        self._result = []
        self._paths = {}
        self._status = False

    def get_graph(self):
        return self._graph

    def get_size(self):
        return self._size

    def get_count_points(self):
        return self._count_points

    def is_empty(self):
        return self._size == 0 or self._graph == [] or self._count_points == 0

    def set_new_path(self, result: int, mark: int, path: list):
        self._paths[result][mark] = path

    def solve_puzzle(self, count_results: int = 1):
        if not self._status:
            self._result = the_least_distance_method(self, count_results)
            self._status = True

    def console_input(self):
        try:
            self._size = int(input())
            self._count_points = int(input())
            for i in range(self._size):
                self._graph += [list(map(int, input().split()))]

        except Exception as e:
            print(e)

    def file_input(self):
        try:
            with open(self._filename) as file:
                self._size = int(file.readline())
                self._count_points = int(file.readline())
                for line in file:
                    self._graph += [list(map(int, line.split()))]

        except Exception as e:
            print(e)

    # основная функция ввода
    def input_puzzle(self, filename=None):
        if self._input_method == GRAPH_FROM_CONSOLE:
            self.console_input()
        elif self._input_method == GRAPH_FROM_FILE:
            self._filename = filename
            self.file_input()

    def console_output(self):
        if not self._status:
            print("Not solved yet")
            return

        if not self._result:
            print("No solutions")
            return

        for matrix in self._result:
            for line in matrix:
                print(*line)
            print("_________________")

    def file_output(self):
        pass

    def img_output(self):
        if self.is_empty():
            return

        for

        image = Image.new("RGB", (self._size * 100, self._size * 100), "white")
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default(40)

        for y in range(self._size):
            for x in range(self._size):
                number = self._graph[y][x]

                draw.rectangle(
                    [x * 100, y * 100, x * 100 + 100, y * 100 + 100],
                    fill=COLORS[number])
                if number:
                    if number // 10 > 0:
                        draw.text((x * 100 + 25, y * 100 + 25),
                                  str(self._graph[y][x]), font=font,
                                  fill=(0, 0, 0))
                    else:
                        draw.text((x * 100 + 37, y * 100 + 25),
                                  str(self._graph[y][x]), font=font,
                                  fill=(0, 0, 0))

        for number, path in self._paths.items():
            for y, x in path[1:-1]:
                draw.rectangle(
                [x * 100, y * 100, x * 100 + 100, y * 100 + 100],
                fill=COLORS[number])

        image.show()

        image.save("proba.png")

    # основная функция вывода ответа
    def output_answer(self):
        if self._output_method == GRAPH_TO_CONSOLE:
            self.console_output()
        elif self._output_method == GRAPH_TO_FILE:
            self.file_output()
        elif self._output_method == GRAPH_TO_IMG:
            self.img_output()
