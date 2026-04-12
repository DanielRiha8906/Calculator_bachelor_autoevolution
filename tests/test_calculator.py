import logging
import pytest
import math
from src.calculator import Calculator


# --- add ---

def test_add_positive_numbers():
    calc = Calculator()
    assert calc.add(2, 3) == 5


def test_add_negative_numbers():
    calc = Calculator()
    assert calc.add(-4, -6) == -10


def test_add_mixed_sign():
    calc = Calculator()
    assert calc.add(-3, 7) == 4


def test_add_zeros():
    calc = Calculator()
    assert calc.add(0, 0) == 0


def test_add_floats():
    calc = Calculator()
    assert calc.add(0.1, 0.2) == pytest.approx(0.3)


# --- subtract ---

def test_subtract_positive_numbers():
    calc = Calculator()
    assert calc.subtract(10, 4) == 6


def test_subtract_negative_numbers():
    calc = Calculator()
    assert calc.subtract(-3, -5) == 2


def test_subtract_mixed_sign():
    calc = Calculator()
    assert calc.subtract(5, -3) == 8


def test_subtract_same_values():
    calc = Calculator()
    assert calc.subtract(7, 7) == 0


def test_subtract_floats():
    calc = Calculator()
    assert calc.subtract(1.5, 0.5) == pytest.approx(1.0)


# --- multiply ---

def test_multiply_positive_numbers():
    calc = Calculator()
    assert calc.multiply(3, 4) == 12


def test_multiply_negative_numbers():
    calc = Calculator()
    assert calc.multiply(-3, -4) == 12


def test_multiply_mixed_sign():
    calc = Calculator()
    assert calc.multiply(3, -4) == -12


def test_multiply_by_zero():
    calc = Calculator()
    assert calc.multiply(99, 0) == 0


def test_multiply_by_one():
    calc = Calculator()
    assert calc.multiply(7, 1) == 7


def test_multiply_floats():
    calc = Calculator()
    assert calc.multiply(2.5, 4.0) == pytest.approx(10.0)


# --- divide ---

def test_divide_by_zero_raises():
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.divide(10, 0)


def test_divide_positive_numbers():
    calc = Calculator()
    assert calc.divide(10, 2) == 5.0


def test_divide_negative_numbers():
    calc = Calculator()
    assert calc.divide(-12, -4) == 3.0


def test_divide_mixed_sign():
    calc = Calculator()
    assert calc.divide(9, -3) == -3.0


def test_divide_by_one():
    calc = Calculator()
    assert calc.divide(42, 1) == 42.0


def test_divide_floats():
    calc = Calculator()
    assert calc.divide(7.5, 2.5) == pytest.approx(3.0)


def test_divide_results_in_fraction():
    calc = Calculator()
    assert calc.divide(1, 3) == pytest.approx(1 / 3)


# --- factorial ---

def test_factorial_zero():
    calc = Calculator()
    assert calc.factorial(0) == 1


def test_factorial_one():
    calc = Calculator()
    assert calc.factorial(1) == 1


def test_factorial_positive():
    calc = Calculator()
    assert calc.factorial(5) == 120


def test_factorial_large():
    calc = Calculator()
    assert calc.factorial(10) == 3628800


def test_factorial_negative_raises():
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.factorial(-1)


# --- square ---

def test_square_positive():
    calc = Calculator()
    assert calc.square(4) == 16


def test_square_negative():
    calc = Calculator()
    assert calc.square(-3) == 9


def test_square_zero():
    calc = Calculator()
    assert calc.square(0) == 0


def test_square_float():
    calc = Calculator()
    assert calc.square(2.5) == pytest.approx(6.25)


# --- cube ---

def test_cube_positive():
    calc = Calculator()
    assert calc.cube(3) == 27


def test_cube_negative():
    calc = Calculator()
    assert calc.cube(-2) == -8


def test_cube_zero():
    calc = Calculator()
    assert calc.cube(0) == 0


def test_cube_float():
    calc = Calculator()
    assert calc.cube(2.0) == pytest.approx(8.0)


# --- square_root ---

def test_square_root_positive():
    calc = Calculator()
    assert calc.square_root(9) == pytest.approx(3.0)


def test_square_root_float():
    calc = Calculator()
    assert calc.square_root(2.0) == pytest.approx(math.sqrt(2.0))


