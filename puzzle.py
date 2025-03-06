class Method:
    pass

class ConsoleMethod(Method):
    pass

class FileMethod(Method):
    pass


class Puzzle:
    def __init__(self, method: Method):
        self._size = 0
        self._graph = []
        self._method = method

    def is_empty(self):
        return self._size == 0 or self._graph == []

    def console_input(self):
        self._size = int(input())
        for i in range(self._size):
            self._graph += [list(map(int, input().split()))]

    def file_input(self):
        pass

    def input_puzzle(self):
        match self._method:
            case ConsoleMethod():
                self.console_input()
            case FileMethod():
                self.file_input()

    def console_output(self):
        if self.is_empty():
            print("Empty Puzzle")
            return
        for line in self._graph:
            print(*line)

    def file_output(self):
        pass

    def output_puzzle(self):
        match self._method:
            case ConsoleMethod():
                self.console_output()
            case FileMethod():
                self.file_output()