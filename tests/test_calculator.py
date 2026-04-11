import pytest
import math
from src.calculator import Calculator


@pytest.fixture
def calc():
    return Calculator()


# --- add ---

def test_add_positive_numbers(calc):
    assert calc.add(2, 3) == 5


def test_add_negative_numbers(calc):
    assert calc.add(-2, -3) == -5


def test_add_mixed_signs(calc):
    assert calc.add(-2, 3) == 1


def test_add_floats(calc):
    assert calc.add(1.5, 2.5) == pytest.approx(4.0)


def test_add_zero(calc):
    assert calc.add(5, 0) == 5


def test_add_invalid_input_raises_type_error(calc):
    with pytest.raises(TypeError):
        calc.add("a", 1)


# --- subtract ---

def test_subtract_positive_numbers(calc):
    assert calc.subtract(5, 3) == 2


def test_subtract_negative_numbers(calc):
    assert calc.subtract(-2, -3) == 1


def test_subtract_result_negative(calc):
    assert calc.subtract(3, 5) == -2


def test_subtract_floats(calc):
    assert calc.subtract(5.5, 2.5) == pytest.approx(3.0)


def test_subtract_zero(calc):
    assert calc.subtract(5, 0) == 5


def test_subtract_invalid_input_raises_type_error(calc):
    with pytest.raises(TypeError):
        calc.subtract(None, 1)


# --- multiply ---

def test_multiply_positive_numbers(calc):
    assert calc.multiply(3, 4) == 12


def test_multiply_negative_and_positive(calc):
    assert calc.multiply(-3, 4) == -12


def test_multiply_both_negative(calc):
    assert calc.multiply(-3, -4) == 12


def test_multiply_by_zero(calc):
    assert calc.multiply(5, 0) == 0


def test_multiply_floats(calc):
    assert calc.multiply(2.5, 2.0) == pytest.approx(5.0)


def test_multiply_float_precision(calc):
    # 0.1 * 3 cannot be represented exactly in IEEE 754; use approx
    assert calc.multiply(0.1, 3) == pytest.approx(0.3)


def test_multiply_invalid_input_raises_type_error(calc):
    with pytest.raises(TypeError):
        calc.multiply(None, 2)


# --- divide ---

def test_divide_positive_numbers(calc):
    assert calc.divide(10, 2) == pytest.approx(5.0)


def test_divide_negative_numerator(calc):
    assert calc.divide(-10, 2) == pytest.approx(-5.0)


def test_divide_negative_denominator(calc):
    assert calc.divide(10, -2) == pytest.approx(-5.0)


def test_divide_both_negative(calc):
    assert calc.divide(-10, -2) == pytest.approx(5.0)


def test_divide_result_is_float(calc):
    # Integer inputs that don't divide evenly must return a float
    assert calc.divide(1, 3) == pytest.approx(1 / 3)


def test_divide_floats(calc):
    assert calc.divide(5.0, 2.0) == pytest.approx(2.5)


def test_divide_float_precision(calc):
    # 1.0 / 3.0 is an infinitely repeating decimal; use approx
    assert calc.divide(1.0, 3.0) == pytest.approx(0.3333333333333333)


def test_divide_by_zero_raises_error(calc):
    with pytest.raises(ZeroDivisionError):
        calc.divide(10, 0)


def test_divide_zero_numerator(calc):
    assert calc.divide(0, 5) == pytest.approx(0.0)


def test_divide_invalid_input_raises_type_error(calc):
    with pytest.raises(TypeError):
        calc.divide("a", 2)


# --- factorial ---

def test_factorial_zero(calc):
    assert calc.factorial(0) == 1


def test_factorial_one(calc):
    assert calc.factorial(1) == 1


def test_factorial_positive(calc):
    assert calc.factorial(5) == 120


def test_factorial_large(calc):
    assert calc.factorial(10) == 3628800


def test_factorial_negative_raises_value_error(calc):
    with pytest.raises(ValueError):
        calc.factorial(-1)


def test_factorial_float_raises_type_error(calc):
    with pytest.raises(TypeError):
        calc.factorial(3.0)


def test_factorial_string_raises_type_error(calc):
    with pytest.raises(TypeError):
        calc.factorial("5")


def test_factorial_none_raises_type_error(calc):
    with pytest.raises(TypeError):
        calc.factorial(None)


def test_factorial_bool_raises_type_error(calc):
    # bool is a subclass of int in Python; reject it explicitly
    with pytest.raises(TypeError):
        calc.factorial(True)
