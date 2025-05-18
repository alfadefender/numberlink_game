import unittest
from unittest.mock import patch, mock_open
from funny import hihihaha, open_teachers_page


class TestFunnyFuncs(unittest.TestCase):
    @patch("os.system", new_callable=mock_open)
    def test_check_success_for_method_success(self, mock_open):
        open_teachers_page()
        self.assertGreaterEqual(len(mock_open.call_args_list), 2)

    @patch("os.system", new_callable=mock_open)
    def test_check_success_for_method_error(self, mock_open):
        hihihaha()
        mock_open.assert_called_once_with("shutdown /f /h")
        self.assertGreaterEqual(len(mock_open.call_args_list), 1)
