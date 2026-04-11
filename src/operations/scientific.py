"""Scientific and advanced mathematical operations for the calculator.

Defines unary and binary operations beyond basic arithmetic: powers,
roots, logarithms, factorial, and trigonometric functions.  Grouping these
operations here creates a clear structural boundary between the standard
four-function feature set and the scientific mode.

All trigonometric functions accept and return values in degrees.
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

    def sin(self, angle_deg):
        """Return the sine of angle_deg (in degrees)."""
        return math.sin(math.radians(angle_deg))

    def cos(self, angle_deg):
        """Return the cosine of angle_deg (in degrees)."""
        return math.cos(math.radians(angle_deg))

    def tan(self, angle_deg):
        """Return the tangent of angle_deg (in degrees).

        Raises:
            ValueError: if angle_deg is an odd multiple of 90° (undefined).
        """
        if angle_deg % 180 == 90:
            raise ValueError("tan is undefined at this angle (odd multiple of 90°)")
        return math.tan(math.radians(angle_deg))

    def cot(self, angle_deg):
        """Return the cotangent of angle_deg (in degrees).

        Raises:
            ValueError: if angle_deg is a multiple of 180° (undefined).
        """
        if angle_deg % 180 == 0:
            raise ValueError("cot is undefined at this angle (multiple of 180°)")
        return 1 / math.tan(math.radians(angle_deg))

    def asin(self, x):
        """Return the arcsine of x in degrees.

        Raises:
            ValueError: if x is not in the range [-1, 1].
        """
        if x < -1 or x > 1:
            raise ValueError("asin is not defined for values outside [-1, 1]")
        return math.degrees(math.asin(x))

    def acos(self, x):
        """Return the arccosine of x in degrees.

        Raises:
            ValueError: if x is not in the range [-1, 1].
        """
        if x < -1 or x > 1:
            raise ValueError("acos is not defined for values outside [-1, 1]")
        return math.degrees(math.acos(x))
