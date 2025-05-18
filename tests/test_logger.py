import unittest
from unittest.mock import patch, mock_open
from logger import _format_time, check_success_for_method, measure_time_console
from constants import LOG_FILENAME


class TestFormatTime(unittest.TestCase):
    def test_format_only_milliseconds(self):
        self.assertEqual(_format_time(0.123), "123 ms")

    def test_format_seconds_and_milliseconds(self):
        self.assertEqual(_format_time(5.456), "5 sec, 456 ms")

    def test_format_minutes_seconds_milliseconds(self):
        self.assertEqual(_format_time(125.789), "2 min, 5 sec, 789 ms")

    def test_format_hours_minutes_seconds_milliseconds(self):
        self.assertEqual(_format_time(3665.012), "1 h, 1 min, 5 sec, 12 ms")

    def test_format_over_24h(self):
        self.assertTrue(_format_time(90000).startswith("..., "))


class TestDecorators(unittest.TestCase):
    def test_measure_time_console(self):
        @measure_time_console
        def test_func():
            return "ok"

        with patch("builtins.print") as mock_print:
            result = test_func()
            self.assertEqual(result, "ok")
            mock_print.assert_any_call(
                unittest.mock.ANY
            )

    @patch("builtins.open", new_callable=mock_open)
    def test_check_success_for_method_success(self, mock_file):
        @check_success_for_method
        def test_func():
            return 42

        result = test_func()
        self.assertEqual(result, 42)

        mock_file.assert_called_once_with(LOG_FILENAME, "w")

        write_calls = mock_file().write.call_args_list
        all_calls = "".join(call_args[0][0] for call_args in write_calls)
        self.assertIn("INFO - Puzzle is solved successfully", all_calls)

    @patch("builtins.open", new_callable=mock_open)
    def test_check_success_for_method_error(self, mock_file):
        @check_success_for_method
        def test_func():
            raise ValueError("Test error")

        result = test_func()
        self.assertIsNone(result)
        mock_file.assert_called_once_with(LOG_FILENAME, "w")

        write_calls = mock_file().write.call_args_list
        all_calls = "".join(call_args[0][0] for call_args in write_calls)
        self.assertIn("ERROR - !!! Caught exception !!!", all_calls)
