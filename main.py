"""
Главный модуль запускающий программу

В классе <Solution> реализуется CLI.
"""
import sys

from solver import Solver
from constants import *
from dbm import DEBUG
import argparse
from logger import check_success_for_method
from os.path import exists
from generator import generate_puzzle

# TODO | от 10/04
# TODO | написать нормальное описание в --help
# TODO | возобновление работы при некорректном завершении программы
# TODO | тесты

_log_file = None
if exists(LOG_FILENAME):
    _log_file = open(LOG_FILENAME, "a")
else:
    _log_file = open(LOG_FILENAME, "w")


class Solution:
    global _log_file

    def __init__(self):
        parser = argparse.ArgumentParser(
            description=HELP_DESCRIPTION,
            formatter_class=argparse.RawTextHelpFormatter
        )

        parser.add_argument("--restart",
                            "-r",
                            action="store_true",
                            help=HELP_RESTART)

        parser.add_argument("--method_in",
                            "-mi",
                            default=GRAPH_FROM_CONSOLE,
                            help=HELP_METHOD_IN)

        parser.add_argument("--method_out",
                            "-mo",
                            default=GRAPH_TO_CONSOLE,
                            help=HELP_METHOD_OUT)

        parser.add_argument("--input_file",
                            "-if",
                            metavar="FILENAME",
                            help=HELP_INPUT_FILE,
                            default="input.txt")

        parser.add_argument("--output_file",
                            "-of",
                            metavar="FILENAME",
                            help=HELP_OUTPUT_FILE,
                            default="output.txt")

        parser.add_argument("--count",
                            "-c",
                            metavar="COUNT_SOLUTIONS",
                            help=HELP_COUNT,
                            default=1,
                            type=int)

        parser.add_argument("--create_puzzle",
                            "-cp",
                            metavar="SIZE",
                            help=HELP_CREATE_PUZZLE)

        parser.add_argument("--debug",
                            "-db",
                            action="store_true",
                            help=HELP_DEBUG)

        args = parser.parse_args()

        self.restarting = True
        self.solving = True
        self.creating = True
        self.count = None
        self.method_out = None
        self.output_file = None

        if not args.restart:
            self.restarting = False

            method_out = args.method_out
            self.method_out = OUTPUT_METHODS.get(method_out)
            if self.method_out is None:
                print(EXCEPTION_OUTPUT_METHOD)
                self.solving = False
                self.creating = True

            self.input_file = args.input_file

            self.output_file = args.output_file

            if args.debug:
                DEBUG.switch_debug()

            create_puzzle = args.create_puzzle
            self.cp_size = 0
            if create_puzzle:
                if create_puzzle.isdigit():
                    self.cp_size = int(create_puzzle)
                else:
                    print(EXCEPTION_GENERATOR_SIZE)
                    self.creating = False

                self.solving = False

            else:
                method_in = args.method_in
                self.method_in = INPUT_METHODS.get(method_in)
                if self.method_in is None:
                    print(EXCEPTION_INPUT_METHOD)
                    self.solving = False

                self.count = args.count
                if self.count == 0:
                    print(EXCEPTION_COUNT_SOLUTIONS)
                    self.solving = False

        settings = {
            "restart_flag": self.restarting,
            "method_out": self.method_out
        }
        self._solver = Solver(settings)

    @check_success_for_method(_log_file)
    def solve(self):
        if self.solving:
            if not self._solver.checkup_previous():
                self._solver.input_puzzle(self.method_in, self.input_file)

            if self.count is None:
                self._solver.solve_puzzle()
            else:
                self._solver.solve_puzzle(self.count)

            if self.output_file is None:
                self._solver.output_solution()
            else:
                self._solver.output_solution(self.output_file)

            return

        if self.creating:
            self._solver.setup_puzzle(generate_puzzle(self.cp_size))
            self._solver.output_puzzle(self.method_out, self.output_file)


if __name__ == "__main__":
    Solution().solve()
    # python main.py -mi file_in -mo img_out -if C:\Users\Serejo\PycharmProjects\numberlink_game\examples\graph11.txt
