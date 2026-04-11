"""Calculator class — public facade over the operations package.

All computation is delegated to the organised sub-modules in
:mod:`src.operations`.  The :class:`Calculator` class keeps a stable
interface for the controller and the rest of the application while the
operations themselves live in categorised modules that can be extended
independently.
"""

from .operations.arithmetic import add, subtract, multiply, divide
from .operations.algebraic import power, square, cube, square_root, cube_root, factorial
from .operations.transcendental import log, ln


class Calculator:
    """Facade that exposes all calculator operations as instance methods.

    Delegates every computation to the corresponding function in
    :mod:`src.operations`.  Adding a new operation category only requires
    creating a new module under ``src/operations/`` and importing it here.
    """

    def add(self, a, b):
        return add(a, b)

    def subtract(self, a, b):
        return subtract(a, b)

    def multiply(self, a, b):
        return multiply(a, b)

    def divide(self, a, b):
        return divide(a, b)

    def factorial(self, n):
        return factorial(n)

    def square(self, a):
        return square(a)

    def cube(self, a):
        return cube(a)

    def square_root(self, a):
        return square_root(a)

    def cube_root(self, a):
        return cube_root(a)

    def power(self, base, exp):
        return power(base, exp)

    def log(self, a, base=10):
        return log(a, base)

    def ln(self, a):
        return ln(a)
