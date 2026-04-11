"""Scientific and advanced mathematical operations for the calculator.

Defines unary and binary operations beyond basic arithmetic: powers,
roots, logarithms, and factorial.  Grouping these operations here creates
a clear structural boundary between the standard four-function feature set
and a potential future scientific mode, without requiring the scientific
mode to be fully implemented now.
"""
import math


class ScientificOperations:
    """Mixin providing scientific and advanced mathematical operations."""

    def factorial(self, n: int) -> int:
        """Return n! for non-negative integers.

        Raises:
            TypeError: if n is not an integer.
            ValueError: if n is negative.
        """
        if not isinstance(n, int) or isinstance(n, bool):
            raise TypeError("factorial requires a non-negative integer")
        if n < 0:
            raise ValueError("factorial is not defined for negative integers")
        return math.factorial(n)

    def square(self, n):
        """Return n squared (n²)."""
        return n ** 2

    def cube(self, n):
        """Return n cubed (n³)."""
        return n ** 3

    def sqrt(self, n):
        """Return the square root of n.

        Raises:
            ValueError: if n is negative.
        """
        if n < 0:
            raise ValueError("square root is not defined for negative numbers")
        return math.sqrt(n)

    def cbrt(self, n):
        """Return the cube root of n.

        Defined for all real numbers, including negative values.
        """
        return math.cbrt(n)

    def power(self, base, exp):
        """Return base raised to the power exp.

        Raises:
            ValueError: if the result would be complex
                        (negative base with a non-integer exponent).
        """
        return math.pow(base, exp)

    def log10(self, n):
        """Return the base-10 logarithm of n.

        Raises:
            ValueError: if n is not positive.
        """
        if n <= 0:
            raise ValueError("log10 is not defined for non-positive numbers")
        return math.log10(n)

    def ln(self, n):
        """Return the natural logarithm of n.

        Raises:
            ValueError: if n is not positive.
        """
        if n <= 0:
            raise ValueError("ln is not defined for non-positive numbers")
        return math.log(n)

    def sin(self, theta):
        """Return the sine of theta (in radians)."""
        return math.sin(theta)

    def cos(self, theta):
        """Return the cosine of theta (in radians)."""
        return math.cos(theta)

    def tan(self, theta):
        """Return the tangent of theta (in radians)."""
        return math.tan(theta)

    def cot(self, theta):
        """Return the cotangent of theta (in radians).

        Raises:
            ValueError: if sin(theta) is exactly zero.
        """
        sin_val = math.sin(theta)
        if sin_val == 0.0:
            raise ValueError("cotangent is not defined where sin is zero")
        return math.cos(theta) / sin_val

    def asin(self, n):
        """Return the arcsine of n in radians.

        Raises:
            ValueError: if n is outside [-1, 1].
        """
        if not -1 <= n <= 1:
            raise ValueError("asin is not defined outside the range [-1, 1]")
        return math.asin(n)

    def acos(self, n):
        """Return the arccosine of n in radians.

        Raises:
            ValueError: if n is outside [-1, 1].
        """
        if not -1 <= n <= 1:
            raise ValueError("acos is not defined outside the range [-1, 1]")
        return math.acos(n)
