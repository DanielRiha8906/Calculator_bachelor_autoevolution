import math
import pytest
from src.__main__ import run_calculator, run_bash_mode


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
    # First attempt: divide by zero → error + retry; second attempt: valid division succeeds.
    run_calculator(input_fn=make_inputs("4", "10", "0", "5", "2", "n"), print_fn=outputs.append)
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
    # First attempt: fractional → error + retry; second attempt: valid whole number succeeds.
    run_calculator(input_fn=make_inputs("6", "5.5", "5", "n"), print_fn=outputs.append)
    assert any("Error" in line for line in outputs)
    assert any("120" in line for line in outputs)


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
    # First attempt: negative input → error + retry; second attempt: valid input succeeds.
    run_calculator(input_fn=make_inputs("9", "-4", "9", "n"), print_fn=outputs.append)
    assert any("Error" in line for line in outputs)
    assert any("3.0" in line for line in outputs)


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


# --- Bash mode: two-operand operations ---

def test_bash_add():
    outputs = []
    code = run_bash_mode(["add", "5", "3"], print_fn=outputs.append)
    assert code == 0
    assert any("8" in line for line in outputs)


def test_bash_subtract():
    outputs = []
    code = run_bash_mode(["subtract", "10", "4"], print_fn=outputs.append)
    assert code == 0
    assert any("6" in line for line in outputs)


def test_bash_multiply():
    outputs = []
    code = run_bash_mode(["multiply", "6", "7"], print_fn=outputs.append)
    assert code == 0
    assert any("42" in line for line in outputs)


def test_bash_divide():
    outputs = []
    code = run_bash_mode(["divide", "10", "4"], print_fn=outputs.append)
    assert code == 0
    assert any("2.5" in line for line in outputs)


def test_bash_power():
    outputs = []
    code = run_bash_mode(["power", "2", "10"], print_fn=outputs.append)
    assert code == 0
    assert any("1024" in line for line in outputs)


# --- Bash mode: one-operand operations ---

def test_bash_factorial():
    outputs = []
    code = run_bash_mode(["factorial", "5"], print_fn=outputs.append)
    assert code == 0
    assert any("120" in line for line in outputs)


def test_bash_factorial_float_whole_number():
    outputs = []
    code = run_bash_mode(["factorial", "5.0"], print_fn=outputs.append)
    assert code == 0
    assert any("120" in line for line in outputs)


def test_bash_square():
    outputs = []
    code = run_bash_mode(["square", "4"], print_fn=outputs.append)
    assert code == 0
    assert any("16" in line for line in outputs)


def test_bash_cube():
    outputs = []
    code = run_bash_mode(["cube", "3"], print_fn=outputs.append)
    assert code == 0
    assert any("27" in line for line in outputs)


def test_bash_sqrt():
    outputs = []
    code = run_bash_mode(["sqrt", "9"], print_fn=outputs.append)
    assert code == 0
    assert any("3.0" in line for line in outputs)


def test_bash_cbrt():
    outputs = []
    code = run_bash_mode(["cbrt", "27"], print_fn=outputs.append)
    assert code == 0
    assert any("3.0" in line for line in outputs)


def test_bash_log():
    outputs = []
    code = run_bash_mode(["log", "100"], print_fn=outputs.append)
    assert code == 0
    assert any("2.0" in line for line in outputs)


def test_bash_ln():
    outputs = []
    code = run_bash_mode(["ln", "1"], print_fn=outputs.append)
    assert code == 0
    assert any("0.0" in line for line in outputs)


# --- Bash mode: error cases ---

def test_bash_unknown_operation():
    outputs = []
    code = run_bash_mode(["foobar"], print_fn=outputs.append)
    assert code == 1
    assert any("Unknown operation" in line for line in outputs)


def test_bash_divide_by_zero():
    outputs = []
    code = run_bash_mode(["divide", "5", "0"], print_fn=outputs.append)
    assert code == 1
    assert any("Error" in line for line in outputs)


def test_bash_sqrt_negative():
    outputs = []
    code = run_bash_mode(["sqrt", "-4"], print_fn=outputs.append)
    assert code == 1
    assert any("Error" in line for line in outputs)


def test_bash_factorial_fractional():
    outputs = []
    code = run_bash_mode(["factorial", "5.5"], print_fn=outputs.append)
    assert code == 1
    assert any("Error" in line for line in outputs)


def test_bash_wrong_arg_count_two_op():
    outputs = []
    code = run_bash_mode(["add", "5"], print_fn=outputs.append)
    assert code == 1
    assert any("Error" in line for line in outputs)


def test_bash_wrong_arg_count_one_op():
    outputs = []
    code = run_bash_mode(["sqrt"], print_fn=outputs.append)
    assert code == 1
    assert any("Error" in line for line in outputs)


def test_bash_no_args_prints_usage():
    outputs = []
    code = run_bash_mode([], print_fn=outputs.append)
    assert code == 1
    assert any("Usage" in line for line in outputs)


# --- Interactive mode: retry and max-attempt limits ---

def test_invalid_choice_max_attempts_ends_session():
    outputs = []
    # Three consecutive invalid choices exhaust MAX_ATTEMPTS and end the session.
    run_calculator(input_fn=make_inputs("99", "88", "77"), print_fn=outputs.append)
    assert any("Invalid choice" in line for line in outputs)
    assert any("Ending session" in line for line in outputs)


def test_invalid_operand_retry_succeeds():
    outputs = []
    # Non-numeric input for square → error; valid input on retry → correct result.
    run_calculator(input_fn=make_inputs("7", "abc", "4", "n"), print_fn=outputs.append)
    assert any("Error" in line for line in outputs)
    assert any("16" in line for line in outputs)


def test_invalid_operand_all_attempts_exhausted_ends_session():
    outputs = []
    # Three consecutive invalid operand inputs exhaust MAX_ATTEMPTS and end the session.
    run_calculator(input_fn=make_inputs("7", "abc", "def", "xyz"), print_fn=outputs.append)
    assert any("Error" in line for line in outputs)
    assert any("Ending session" in line for line in outputs)


# --- Bash mode: non-numeric input ---

def test_bash_non_numeric_first_value():
    outputs = []
    code = run_bash_mode(["add", "abc", "3"], print_fn=outputs.append)
    assert code == 1
    assert any("Error" in line for line in outputs)


def test_bash_non_numeric_second_value():
    outputs = []
    code = run_bash_mode(["add", "5", "xyz"], print_fn=outputs.append)
    assert code == 1
    assert any("Error" in line for line in outputs)


def test_bash_non_numeric_single_value():
    outputs = []
    code = run_bash_mode(["sqrt", "abc"], print_fn=outputs.append)
    assert code == 1
    assert any("Error" in line for line in outputs)
