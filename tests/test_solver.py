import unittest
from io import StringIO
from unittest.mock import patch, mock_open

from puzzle import Puzzle
from solver import Solver
from constants import GRAPH_FROM_CONSOLE, GRAPH_TO_CONSOLE, GRAPH_TO_FILE, \
    GRAPH_TO_IMG


class TestSolver(unittest.TestCase):
    @staticmethod
    def imitate_input():
        yield "2"
        yield "2"
        yield "1 2"
        yield "1 2"

    def test_setup_puzzle_checkup(self):
        solver = Solver({
            "restart_flag": False,
            "method_out": GRAPH_TO_CONSOLE
        })
        solver.setup_puzzle(Puzzle(2, 2, [[1, 2], [1, 2]]))
        self.assertIsNotNone(solver._puzzle)

    def test_checkup_previous_false(self):
        solver = Solver({
            "restart_flag": False,
            "method_out": GRAPH_TO_CONSOLE
        })
        self.assertFalse(solver.checkup_previous())

    def test_checkup_previous_another_false(self):
        solver = Solver({
            "restart_flag": True,
            "method_out": GRAPH_TO_CONSOLE
        })
        self.assertFalse(solver.checkup_previous())

    @patch("builtins.input", return_value=next(imitate_input()))
    @patch("builtins.open", new_callable=mock_open)
    def test_input_puzzle_console(self, mock_input, mock_open):
        solver = Solver({
            "restart_flag": False,
            "method_out": GRAPH_TO_CONSOLE
        })
        solver.input_puzzle(GRAPH_FROM_CONSOLE)
        self.assertIsNotNone(solver._puzzle)

    def test_is_solved(self):
        solver = Solver({
            "restart_flag": False,
            "method_out": GRAPH_TO_CONSOLE
        })
        solver.setup_puzzle(Puzzle(2, 2, [[1, 2], [1, 2]]))
        self.assertFalse(solver._puzzle.is_solved())
        solver.solve_puzzle()
        self.assertTrue(solver._puzzle.is_solved())

    @patch("sys.stdout", new_callable=StringIO)
    def test_output_solution_console(self, mock_stdout):
        solver = Solver({
            "restart_flag": False,
            "method_out": GRAPH_TO_CONSOLE
        })
        solver.setup_puzzle(Puzzle(2, 2, [[1, 2], [1, 2]]))
        solver.solve_puzzle()
        solver.output_solution()
        s = "".join((
            "   1|   2|\n",
            "   1|   2|\n",
            "_________________\n"
        ))
        temp = mock_stdout.getvalue()
        idx = temp.find("\n")
        self.assertEqual(s, temp[idx + 1:])

    @patch("builtins.open", new_callable=mock_open)
    def test_output_solution_file(self, mock_open):
        solver = Solver({
            "restart_flag": False,
            "method_out": GRAPH_TO_FILE
        })
        solver.setup_puzzle(Puzzle(2, 2, [[1, 2], [1, 2]]))
        solver.solve_puzzle()
        solver.output_solution()
        self.assertGreaterEqual(mock_open.call_count, 1)

    @patch("builtins.open", new_callable=mock_open)
    def test_output_solution_img(self, mock_open):
        solver = Solver({
            "restart_flag": False,
            "method_out": GRAPH_TO_IMG
        })
        solver.setup_puzzle(Puzzle(2, 2, [[1, 2], [1, 2]]))
        solver.solve_puzzle()
        solver.output_solution()
        self.assertGreaterEqual(mock_open.call_count, 1)

    @patch("builtins.open", new_callable=mock_open)
    def test_output_puzzle_file(self, mock_open):
        solver = Solver({
            "restart_flag": False,
            "method_out": GRAPH_TO_FILE
        })
        solver.setup_puzzle(Puzzle(2, 2, [[1, 2], [1, 2]]))
        solver.output_puzzle(GRAPH_TO_FILE)
        self.assertGreaterEqual(mock_open.call_count, 1)

    @patch("builtins.open", new_callable=mock_open)
    def test_output_puzzle_img(self, mock_open):
        solver = Solver({
            "restart_flag": False,
            "method_out": GRAPH_TO_IMG
        })
        solver.setup_puzzle(Puzzle(2, 2, [[1, 2], [1, 2]]))
        solver.output_puzzle(GRAPH_TO_IMG)
        self.assertGreaterEqual(mock_open.call_count, 1)
