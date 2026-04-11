"""Operations package for the calculator.

Organises calculator operations by mathematical category so that new
categories (e.g. trigonometric, statistical) can be added as separate
modules without reorganising existing code.

Public re-exports
-----------------
All individual operation functions are re-exported here so callers can
import them from a single location::

    from src.operations import add, divide, factorial, ln

Alternatively, import from the specific sub-module when you need only one
category::

    from src.operations.arithmetic import add, subtract
"""

from .arithmetic import add, subtract, multiply, divide
from .algebraic import power, square, cube, square_root, cube_root, factorial
from .transcendental import log, ln

__all__ = [
    # arithmetic
    "add",
    "subtract",
    "multiply",
    "divide",
    # algebraic
    "power",
    "square",
    "cube",
    "square_root",
    "cube_root",
    "factorial",
    # transcendental
    "log",
    "ln",
]
