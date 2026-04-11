"""Tests for CalculatorController — the dispatch layer between UIs and Calculator."""
import math
import pytest

from src.controller import CalculatorController, CHOICE_TO_OPERATION


@pytest.fixture
def controller():
    return CalculatorController()


# --- CHOICE_TO_OPERATION mapping ---

def test_choice_to_operation_covers_all_twelve():
    assert set(CHOICE_TO_OPERATION.keys()) == {str(i) for i in range(1, 13)}


def test_choice_to_operation_values_are_strings():
    for key, value in CHOICE_TO_OPERATION.items():
        assert isinstance(value, str), f"choice {key!r} maps to non-string {value!r}"


# --- CalculatorController.execute: all 12 operations ---

def test_execute_add(controller):
    assert controller.execute("add", a=3.0, b=4.0) == "7.0"


def test_execute_subtract(controller):
    assert controller.execute("subtract", a=10.0, b=3.0) == "7.0"


def test_execute_multiply(controller):
    assert controller.execute("multiply", a=3.0, b=4.0) == "12.0"


def test_execute_divide(controller):
    assert controller.execute("divide", a=10.0, b=2.0) == "5.0"


def test_execute_divide_by_zero_raises(controller):
    with pytest.raises(ZeroDivisionError):
        controller.execute("divide", a=10.0, b=0.0)


def test_execute_factorial(controller):
    assert controller.execute("factorial", a=5) == "120"


def test_execute_factorial_zero(controller):
    assert controller.execute("factorial", a=0) == "1"


def test_execute_factorial_negative_raises(controller):
    with pytest.raises(ValueError):
        controller.execute("factorial", a=-1)


def test_execute_square(controller):
    assert controller.execute("square", a=4.0) == "16.0"


def test_execute_cube(controller):
    assert controller.execute("cube", a=3.0) == "27.0"


def test_execute_square_root(controller):
    assert controller.execute("square_root", a=9.0) == "3.0"


def test_execute_square_root_negative_raises(controller):
    with pytest.raises(ValueError):
        controller.execute("square_root", a=-4.0)


def test_execute_cube_root(controller):
    result = float(controller.execute("cube_root", a=27.0))
    assert result == pytest.approx(3.0)


def test_execute_cube_root_negative(controller):
    result = float(controller.execute("cube_root", a=-8.0))
    assert result == pytest.approx(-2.0)


def test_execute_power(controller):
    assert controller.execute("power", a=2.0, b=10.0) == "1024.0"


def test_execute_log_default_base(controller):
    result = float(controller.execute("log", a=100.0))
    assert result == pytest.approx(2.0)


def test_execute_log_custom_base(controller):
    result = float(controller.execute("log", a=8.0, base=2.0))
    assert result == pytest.approx(3.0)


def test_execute_log_non_positive_raises(controller):
    with pytest.raises(ValueError):
        controller.execute("log", a=0.0)


def test_execute_ln(controller):
    result = float(controller.execute("ln", a=math.e))
    assert result == pytest.approx(1.0)


def test_execute_ln_non_positive_raises(controller):
    with pytest.raises(ValueError):
        controller.execute("ln", a=0.0)


# --- CalculatorController.execute: unknown operation ---

def test_execute_unknown_operation_raises(controller):
    with pytest.raises(ValueError, match="Unknown operation"):
        controller.execute("unknown_op")


def test_execute_empty_operation_raises(controller):
    with pytest.raises(ValueError, match="Unknown operation"):
        controller.execute("")


# --- Result is always a string ---

def test_execute_returns_string_for_add(controller):
    result = controller.execute("add", a=1.0, b=2.0)
    assert isinstance(result, str)


def test_execute_returns_string_for_factorial(controller):
    result = controller.execute("factorial", a=5)
    assert isinstance(result, str)
