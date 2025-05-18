import unittest
from unittest.mock import patch

from constants import GRAPH_FROM_FILE, GRAPH_TO_IMG
from main import Solution


class TestSolution(unittest.TestCase):
    @patch("sys.argv", ["main.py", "-h"])
    def test_help(self):
        with self.assertRaises(SystemExit):
            Solution()

    @patch("sys.argv", ["main.py", "-a"])
    def test_link_to_teacher(self):
        test_solution = Solution()
        self.assertEqual(test_solution.author_true, test_solution.function)

    @patch("sys.argv", ["main.py", "-r"])
    def test_restart(self):
        test_solution = Solution()
        self.assertEqual(test_solution.restart_program, test_solution.function)

    @patch("sys.argv", ["main.py", "-mi", "file_in", "-mo", "img_out"])
    def test_method_in_out(self):
        test_solution = Solution()
        self.assertEqual(GRAPH_FROM_FILE, test_solution.method_in)
        self.assertEqual(GRAPH_TO_IMG, test_solution.method_out)

    @patch("sys.argv",
           ["main.py", "-mi", "file_in", "-mo", "img_out", "-c", "23"])
    def test_count(self):
        test_solution = Solution()
        self.assertEqual(GRAPH_FROM_FILE, test_solution.method_in)
        self.assertEqual(GRAPH_TO_IMG, test_solution.method_out)
        self.assertEqual(23, test_solution.count)

    @patch("sys.argv",
           ["main.py", "-mi", "file_in", "-mo", "img_out", "-c", "0"])
    def test_count_error(self):
        with self.assertRaises(SystemExit):
            Solution()

    @patch("sys.argv",
           ["main.py", "-cp", "4", "-mo", "img_out"])
    def test_create_puzzle(self):
        test_solution = Solution()
        self.assertEqual(
            test_solution.create_puzzle(4, GRAPH_TO_IMG, "a.txt").__name__,
            test_solution.function.__name__
        )
