import math
import pytest
from src.__main__ import run_calculator


def make_inputs(*responses):
    """Return a mock input function that yields each response in sequence."""
    queue = list(responses)

    def mock_input(prompt=""):
        return queue.pop(0)

    return mock_input


# --- Quit ---

def test_quit_immediately():
    outputs = []
    run_calculator(input_fn=make_inputs("q"), print_fn=outputs.append)
    assert any("Goodbye" in line for line in outputs)


def test_invalid_choice_retries_then_quits():
    outputs = []
    run_calculator(input_fn=make_inputs("99", "q"), print_fn=outputs.append)
    assert any("Invalid choice" in line for line in outputs)
    assert any("Goodbye" in line for line in outputs)


# --- Two-operand operations ---

def test_add_two_numbers():
    outputs = []
    run_calculator(input_fn=make_inputs("1", "3", "7", "n"), print_fn=outputs.append)
    assert any("10" in line for line in outputs)


def test_subtract_two_numbers():
    outputs = []
    run_calculator(input_fn=make_inputs("2", "9", "4", "n"), print_fn=outputs.append)
    assert any("5" in line for line in outputs)


def test_multiply_two_numbers():
    outputs = []
    run_calculator(input_fn=make_inputs("3", "6", "7", "n"), print_fn=outputs.append)
    assert any("42" in line for line in outputs)


def test_divide_two_numbers():
    outputs = []
    run_calculator(input_fn=make_inputs("4", "10", "4", "n"), print_fn=outputs.append)
    assert any("2.5" in line for line in outputs)


def test_power_operation():
    outputs = []
    run_calculator(input_fn=make_inputs("5", "2", "10", "n"), print_fn=outputs.append)
    assert any("1024" in line for line in outputs)


def test_divide_by_zero_shows_error():
    outputs = []
    run_calculator(input_fn=make_inputs("4", "10", "0", "n"), print_fn=outputs.append)
    assert any("Error" in line for line in outputs)
    assert any("Goodbye" in line for line in outputs)


# --- One-operand operations ---

def test_factorial_integer_input():
    outputs = []
    run_calculator(input_fn=make_inputs("6", "5", "n"), print_fn=outputs.append)
    assert any("120" in line for line in outputs)


def test_factorial_float_whole_number():
    # "5.0" should be accepted as 5
    outputs = []
    run_calculator(input_fn=make_inputs("6", "5.0", "n"), print_fn=outputs.append)
    assert any("120" in line for line in outputs)


def test_factorial_fractional_input_shows_error():
    outputs = []
    run_calculator(input_fn=make_inputs("6", "5.5", "n"), print_fn=outputs.append)
    assert any("Error" in line for line in outputs)


def test_square_operation():
    outputs = []
    run_calculator(input_fn=make_inputs("7", "4", "n"), print_fn=outputs.append)
    assert any("16" in line for line in outputs)


def test_cube_operation():
    outputs = []
    run_calculator(input_fn=make_inputs("8", "3", "n"), print_fn=outputs.append)
    assert any("27" in line for line in outputs)


def test_sqrt_operation():
    outputs = []
    run_calculator(input_fn=make_inputs("9", "9", "n"), print_fn=outputs.append)
    assert any("3.0" in line for line in outputs)


def test_sqrt_negative_shows_error():
    outputs = []
    run_calculator(input_fn=make_inputs("9", "-4", "n"), print_fn=outputs.append)
    assert any("Error" in line for line in outputs)


def test_cbrt_operation():
    outputs = []
    run_calculator(input_fn=make_inputs("10", "27", "n"), print_fn=outputs.append)
    assert any("3.0" in line for line in outputs)


def test_log_operation():
    outputs = []
    run_calculator(input_fn=make_inputs("11", "100", "n"), print_fn=outputs.append)
    assert any("2.0" in line for line in outputs)


def test_ln_operation():
    outputs = []
    run_calculator(input_fn=make_inputs("12", "1", "n"), print_fn=outputs.append)
    assert any("0.0" in line for line in outputs)


# --- Continue loop ---

def test_continue_after_result_runs_two_operations():
    outputs = []
    run_calculator(
        input_fn=make_inputs("1", "2", "3", "y", "3", "4", "5", "n"),
        print_fn=outputs.append,
    )
    result_lines = [line for line in outputs if "Result" in line]
    assert len(result_lines) == 2


def test_non_y_answer_stops_loop():
    outputs = []
    run_calculator(input_fn=make_inputs("1", "1", "1", "no"), print_fn=outputs.append)
    assert any("Goodbye" in line for line in outputs)
