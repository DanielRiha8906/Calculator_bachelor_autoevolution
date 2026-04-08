import math
import pytest
from src.__main__ import run_calculator, run_cli


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


# ---------------------------------------------------------------------------
# CLI (bash) mode tests
# ---------------------------------------------------------------------------

# --- Binary operations ---

def test_cli_add():
    outputs = []
    run_cli(["add", "5", "3"], print_fn=outputs.append)
    assert outputs == ["Result: 8.0"]


def test_cli_subtract():
    outputs = []
    run_cli(["subtract", "10", "3"], print_fn=outputs.append)
    assert outputs == ["Result: 7.0"]


def test_cli_multiply():
    outputs = []
    run_cli(["multiply", "4", "5"], print_fn=outputs.append)
    assert outputs == ["Result: 20.0"]


def test_cli_divide():
    outputs = []
    run_cli(["divide", "10", "4"], print_fn=outputs.append)
    assert outputs == ["Result: 2.5"]


def test_cli_power():
    outputs = []
    run_cli(["power", "2", "8"], print_fn=outputs.append)
    assert outputs == ["Result: 256.0"]


# --- Unary operations ---

def test_cli_factorial():
    outputs = []
    run_cli(["factorial", "5"], print_fn=outputs.append)
    assert outputs == ["Result: 120"]


def test_cli_factorial_float_whole_number():
    outputs = []
    run_cli(["factorial", "5.0"], print_fn=outputs.append)
    assert outputs == ["Result: 120"]


def test_cli_square():
    outputs = []
    run_cli(["square", "4"], print_fn=outputs.append)
    assert outputs == ["Result: 16.0"]


def test_cli_cube():
    outputs = []
    run_cli(["cube", "3"], print_fn=outputs.append)
    assert outputs == ["Result: 27.0"]


def test_cli_sqrt():
    outputs = []
    run_cli(["sqrt", "9"], print_fn=outputs.append)
    assert outputs == ["Result: 3.0"]


def test_cli_cbrt():
    # math.cbrt(27) may return 3.0000000000000004 due to float precision
    outputs = []
    run_cli(["cbrt", "27"], print_fn=outputs.append)
    assert len(outputs) == 1
    assert math.isclose(float(outputs[0].split(": ")[1]), 3.0, rel_tol=1e-9)


def test_cli_log():
    outputs = []
    run_cli(["log", "100"], print_fn=outputs.append)
    assert outputs == ["Result: 2.0"]


def test_cli_ln():
    outputs = []
    run_cli(["ln", "1"], print_fn=outputs.append)
    assert outputs == ["Result: 0.0"]


# --- Error cases ---

def test_cli_divide_by_zero_exits_with_error():
    outputs = []
    with pytest.raises(SystemExit) as exc_info:
        run_cli(["divide", "5", "0"], print_fn=outputs.append)
    assert exc_info.value.code == 1
    assert any("Error" in line for line in outputs)


def test_cli_sqrt_negative_exits_with_error():
    outputs = []
    with pytest.raises(SystemExit) as exc_info:
        run_cli(["sqrt", "-4"], print_fn=outputs.append)
    assert exc_info.value.code == 1
    assert any("Error" in line for line in outputs)


def test_cli_factorial_fractional_exits_with_error():
    outputs = []
    with pytest.raises(SystemExit) as exc_info:
        run_cli(["factorial", "5.5"], print_fn=outputs.append)
    assert exc_info.value.code == 1
    assert any("Error" in line for line in outputs)


def test_cli_log_nonpositive_exits_with_error():
    outputs = []
    with pytest.raises(SystemExit) as exc_info:
        run_cli(["log", "0"], print_fn=outputs.append)
    assert exc_info.value.code == 1
    assert any("Error" in line for line in outputs)


# --- Argument count errors ---

def test_cli_binary_op_with_one_value_exits():
    with pytest.raises(SystemExit) as exc_info:
        run_cli(["add", "5"])
    assert exc_info.value.code == 2


def test_cli_unary_op_with_two_values_exits():
    with pytest.raises(SystemExit) as exc_info:
        run_cli(["sqrt", "9", "4"])
    assert exc_info.value.code == 2


def test_cli_unknown_operation_exits():
    with pytest.raises(SystemExit) as exc_info:
        run_cli(["unknown_op", "5"])
    assert exc_info.value.code == 2
