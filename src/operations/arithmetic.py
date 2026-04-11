"""Arithmetic operations: addition, subtraction, multiplication, division.

Each function is a pure computation — no I/O, no state.
"""


def add(a: float, b: float) -> float:
    """Return the sum of *a* and *b*."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Return *a* minus *b*."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Return the product of *a* and *b*."""
    return a * b


def divide(a: float, b: float) -> float:
    """Return *a* divided by *b*.

    Raises:
        ZeroDivisionError: When *b* is zero.
    """
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b
