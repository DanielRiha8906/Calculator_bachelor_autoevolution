"""Advanced mathematical operations: power, roots, factorial, and logarithms."""
import math


def factorial(n: int) -> int:
    """Return n!. Raises ValueError for negative n."""
    return math.factorial(n)


def square(n: "float | int") -> "float | int":
    """Return n squared (n ** 2)."""
    return n ** 2


def cube(n: "float | int") -> "float | int":
    """Return n cubed (n ** 3)."""
    return n ** 3


def square_root(n: "float | int") -> float:
    """Return the square root of n. Raises ValueError for negative n."""
    return math.sqrt(n)


def cube_root(n: "float | int") -> float:
    """Return the cube root of n. Handles negative inputs (requires Python 3.11+)."""
    return math.cbrt(n)


def power(base: "float | int", exp: "float | int") -> "float | int":
    """Return base raised to the power exp."""
    return base ** exp


def log(n: "float | int") -> float:
    """Return the base-10 logarithm of n. Raises ValueError for n <= 0."""
    return math.log10(n)


def ln(n: "float | int") -> float:
    """Return the natural logarithm of n. Raises ValueError for n <= 0."""
    return math.log(n)
