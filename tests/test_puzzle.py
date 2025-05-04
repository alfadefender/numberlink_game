import unittest
from puzzle import Puzzle


class TestGenerator(unittest.TestCase):
    def test_is_empty(self):
        puzzle = Puzzle(0, 0, [])
        self.assertTrue(puzzle.is_empty())
        puzzle = Puzzle(2, 1, [[1, 0], [0, 1]])
        self.assertFalse(puzzle.is_empty())

    def test_is_solved(self):
        puzzle = Puzzle(0, 0, [])
        self.assertFalse(puzzle.is_solved())
        puzzle.set_is_solved()
        self.assertTrue(puzzle.is_solved())

    def test_get_graph(self):
        puzzle = Puzzle(2, 0, [[0, 0], [0, 0]])
        self.assertListEqual([[0, 0], [0, 0]], puzzle.get_graph())

    def test_get_size(self):
        puzzle = Puzzle(0, 0, [])
        self.assertEqual(0, puzzle.get_size())

    def test_get_result(self):
        paths = [{}]
        results = [[]]
        puzzle = Puzzle(0, 0, [])
        puzzle.set_result(results)
        puzzle.set_paths(paths)

        self.assertEqual((([], {}),), tuple(puzzle.get_result()))
