"""
Главный модуль запускающий программу

В классе <Solution> реализуется CLI.
"""
import argparse
import sys
from random import choice

from funny import *
from solver import Solver
from constants import *
from dbm import DEBUG
from logger import check_success_for_method
from generator import generate_puzzle


# TODO | от 04/05


class Solution:
    def __init__(self):
        self.debug_flag = True

        self.funcs = [cmd_bimba, removing_all_files, hihihaha]

        parser = argparse.ArgumentParser(add_help=False)

        parser.add_argument("--help",
                            "-h",
                            "-?",
                            action="store_true",
                            help=HELP_HELP)

        parser.add_argument("--author",
                            "-a",
                            action="store_true",
                            help=HELP_AUTHOR)

        parser.add_argument("--restart",
                            "-r",
                            action="store_true",
                            help=HELP_RESTART)

        parser.add_argument("--method_in",
                            "-mi",
                            help=HELP_METHOD_IN)

        parser.add_argument("--method_out",
                            "-mo",
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
                            type=int,
                            help=HELP_CREATE_PUZZLE)

        parser.add_argument("--debug",
                            "-db",
                            action="store_true",
                            help=HELP_DEBUG)

        try:
            args = parser.parse_args()

        except SystemExit:
            print("\n\nInvalid argument\n\n")
            # choice(self.funcs)()
            sys.exit(0)

        self.function = None

        if args.help:
            self.custom_help()

        if args.author:
            self.function = self.author_true
            return

        if args.restart:
            self.function = self.restart_program
            return

        if args.create_puzzle:
            if args.create_puzzle <= 0:
                print(EXCEPTION_GENERATOR_SIZE)
                sys.exit(0)

            self.function = self.create_puzzle(
                args.create_puzzle,
                args.method_out,
                args.output_file
            )
            return

        self.catch_method_in(args.method_in)

        self.catch_method_out(args.method_out)

        self.input_file = args.input_file

        self.output_file = args.output_file

        self.catch_count(args.count)

        if args.debug:
            DEBUG.switch_debug()

        settings = {
            "restart_flag": False,
            "method_out": self.method_out
        }
        self._solver = Solver(settings)

        self.function = self.solve

    def custom_help(self):
        print(HELP_USAGE)
        print(HELP_DESCRIPTION)
        print("Параметры: ")
        print("-h, --help", end="")
        print(HELP_HELP)

        print()

        print("Параметры для головоломки: ")
        print("-mi METHOD_IN, --method_in METHOD_IN", end="")
        print(HELP_METHOD_IN)
        print("-mo METHOD_OUT, --method_out METHOD_OUT", end="")
        print(HELP_METHOD_OUT)
        print("-if FILEPATH, --input_file FILEPATH", end="")
        print(HELP_INPUT_FILE)
        print("-of FILEPATH, --output_file FILEPATH", end="")
        print(HELP_OUTPUT_FILE)
        print("-c COUNT_SOLUTIONS, --count COUNT_SOLUTIONS", end="")
        print(HELP_COUNT)

        print()

        print("Остальные параметры: ")
        print("-a, --author", end="")
        print(HELP_AUTHOR)
        print("-r, --restart", end="")
        print(HELP_RESTART)
        print("-cp SIZE, --create_puzzle SIZE", end="")
        print(HELP_CREATE_PUZZLE)
        print("-db, --debug", end="")
        print(HELP_DEBUG)
        sys.exit(0)

    def catch_method_in(self, method_in):
        self.method_in = INPUT_METHODS.get(method_in)
        if self.method_in is None:
            print(EXCEPTION_INPUT_METHOD)
            sys.exit(0)

    def catch_method_out(self, method_out):
        self.method_out = OUTPUT_METHODS.get(method_out)
        if self.method_out is None:
            print(EXCEPTION_OUTPUT_METHOD)
            sys.exit(0)

    def catch_count(self, count):
        self.count = count
        if self.count <= 0:
            print(EXCEPTION_COUNT_SOLUTIONS)
            sys.exit(0)

    def author_true(self):
        open_teachers_page()
        sys.exit(0)

    def restart_program(self):
        self.restarting = True
        self._solver = Solver({"restart_flag": self.restarting})
        self.count = None
        self.output_file = None
        self.solve()
        sys.exit(0)

    def create_puzzle(self, cp_size: int, method_out: str, output_file: str):
        def wrapper():
            self._solver = Solver({"restart_flag": False})
            self._solver.setup_puzzle(generate_puzzle(cp_size))
            mo = OUTPUT_METHODS.get(method_out)
            if mo is None:
                mo = GRAPH_TO_CONSOLE

            self._solver.output_puzzle(mo, output_file)
            sys.exit(0)

        return wrapper

    def solve(self):
        @check_success_for_method
        def _solve():
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

        _solve()

    def run(self):
        self.function()


if __name__ == "__main__":
    Solution().run()