def test_square_root_zero():
    calc = Calculator()
    assert calc.square_root(0) == pytest.approx(0.0)


def test_square_root_negative_raises():
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.square_root(-1)


# --- cube_root ---

def test_cube_root_positive():
    calc = Calculator()
    assert calc.cube_root(27) == pytest.approx(3.0)


def test_cube_root_negative():
    calc = Calculator()
    assert calc.cube_root(-8) == pytest.approx(-2.0)


def test_cube_root_zero():
    calc = Calculator()
    assert calc.cube_root(0) == pytest.approx(0.0)


def test_cube_root_float():
    calc = Calculator()
    assert calc.cube_root(2.0) == pytest.approx(math.cbrt(2.0))


# --- power ---

def test_power_positive_exponent():
    calc = Calculator()
    assert calc.power(2, 10) == 1024


def test_power_zero_exponent():
    calc = Calculator()
    assert calc.power(99, 0) == 1


def test_power_negative_exponent():
    calc = Calculator()
    assert calc.power(2, -1) == pytest.approx(0.5)


def test_power_float_base():
    calc = Calculator()
    assert calc.power(2.5, 2) == pytest.approx(6.25)


# --- log (base 10) ---

def test_log_one():
    calc = Calculator()
    assert calc.log(1) == pytest.approx(0.0)


def test_log_ten():
    calc = Calculator()
    assert calc.log(10) == pytest.approx(1.0)


def test_log_hundred():
    calc = Calculator()
    assert calc.log(100) == pytest.approx(2.0)


def test_log_non_positive_raises():
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.log(0)


def test_log_negative_raises():
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.log(-5)


# --- ln (natural log) ---

def test_ln_one():
    calc = Calculator()
    assert calc.ln(1) == pytest.approx(0.0)


def test_ln_e():
    calc = Calculator()
    assert calc.ln(math.e) == pytest.approx(1.0)


def test_ln_float():
    calc = Calculator()
    assert calc.ln(2.0) == pytest.approx(math.log(2.0))


def test_ln_non_positive_raises():
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.ln(0)


def test_ln_negative_raises():
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.ln(-1)


# --- history ---

def test_history_initially_empty():
    calc = Calculator()
    assert calc.get_history() == []


def test_history_after_add():
    calc = Calculator()
    calc.add(2, 3)
    assert len(calc.get_history()) == 0  # history is recorded by run_operation, not Calculator methods


def test_history_list_is_instance_attribute():
    calc1 = Calculator()
    calc2 = Calculator()
    calc1.history.append({"test": True})
    assert calc2.get_history() == []


def test_get_history_returns_copy():
    calc = Calculator()
    calc.history.append({"op": "add", "operands": (1, 2), "result": 3})
    copy = calc.get_history()
    copy.append({"op": "fake"})
    assert len(calc.history) == 1


# --- error logging ---

def test_divide_by_zero_logs_error(caplog):
    calc = Calculator()
    with caplog.at_level(logging.ERROR, logger="src.calculator"):
        with pytest.raises(ZeroDivisionError):
            calc.divide(10, 0)
    assert any("divide error" in r.message and "division by zero" in r.message for r in caplog.records)


def test_factorial_negative_logs_error(caplog):
    calc = Calculator()
    with caplog.at_level(logging.ERROR, logger="src.calculator"):
        with pytest.raises(ValueError):
            calc.factorial(-1)
    assert any("factorial error" in r.message for r in caplog.records)


def test_square_root_negative_logs_error(caplog):
    calc = Calculator()
    with caplog.at_level(logging.ERROR, logger="src.calculator"):
        with pytest.raises(ValueError):
            calc.square_root(-4)
    assert any("square_root error" in r.message for r in caplog.records)


def test_log_non_positive_logs_error(caplog):
    calc = Calculator()
    with caplog.at_level(logging.ERROR, logger="src.calculator"):
        with pytest.raises(ValueError):
            calc.log(0)
    assert any("log error" in r.message for r in caplog.records)


def test_ln_non_positive_logs_error(caplog):
    calc = Calculator()
    with caplog.at_level(logging.ERROR, logger="src.calculator"):
        with pytest.raises(ValueError):
            calc.ln(-1)
    assert any("ln error" in r.message for r in caplog.records)
