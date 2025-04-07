from solver import Solver
from constants import *


# TODO | сделать разные реализации ввода данных такие как:
# TODO | <.txt>, .json, <console>, с помощью GUI (???)
# TODO | нужно иметь возможность влиять на поведение программы с помощью
# TODO | аргументов командной строки, а также документацию и help

class Solution:
    def __init__(self):
        self._solver = Solver()

    def solve(self,
              method_in,
              method_out,
              input_file="input.txt",
              output_file="output.txt",
              count_solutions=1):

        self._solver.input_puzzle(method_in, input_file)
        self._solver.solve_puzzle(count_solutions)
        self._solver.output_solution(method_out, output_file)


if __name__ == "__main__":
    Solution().solve(GRAPH_FROM_FILE, GRAPH_TO_IMG, input_file="graph10.txt", count_solutions=3)