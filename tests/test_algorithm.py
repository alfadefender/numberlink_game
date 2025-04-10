import unittest
from unittest.mock import patch, MagicMock
from puzzle import Puzzle
from algorithm import the_least_distance_method


class TestTheLeastDistanceMethod(unittest.TestCase):
    @patch('time.time', return_value=1625065000)  # Закрепляем время
    def test_the_least_distance_method_empty_puzzle(self, mock_time):
        mock_puzzle = MagicMock(spec=Puzzle)
        mock_puzzle.is_empty.return_value = True

        the_least_distance_method(mock_puzzle)

        # Проверяем, что set_is_solved не был вызван, так как головоломка пуста
        mock_puzzle.set_is_solved.assert_not_called()

        # Проверяем, что set_result и set_paths также не были вызваны
        mock_puzzle.set_result.assert_not_called()
        mock_puzzle.set_paths.assert_not_called()

    @patch('time.time', return_value=1625065000)  # Закрепляем время
    @patch('builtins.open', new_callable=MagicMock)  # Для Logger'a
    def test_the_least_distance_method_success(self, mock_open, mock_time):
        mock_puzzle = MagicMock(spec=Puzzle)
        mock_puzzle.is_empty.return_value = False
        mock_puzzle.get_graph.return_value = [[0, 1], [1, 0]]
        mock_puzzle.get_size.return_value = 2
        mock_puzzle.get_count_points.return_value = 1

        the_least_distance_method(mock_puzzle, count_results=1)

        # Проверяем, что метод set_is_solved был вызван
        mock_puzzle.set_is_solved.assert_called_once()

        # Проверяем, что результат не пустой
        mock_puzzle.set_result.assert_called_once()
        mock_puzzle.set_paths.assert_called_once()

    @patch('time.time', return_value=1625065000)  # Закрепляем время
    @patch('builtins.open', new_callable=MagicMock)  # Для Logger'a
    def test_the_least_distance_method_multiple_results(self, mock_open, mock_time):
        mock_puzzle = MagicMock(spec=Puzzle)
        mock_puzzle.is_empty.return_value = False
        mock_puzzle.get_graph.return_value = [[0, 1], [1, 0]]
        mock_puzzle.get_size.return_value = 2
        mock_puzzle.get_count_points.return_value = 1

        the_least_distance_method(mock_puzzle, count_results=2)

        # Проверяем, что метод set_is_solved был вызван
        mock_puzzle.set_is_solved.assert_called_once()

        # Проверяем, что результат не пустой
        mock_puzzle.set_result.assert_called_once()
        mock_puzzle.set_paths.assert_called_once()