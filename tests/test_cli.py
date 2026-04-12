"""Tests for the command-line interface in main.py."""
import pytest

from main import main


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run_cli(args, capsys):
    """Call main() with the given arg list and return (exit_code, stdout, stderr)."""
    code = main(args)
    captured = capsys.readouterr()
    return code, captured.out.strip(), captured.err.strip()


# ---------------------------------------------------------------------------
# Argument validation
# ---------------------------------------------------------------------------

def test_no_args_exits_1_and_prints_usage(capsys):
    code, out, err = run_cli([], capsys)
    assert code == 1
    assert "Usage" in err


def test_unknown_operation_exits_1(capsys):
    code, out, err = run_cli(["unknown_op", "5"], capsys)
    assert code == 1
    assert "unknown operation" in err


def test_binary_op_with_one_arg_exits_1(capsys):
    code, out, err = run_cli(["add", "5"], capsys)
    assert code == 1
    assert "two operands" in err


def test_binary_op_with_three_args_exits_1(capsys):
    code, out, err = run_cli(["add", "1", "2", "3"], capsys)
    assert code == 1
    assert "two operands" in err


def test_unary_op_with_zero_args_exits_1(capsys):
    code, out, err = run_cli(["factorial"], capsys)
    assert code == 1
    assert "one operand" in err


def test_unary_op_with_two_args_exits_1(capsys):
    code, out, err = run_cli(["square", "4", "9"], capsys)
    assert code == 1
    assert "one operand" in err


# ---------------------------------------------------------------------------
# Binary operations
# ---------------------------------------------------------------------------

def test_add_integers(capsys):
    code, out, err = run_cli(["add", "5", "7"], capsys)
    assert code == 0
    assert out == "12"


def test_add_floats(capsys):
    code, out, err = run_cli(["add", "1.5", "2.5"], capsys)
    assert code == 0
    assert float(out) == pytest.approx(4.0)


def test_subtract(capsys):
    code, out, err = run_cli(["subtract", "10", "4"], capsys)
    assert code == 0
    assert out == "6"


def test_multiply(capsys):
    code, out, err = run_cli(["multiply", "6", "7"], capsys)
    assert code == 0
    assert out == "42"


def test_divide(capsys):
    code, out, err = run_cli(["divide", "10", "2"], capsys)
    assert code == 0
    assert float(out) == pytest.approx(5.0)


def test_power(capsys):
    code, out, err = run_cli(["power", "2", "10"], capsys)
    assert code == 0
    assert out == "1024"


def test_divide_by_zero_exits_1(capsys):
    code, out, err = run_cli(["divide", "5", "0"], capsys)
    assert code == 1
    assert "Error" in err


# ---------------------------------------------------------------------------
# Unary operations
# ---------------------------------------------------------------------------

def test_factorial(capsys):
    code, out, err = run_cli(["factorial", "5"], capsys)
    assert code == 0
    assert out == "120"


def test_factorial_zero(capsys):
    code, out, err = run_cli(["factorial", "0"], capsys)
    assert code == 0
    assert out == "1"


def test_factorial_float_arg_exits_1(capsys):
    code, out, err = run_cli(["factorial", "3.5"], capsys)
    assert code == 1
    assert "Error" in err


def test_factorial_negative_exits_1(capsys):
    code, out, err = run_cli(["factorial", "-1"], capsys)
    assert code == 1
    assert "Error" in err


def test_square(capsys):
    code, out, err = run_cli(["square", "4"], capsys)
    assert code == 0
    assert out == "16"


def test_cube(capsys):
    code, out, err = run_cli(["cube", "3"], capsys)
    assert code == 0
    assert out == "27"


def test_square_root(capsys):
    code, out, err = run_cli(["square_root", "9"], capsys)
    assert code == 0
    assert float(out) == pytest.approx(3.0)


def test_square_root_negative_exits_1(capsys):
    code, out, err = run_cli(["square_root", "-1"], capsys)
    assert code == 1
    assert "Error" in err


def test_cube_root(capsys):
    code, out, err = run_cli(["cube_root", "27"], capsys)
    assert code == 0
    assert float(out) == pytest.approx(3.0)


def test_cube_root_negative(capsys):
    code, out, err = run_cli(["cube_root", "-8"], capsys)
    assert code == 0
    assert float(out) == pytest.approx(-2.0)


def test_log(capsys):
    code, out, err = run_cli(["log", "100"], capsys)
    assert code == 0
    assert float(out) == pytest.approx(2.0)


def test_log_non_positive_exits_1(capsys):
    code, out, err = run_cli(["log", "0"], capsys)
    assert code == 1
    assert "Error" in err


def test_ln(capsys):
    code, out, err = run_cli(["ln", "1"], capsys)
    assert code == 0
    assert float(out) == pytest.approx(0.0)


def test_ln_negative_exits_1(capsys):
    code, out, err = run_cli(["ln", "-5"], capsys)
    assert code == 1
    assert "Error" in err


# ---------------------------------------------------------------------------
# Non-numeric operand
# ---------------------------------------------------------------------------

def test_non_numeric_operand_exits_1(capsys):
    code, out, err = run_cli(["add", "five", "7"], capsys)
    assert code == 1
    assert "Error" in err
