"""Calculator package — public API.

This package exposes two classes:

Calculator
    Stateful arithmetic and scientific calculator with operation history.
    Supports: add, subtract, multiply, divide, factorial, square, cube,
    square_root, cube_root, power, log, ln.

ScientificCalculator
    Subclass of Calculator reserved for future scientific-only operations
    (e.g. trigonometric, hyperbolic, combinatorial functions).  Currently
    identical in behaviour to Calculator.

Usage example::

    from src import Calculator

    calc = Calculator()
    print(calc.add(3, 4))       # 7
    print(calc.factorial(5))    # 120
    print(calc.get_history())   # [{'operation': 'add', ...}, ...]
"""

from .calculator import Calculator
from .scientific_calculator import ScientificCalculator

__all__ = ["Calculator", "ScientificCalculator"]
