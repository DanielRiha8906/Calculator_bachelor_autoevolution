"""Scientific calculator mode operations.

Pure functions for trigonometric, hyperbolic, and exponential operations.
All angle inputs and outputs are in radians.
"""
import math


def sin(x):
    """Return the sine of x (x in radians)."""
    return math.sin(x)


def cos(x):
    """Return the cosine of x (x in radians)."""
    return math.cos(x)


def tan(x):
    """Return the tangent of x (x in radians)."""
    return math.tan(x)


def asin(x):
    """Return the arcsine of x in radians. Raises ValueError for |x| > 1."""
    return math.asin(x)


def acos(x):
    """Return the arccosine of x in radians. Raises ValueError for |x| > 1."""
    return math.acos(x)


def atan(x):
    """Return the arctangent of x in radians."""
    return math.atan(x)


def sinh(x):
    """Return the hyperbolic sine of x."""
    return math.sinh(x)


def cosh(x):
    """Return the hyperbolic cosine of x."""
    return math.cosh(x)


def tanh(x):
    """Return the hyperbolic tangent of x."""
    return math.tanh(x)


def exp(x):
    """Return e raised to the power x."""
    return math.exp(x)
