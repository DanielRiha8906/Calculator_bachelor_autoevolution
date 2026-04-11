"""Tests for ScientificCalculator.

Verifies that ScientificCalculator inherits all Calculator operations and is a
proper subclass, ready to accept future scientific-only methods.
"""

import math
import pytest
from src.scientific_calculator import ScientificCalculator


class TestScientificCalculatorIsSubclass:
    def test_is_subclass_of_calculator(self):
        from src.calculator import Calculator
        assert issubclass(ScientificCalculator, Calculator)

    def test_instance_is_calculator(self):
        from src.calculator import Calculator
        calc = ScientificCalculator()
        assert isinstance(calc, Calculator)


class TestScientificCalculatorInheritsBasicOps:
    def setup_method(self):
        self.calc = ScientificCalculator()

    def test_add(self):
        assert self.calc.add(3, 4) == 7

    def test_subtract(self):
        assert self.calc.subtract(10, 3) == 7

    def test_multiply(self):
        assert self.calc.multiply(3, 4) == 12

    def test_divide(self):
        assert self.calc.divide(10, 4) == 2.5

    def test_divide_by_zero_raises(self):
        with pytest.raises(ZeroDivisionError):
            self.calc.divide(1, 0)


class TestScientificCalculatorInheritsScientificOps:
    def setup_method(self):
        self.calc = ScientificCalculator()

    def test_factorial(self):
        assert self.calc.factorial(5) == 120

    def test_square(self):
        assert self.calc.square(4) == 16

    def test_cube(self):
        assert self.calc.cube(3) == 27

    def test_square_root(self):
        assert self.calc.square_root(9) == 3.0

    def test_cube_root(self):
        assert self.calc.cube_root(27) == pytest.approx(3.0)

    def test_power(self):
        assert self.calc.power(2, 10) == 1024.0

    def test_log(self):
        assert self.calc.log(100) == pytest.approx(2.0)

    def test_ln(self):
        assert self.calc.ln(math.e) == pytest.approx(1.0)


class TestScientificCalculatorHistory:
    def setup_method(self):
        self.calc = ScientificCalculator()

    def test_history_starts_empty(self):
        assert self.calc.get_history() == []

    def test_history_records_inherited_ops(self):
        self.calc.add(1, 2)
        self.calc.square(4)
        history = self.calc.get_history()
        assert len(history) == 2
        assert history[0]["operation"] == "add"
        assert history[1]["operation"] == "square"

    def test_clear_history(self):
        self.calc.add(1, 2)
        self.calc.clear_history()
        assert self.calc.get_history() == []
