import pytest
import math
from src.calculator import Calculator


@pytest.fixture
def calc():
    return Calculator()


# --- add ---

def test_add_positive_integers(calc):
    assert calc.add(3, 4) == 7

def test_add_negative_integers(calc):
    assert calc.add(-3, -4) == -7

def test_add_mixed_sign(calc):
    assert calc.add(-3, 4) == 1

def test_add_zeros(calc):
    assert calc.add(0, 0) == 0

def test_add_floats(calc):
    assert calc.add(1.5, 2.5) == 4.0

def test_add_invalid_type_raises(calc):
    with pytest.raises(TypeError):
        calc.add("a", 1)

def test_add_none_raises(calc):
    with pytest.raises(TypeError):
        calc.add(None, 1)


# --- subtract ---

def test_subtract_positive_integers(calc):
    assert calc.subtract(10, 3) == 7

def test_subtract_negative_result(calc):
    assert calc.subtract(3, 10) == -7

def test_subtract_same_values(calc):
    assert calc.subtract(5, 5) == 0

def test_subtract_zeros(calc):
    assert calc.subtract(0, 0) == 0

def test_subtract_floats(calc):
    assert calc.subtract(5.5, 2.5) == 3.0

def test_subtract_invalid_type_raises(calc):
    with pytest.raises(TypeError):
        calc.subtract("b", 2)


# --- multiply ---

def test_multiply_positive_integers(calc):
    assert calc.multiply(3, 4) == 12

def test_multiply_by_zero(calc):
    assert calc.multiply(99, 0) == 0

def test_multiply_negative_numbers(calc):
    assert calc.multiply(-3, 4) == -12

def test_multiply_two_negatives(calc):
    assert calc.multiply(-3, -4) == 12

def test_multiply_floats_precision(calc):
    # 0.1 * 3 has a known floating-point representation issue;
    # verify against math.isclose rather than exact equality.
    result = calc.multiply(0.1, 3)
    assert math.isclose(result, 0.3, rel_tol=1e-9)

def test_multiply_float_by_integer(calc):
    assert calc.multiply(2.5, 4) == 10.0

def test_multiply_invalid_type_raises(calc):
    # str * str is not supported by Python's * operator
    with pytest.raises(TypeError):
        calc.multiply("x", "y")


# --- divide ---

def test_divide_by_zero_raises(calc):
    with pytest.raises(ZeroDivisionError):
        calc.divide(1, 0)

def test_divide_positive_integers(calc):
    assert calc.divide(10, 2) == 5.0

def test_divide_produces_float(calc):
    # Python 3 true division always returns float
    result = calc.divide(7, 2)
    assert result == 3.5

def test_divide_negative_dividend(calc):
    assert calc.divide(-9, 3) == -3.0

def test_divide_negative_divisor(calc):
    assert calc.divide(9, -3) == -3.0

def test_divide_both_negative(calc):
    assert calc.divide(-9, -3) == 3.0

def test_divide_float_precision(calc):
    result = calc.divide(1.0, 3.0)
    assert math.isclose(result, 1 / 3, rel_tol=1e-9)

def test_divide_zero_dividend(calc):
    assert calc.divide(0, 5) == 0.0

def test_divide_float_by_zero_raises(calc):
    with pytest.raises(ZeroDivisionError):
        calc.divide(1.0, 0)

def test_divide_invalid_type_raises(calc):
    with pytest.raises(TypeError):
        calc.divide("y", 2)
