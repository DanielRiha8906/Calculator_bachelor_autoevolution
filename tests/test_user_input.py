import pytest
from unittest.mock import patch
from src.user_input import interactive_mode


class TestInteractiveMode:
    def test_quit_immediately(self, capsys):
        with patch("builtins.input", return_value="q"):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Goodbye!" in captured.out

    def test_menu_is_printed(self, capsys):
        with patch("builtins.input", return_value="q"):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Calculator - Interactive Mode" in captured.out
        assert "Operations:" in captured.out

    def test_add_two_numbers(self, capsys):
        inputs = iter(["1", "3", "5", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Result: 8.0" in captured.out

    def test_subtract_two_numbers(self, capsys):
        inputs = iter(["2", "10", "3", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Result: 7.0" in captured.out

    def test_multiply_two_numbers(self, capsys):
        inputs = iter(["3", "4", "5", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Result: 20.0" in captured.out

    def test_divide_two_numbers(self, capsys):
        inputs = iter(["4", "10", "2", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Result: 5.0" in captured.out

    def test_factorial_integer(self, capsys):
        inputs = iter(["5", "5", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Result: 120" in captured.out

    def test_square_number(self, capsys):
        inputs = iter(["6", "4", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Result: 16.0" in captured.out

    def test_cube_number(self, capsys):
        inputs = iter(["7", "3", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Result: 27.0" in captured.out

    def test_square_root(self, capsys):
        inputs = iter(["8", "9", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Result: 3.0" in captured.out

    def test_power_operation(self, capsys):
        inputs = iter(["10", "2", "3", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Result: 8.0" in captured.out

    def test_invalid_choice_shows_error(self, capsys):
        inputs = iter(["99", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Unknown operation" in captured.out

    def test_divide_by_zero_shows_error(self, capsys):
        inputs = iter(["4", "10", "0", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Error:" in captured.out

    def test_square_root_negative_shows_error(self, capsys):
        inputs = iter(["8", "-1", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Error:" in captured.out

    def test_multiple_operations_in_session(self, capsys):
        inputs = iter(["1", "2", "3", "2", "10", "4", "q"])
        with patch("builtins.input", side_effect=inputs):
            interactive_mode()
        captured = capsys.readouterr()
        assert "Result: 5.0" in captured.out
        assert "Result: 6.0" in captured.out
