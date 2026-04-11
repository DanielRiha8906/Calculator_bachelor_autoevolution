"""Transcendental operations: logarithms and natural logarithm.

Each function is a pure computation — no I/O, no state.

Adding further transcendental functions (e.g. trigonometric, exponential)
to this module keeps related mathematical concepts together and avoids
polluting the core Calculator class.
"""
import math


def log(a: float, base: float = 10) -> float:
    """Return the logarithm of *a* in the given *base* (default base 10).

    Raises:
        ValueError: When *a* is non-positive.
    """
    if a <= 0:
        raise ValueError("Logarithm is not defined for non-positive values")
    return math.log(a, base)


def ln(a: float) -> float:
    """Return the natural logarithm of *a* (log base e).

    Raises:
        ValueError: When *a* is non-positive.
    """
    if a <= 0:
        raise ValueError("Natural logarithm is not defined for non-positive values")
    return math.log(a)
