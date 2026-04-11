"""Pure functions for scientific calculator operations."""

import math


def factorial(n: int) -> int:
    """Return n! (n factorial).

    Raises:
        ValueError: if n is negative.
        TypeError: if n is not an integer.
    """
    return math.factorial(n)


def square(x: float) -> float:
    """Return x squared (x ** 2)."""
    return x ** 2


def cube(x: float) -> float:
    """Return x cubed (x ** 3)."""
    return x ** 3


def square_root(x: float) -> float:
    """Return the square root of x.

    Raises:
        ValueError: if x is negative.
    """
    return math.sqrt(x)


def cube_root(x: float) -> float:
    """Return the real cube root of x."""
    return math.cbrt(x)


def power(base: float, exp: float) -> float:
    """Return base raised to the power exp."""
    return math.pow(base, exp)


def log(x: float) -> float:
    """Return the base-10 logarithm of x.

    Raises:
        ValueError: if x is zero or negative.
    """
    return math.log10(x)


def ln(x: float) -> float:
    """Return the natural logarithm of x.

    Raises:
        ValueError: if x is zero or negative.
    """
    return math.log(x)
