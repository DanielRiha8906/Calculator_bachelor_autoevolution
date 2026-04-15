"""Scientific operations: factorial, square, cube, square_root, cube_root, power, log, ln."""
import math


def factorial(n: int) -> int:
    """Return n! for non-negative integers; raise ValueError otherwise."""
    if not isinstance(n, int):
        raise ValueError("Factorial is only defined for non-negative integers")
    if n < 0:
        raise ValueError("Factorial is not defined for negative integers")
    return math.factorial(n)


def square(a):
    """Return a squared (a ** 2)."""
    return a ** 2


def cube(a):
    """Return a cubed (a ** 3)."""
    return a ** 3


def square_root(a):
    """Return the square root of a; raise ValueError for negative input."""
    if a < 0:
        raise ValueError("Square root is not defined for negative numbers")
    return math.sqrt(a)


def cube_root(a):
    """Return the real cube root of a (supports negative input)."""
    if a < 0:
        return -((-a) ** (1 / 3))
    return a ** (1 / 3)


def power(a, b):
    """Return a raised to the power b (a ** b)."""
    return a ** b


def log(a, base):
    """Return log base `base` of a; raise ValueError for non-positive a or invalid base."""
    if a <= 0:
        raise ValueError("Logarithm is not defined for non-positive numbers")
    if base <= 0 or base == 1:
        raise ValueError("Logarithm base must be positive and not equal to 1")
    return math.log(a, base)


def ln(a):
    """Return the natural logarithm of a; raise ValueError for non-positive input."""
    if a <= 0:
        raise ValueError("Natural logarithm is not defined for non-positive numbers")
    return math.log(a)
