from solver import Solver
from constants import *
import argparse
from logger import check_success_for_method
from os.path import exists


# TODO | от 10/04
# TODO | сделать разные реализации ввода данных такие как:
# TODO | .json (???), с помощью GUI (???)
# TODO | написать нормальное описание в --help
# TODO | тесты

_log_file = None
if exists(LOG_FILENAME):
    _log_file = open(LOG_FILENAME, "a")
else:
    _log_file = open(LOG_FILENAME, "w")


class Solution:
    global _log_file

    def __init__(self):
        parser = argparse.ArgumentParser(description=HELP_DESCRIPTION, formatter_class=argparse.RawTextHelpFormatter)

        parser.add_argument("method_in", help=HELP_METHOD_IN)

        parser.add_argument("method_out", help=HELP_METHOD_OUT)

        parser.add_argument("--input_file", "-if", help=HELP_INPUT_FILE, default="input.txt")

        parser.add_argument("--output_file", "-of", help=HELP_OUTPUT_FILE, default="output.txt")

        parser.add_argument("--count", "-c", help=HELP_COUNT, default=1, type=int)

        parser.add_argument("--debug", "-db", action="store_true", help=HELP_DEBUG)

        args = parser.parse_args()

        self.runnable = True

        method_in = args.method_in
        self.method_in = INPUT_METHODS.get(method_in)
        if self.method_in is None:
            print(EXCEPTION_INPUT_METHOD)
            self.runnable = False

        method_out = args.method_out
        self.method_out = OUTPUT_METHODS.get(method_out)
        if self.method_out is None:
            print(EXCEPTION_OUTPUT_METHOD)
            self.runnable = False

        self.input_file = args.input_file

        self.output_file = args.output_file

        self.count = args.count
        if self.count == 0:
            print(EXCEPTION_COUNT_SOLUTIONS)
            self.runnable = False

        if args.debug:
            DEBUG.switch_debug()

        self._solver = Solver()

    @check_success_for_method(_log_file)
    def solve(self):
        if self.runnable:
            self._solver.input_puzzle(self.method_in, self.input_file)
            self._solver.solve_puzzle(self.count)
            self._solver.output_solution(self.method_out, self.output_file)


if __name__ == "__main__":
    Solution().solve()