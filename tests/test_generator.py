import unittest
from algorithm import the_least_distance_method
from generator import _get_empty_cell, _get_next_points, generate_puzzle


class TestGenerator(unittest.TestCase):

    def test_get_empty_cell_empty_zeros(self):
        with self.assertRaises(IndexError):
            n = 2
            graph = [[1, 2], [2, 1]]
            _get_empty_cell(n, graph)

    def test_get_empty_cell_with_zeros(self):
        n = 2
        graph = [[1, 4], [2, 0]]
        result = _get_empty_cell(n, graph)
        self.assertEqual(result, (1, 1))

    def test_get_next_points_two_points(self):
        n = 2
        cur_point = (0, 0)
        result = _get_next_points(n, cur_point)
        self.assertListEqual([(1, 0), (0, 1)], result)

    def test_get_next_points_three_points(self):
        n = 3
        cur_point = (0, 1)
        result = _get_next_points(n, cur_point)
        self.assertListEqual([(0, 0), (1, 1), (0, 2)], result)

    def test_get_next_points_four_points(self):
        n = 3
        cur_point = (1, 1)
        result = _get_next_points(n, cur_point)
        self.assertListEqual([(0, 1), (1, 0), (2, 1), (1, 2)], result)

    def test_generate_puzzle(self):
        # TODO INDEX ERROR FUCKED UP
        n = 5
        puzzle = generate_puzzle(n)
        the_least_distance_method(puzzle)
        self.assertTrue(puzzle.is_solved())
        self.assertEqual(len(puzzle._results), 1)
