import pytest
import math
from src.calculator import Calculator


class TestAdd:
    def setup_method(self):
        self.calc = Calculator()

    def test_add_positive_numbers(self):
        assert self.calc.add(3, 5) == 8

    def test_add_negative_numbers(self):
        assert self.calc.add(-3, -5) == -8

    def test_add_positive_and_negative(self):
        assert self.calc.add(10, -4) == 6

    def test_add_zero(self):
        assert self.calc.add(7, 0) == 7

    def test_add_both_zero(self):
        assert self.calc.add(0, 0) == 0


class TestSubtract:
    def setup_method(self):
        self.calc = Calculator()

    def test_subtract_positive_numbers(self):
        assert self.calc.subtract(10, 4) == 6

    def test_subtract_negative_numbers(self):
        assert self.calc.subtract(-3, -5) == 2

    def test_subtract_positive_and_negative(self):
        assert self.calc.subtract(5, -3) == 8

    def test_subtract_zero(self):
        assert self.calc.subtract(9, 0) == 9

    def test_subtract_to_zero(self):
        assert self.calc.subtract(5, 5) == 0


class TestMultiply:
    def setup_method(self):
        self.calc = Calculator()

    def test_multiply_positive_numbers(self):
        assert self.calc.multiply(3, 4) == 12

    def test_multiply_negative_numbers(self):
        assert self.calc.multiply(-3, -4) == 12

    def test_multiply_positive_and_negative(self):
        assert self.calc.multiply(3, -4) == -12

    def test_multiply_by_zero(self):
        assert self.calc.multiply(5, 0) == 0

    def test_multiply_by_one(self):
        assert self.calc.multiply(7, 1) == 7


class TestDivide:
    def setup_method(self):
        self.calc = Calculator()

    def test_divide_normal(self):
        assert self.calc.divide(10, 2) == 5

    def test_divide_by_zero_raises_value_error(self):
        with pytest.raises(ValueError, match="Division by zero is not allowed"):
            self.calc.divide(10, 0)

    def test_divide_negative_by_zero_raises_value_error(self):
        with pytest.raises(ValueError):
            self.calc.divide(-5, 0)

    def test_divide_zero_by_zero_raises_value_error(self):
        with pytest.raises(ValueError):
            self.calc.divide(0, 0)


class TestFactorial:
    def setup_method(self):
        self.calc = Calculator()

    def test_factorial_of_zero(self):
        assert self.calc.factorial(0) == 1

    def test_factorial_of_one(self):
        assert self.calc.factorial(1) == 1

    def test_factorial_of_positive_number(self):
        assert self.calc.factorial(5) == 120

    def test_factorial_large_number(self):
        assert self.calc.factorial(10) == 3628800

    def test_factorial_negative_raises_value_error(self):
        with pytest.raises(ValueError, match="Factorial is not defined for negative numbers"):
            self.calc.factorial(-1)

    def test_factorial_float_raises_type_error(self):
        with pytest.raises(TypeError, match="Factorial is only defined for integers"):
            self.calc.factorial(3.5)


class TestSquare:
    def setup_method(self):
        self.calc = Calculator()

    def test_square_positive(self):
        assert self.calc.square(4) == 16

    def test_square_negative(self):
        assert self.calc.square(-3) == 9

    def test_square_zero(self):
        assert self.calc.square(0) == 0

    def test_square_float(self):
        assert self.calc.square(2.5) == pytest.approx(6.25)


class TestCube:
    def setup_method(self):
        self.calc = Calculator()

    def test_cube_positive(self):
        assert self.calc.cube(3) == 27

    def test_cube_negative(self):
        assert self.calc.cube(-2) == -8

    def test_cube_zero(self):
        assert self.calc.cube(0) == 0

    def test_cube_float(self):
        assert self.calc.cube(2.0) == pytest.approx(8.0)


class TestSquareRoot:
    def setup_method(self):
        self.calc = Calculator()

    def test_square_root_positive(self):
        assert self.calc.square_root(9) == pytest.approx(3.0)

    def test_square_root_zero(self):
        assert self.calc.square_root(0) == pytest.approx(0.0)

    def test_square_root_float(self):
        assert self.calc.square_root(2.0) == pytest.approx(math.sqrt(2))

    def test_square_root_negative_raises_value_error(self):
        with pytest.raises(ValueError, match="Square root is not defined for negative numbers"):
            self.calc.square_root(-1)


class TestCubeRoot:
    def setup_method(self):
        self.calc = Calculator()

    def test_cube_root_positive(self):
        assert self.calc.cube_root(27) == pytest.approx(3.0)

    def test_cube_root_negative(self):
        assert self.calc.cube_root(-8) == pytest.approx(-2.0)

    def test_cube_root_zero(self):
        assert self.calc.cube_root(0) == pytest.approx(0.0)

    def test_cube_root_float(self):
        assert self.calc.cube_root(1.0) == pytest.approx(1.0)


class TestPower:
    def setup_method(self):
        self.calc = Calculator()

    def test_power_positive_exponent(self):
        assert self.calc.power(2, 10) == 1024

    def test_power_zero_exponent(self):
        assert self.calc.power(5, 0) == 1

    def test_power_negative_exponent(self):
        assert self.calc.power(2, -1) == pytest.approx(0.5)

    def test_power_fractional_exponent(self):
        assert self.calc.power(9, 0.5) == pytest.approx(3.0)

    def test_power_base_zero(self):
        assert self.calc.power(0, 5) == 0


class TestLog:
    def setup_method(self):
        self.calc = Calculator()

    def test_log_of_one(self):
        assert self.calc.log(1) == pytest.approx(0.0)

    def test_log_of_ten(self):
        assert self.calc.log(10) == pytest.approx(1.0)

    def test_log_of_hundred(self):
        assert self.calc.log(100) == pytest.approx(2.0)

    def test_log_zero_raises_value_error(self):
        with pytest.raises(ValueError, match="Logarithm is not defined for non-positive numbers"):
            self.calc.log(0)

    def test_log_negative_raises_value_error(self):
        with pytest.raises(ValueError):
            self.calc.log(-5)


class TestLn:
    def setup_method(self):
        self.calc = Calculator()

    def test_ln_of_one(self):
        assert self.calc.ln(1) == pytest.approx(0.0)

    def test_ln_of_e(self):
        assert self.calc.ln(math.e) == pytest.approx(1.0)

    def test_ln_positive(self):
        assert self.calc.ln(math.e ** 3) == pytest.approx(3.0)

    def test_ln_zero_raises_value_error(self):
        with pytest.raises(ValueError, match="Natural logarithm is not defined for non-positive numbers"):
            self.calc.ln(0)

    def test_ln_negative_raises_value_error(self):
        with pytest.raises(ValueError):
            self.calc.ln(-1)
