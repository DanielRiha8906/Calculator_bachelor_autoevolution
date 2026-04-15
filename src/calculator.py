"""Core Calculator class.

Provides a unified object-oriented interface over the operation implementations
in :mod:`src.operations.basic` and :mod:`src.operations.scientific`.
The :meth:`Calculator.execute` method acts as the logic-layer dispatch point,
allowing callers to route by operation name without importing individual
operation functions.
"""
from .operations.basic import add, subtract, multiply, divide
from .operations.scientific import (
    factorial, square, cube, square_root, cube_root, power, log, ln,
)


class Calculator:
    def add(self, a, b):
        return add(a, b)

    def subtract(self, a, b):
        return subtract(a, b)

    def multiply(self, a, b):
        return multiply(a, b)

    def divide(self, a, b):
        return divide(a, b)

    def factorial(self, n: int) -> int:
        """Return n! for non-negative integers; raise ValueError otherwise."""
        return factorial(n)

    def square(self, a):
        """Return a squared (a ** 2)."""
        return square(a)

    def cube(self, a):
        """Return a cubed (a ** 3)."""
        return cube(a)

    def square_root(self, a):
        """Return the square root of a; raise ValueError for negative input."""
        return square_root(a)

    def cube_root(self, a):
        """Return the real cube root of a (supports negative input)."""
        return cube_root(a)

    def power(self, a, b):
        """Return a raised to the power b (a ** b)."""
        return power(a, b)

    def log(self, a, base):
        """Return log base `base` of a; raise ValueError for non-positive a or invalid base."""
        return log(a, base)

    def ln(self, a):
        """Return the natural logarithm of a; raise ValueError for non-positive input."""
        return ln(a)

    def execute(self, operation: str, *args):
        """Dispatch to the named Calculator method with the given arguments.

        Separates calculation logic from caller code — callers supply an
        operation name and already-validated arguments; this method routes to
        the correct Calculator method without the caller needing to know the
        method directly.

        Raises ValueError for unrecognised or non-callable operation names.
        """
        method = getattr(self, operation, None)
        if method is None or not callable(method):
            raise ValueError(f"Unknown operation: '{operation}'")
        return method(*args)
