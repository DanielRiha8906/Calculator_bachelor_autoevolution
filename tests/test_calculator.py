import pytest
import math
from src.calculator import Calculator


@pytest.fixture
def calc():
    return Calculator()


# --- Addition ---

def test_add_positive_numbers(calc):
    assert calc.add(2, 3) == 5

def test_add_negative_numbers(calc):
    assert calc.add(-4, -6) == -10

def test_add_positive_and_negative(calc):
    assert calc.add(10, -3) == 7

def test_add_zero(calc):
    assert calc.add(0, 0) == 0

def test_add_floats(calc):
    assert math.isclose(calc.add(1.1, 2.2), 3.3)


# --- Subtraction ---

def test_subtract_positive_numbers(calc):
    assert calc.subtract(10, 4) == 6

def test_subtract_negative_numbers(calc):
    assert calc.subtract(-3, -7) == 4

def test_subtract_resulting_in_negative(calc):
    assert calc.subtract(2, 9) == -7

def test_subtract_same_number(calc):
    assert calc.subtract(5, 5) == 0

def test_subtract_floats(calc):
    assert math.isclose(calc.subtract(5.5, 2.2), 3.3)


# --- Multiplication ---

def test_multiply_positive_numbers(calc):
    assert calc.multiply(3, 4) == 12

def test_multiply_negative_numbers(calc):
    assert calc.multiply(-3, -4) == 12

def test_multiply_positive_and_negative(calc):
    assert calc.multiply(5, -3) == -15

def test_multiply_by_zero(calc):
    assert calc.multiply(99, 0) == 0

def test_multiply_floats(calc):
    assert math.isclose(calc.multiply(2.5, 4.0), 10.0)


# --- Division ---

def test_divide_positive_numbers(calc):
    assert calc.divide(10, 2) == 5

def test_divide_negative_numbers(calc):
    assert calc.divide(-12, -4) == 3

def test_divide_positive_by_negative(calc):
    assert calc.divide(9, -3) == -3

def test_divide_resulting_in_float(calc):
    assert math.isclose(calc.divide(7, 2), 3.5)

def test_divide_by_zero_raises_value_error():
    calc = Calculator()
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calc.divide(10, 0)


# --- Factorial ---

def test_factorial_zero(calc):
    assert calc.factorial(0) == 1

def test_factorial_one(calc):
    assert calc.factorial(1) == 1

def test_factorial_positive(calc):
    assert calc.factorial(5) == 120

def test_factorial_large(calc):
    assert calc.factorial(10) == 3628800

def test_factorial_negative_raises_value_error(calc):
    with pytest.raises(ValueError, match="Factorial is not defined for negative numbers"):
        calc.factorial(-1)

def test_factorial_non_integer_raises_value_error(calc):
    with pytest.raises(ValueError, match="Factorial requires a non-negative integer"):
        calc.factorial(3.5)


# --- Square ---

def test_square_positive(calc):
    assert calc.square(4) == 16

def test_square_negative(calc):
    assert calc.square(-3) == 9

def test_square_zero(calc):
    assert calc.square(0) == 0

def test_square_float(calc):
    assert math.isclose(calc.square(2.5), 6.25)


# --- Cube ---

def test_cube_positive(calc):
    assert calc.cube(3) == 27

def test_cube_negative(calc):
    assert calc.cube(-2) == -8

def test_cube_zero(calc):
    assert calc.cube(0) == 0

def test_cube_float(calc):
    assert math.isclose(calc.cube(2.0), 8.0)


# --- Square Root ---

def test_sqrt_positive(calc):
    assert math.isclose(calc.sqrt(9), 3.0)

def test_sqrt_zero(calc):
    assert calc.sqrt(0) == 0.0

def test_sqrt_float(calc):
    assert math.isclose(calc.sqrt(2.0), math.sqrt(2.0))

def test_sqrt_negative_raises_value_error(calc):
    with pytest.raises(ValueError, match="Square root is not defined for negative numbers"):
        calc.sqrt(-1)


# --- Cube Root ---

def test_cbrt_positive(calc):
    assert math.isclose(calc.cbrt(27), 3.0)

def test_cbrt_negative(calc):
    assert math.isclose(calc.cbrt(-8), -2.0)

def test_cbrt_zero(calc):
    assert calc.cbrt(0) == 0.0

def test_cbrt_float(calc):
    assert math.isclose(calc.cbrt(1.0), 1.0)


# --- Power ---

def test_power_positive_exponent(calc):
    assert calc.power(2, 10) == 1024

def test_power_zero_exponent(calc):
    assert calc.power(5, 0) == 1

def test_power_negative_exponent(calc):
    assert math.isclose(calc.power(2, -1), 0.5)

def test_power_float_base(calc):
    assert math.isclose(calc.power(4.0, 0.5), 2.0)

def test_power_negative_base(calc):
    assert calc.power(-2, 3) == -8


# --- Log (base 10) ---

def test_log_one(calc):
    assert calc.log(1) == 0.0

def test_log_ten(calc):
    assert math.isclose(calc.log(10), 1.0)

def test_log_hundred(calc):
    assert math.isclose(calc.log(100), 2.0)

def test_log_zero_raises_value_error(calc):
    with pytest.raises(ValueError, match="Logarithm is not defined for non-positive numbers"):
        calc.log(0)

def test_log_negative_raises_value_error(calc):
    with pytest.raises(ValueError, match="Logarithm is not defined for non-positive numbers"):
        calc.log(-5)


# --- Natural Logarithm (ln) ---

def test_ln_one(calc):
    assert calc.ln(1) == 0.0

def test_ln_e(calc):
    assert math.isclose(calc.ln(math.e), 1.0)

def test_ln_positive(calc):
    assert math.isclose(calc.ln(math.e ** 3), 3.0)

def test_ln_zero_raises_value_error(calc):
    with pytest.raises(ValueError, match="Natural logarithm is not defined for non-positive numbers"):
        calc.ln(0)

def test_ln_negative_raises_value_error(calc):
    with pytest.raises(ValueError, match="Natural logarithm is not defined for non-positive numbers"):
        calc.ln(-1)
