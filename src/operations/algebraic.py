"""Algebraic operations: powers, roots, and factorial.

Each function is a pure computation — no I/O, no state.
"""
import math


def power(base: float, exp: float) -> float:
    """Return *base* raised to the power of *exp*."""
    return base ** exp


def square(a: float) -> float:
    """Return *a* squared (a²)."""
    return a ** 2


def cube(a: float) -> float:
    """Return *a* cubed (a³)."""
    return a ** 3


def square_root(a: float) -> float:
    """Return the square root of *a*.

    Raises:
        ValueError: When *a* is negative.
    """
    if a < 0:
        raise ValueError("Square root is not defined for negative numbers")
    return math.sqrt(a)


def cube_root(a: float) -> float:
    """Return the cube root of *a*.

    Supports negative inputs by computing the real cube root directly.
    """
    if a < 0:
        return -((-a) ** (1 / 3))
    return a ** (1 / 3)


def factorial(n: int) -> int:
    """Return *n*! (n factorial).

    Raises:
        ValueError: When *n* is not a non-negative integer.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise ValueError("Factorial requires a non-negative integer")
    if n < 0:
        raise ValueError("Factorial is not defined for negative integers")
    return math.factorial(n)
