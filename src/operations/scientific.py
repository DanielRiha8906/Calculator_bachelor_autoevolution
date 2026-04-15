"""Scientific / advanced operations for the Calculator.

Contains operations beyond basic arithmetic: exponentiation, roots,
powers, factorial, logarithms, and trigonometric functions.  These are
the operations typically found in the scientific mode of a calculator,
and are collected here so the structural boundary between normal and
scientific functionality is clear.

All trigonometric functions accept and return values in degrees.
"""

import math


class ScientificOperations:
    """Advanced mathematical operations: powers, roots, logs, factorial, trig.

    Intended to be combined with :class:`BasicOperations` via multiple
    inheritance to build the full :class:`~src.calculator.Calculator`.
    """

    def factorial(self, n: int) -> int:
        """Return n! for non-negative integers.

        Raises:
            TypeError: if n is not an integer (floats and booleans are rejected).
            ValueError: if n is a negative integer.
        """
        if isinstance(n, bool) or not isinstance(n, int):
            raise TypeError("factorial requires a non-negative integer")
        if n < 0:
            raise ValueError("factorial is not defined for negative integers")
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    def square(self, x) -> float:
        """Return x squared (x²)."""
        return x * x

    def cube(self, x) -> float:
        """Return x cubed (x³)."""
        return x * x * x

    def square_root(self, x) -> float:
        """Return the square root of x.

        Raises:
            ValueError: if x is negative (square root of a negative number
                is undefined in the reals).
        """
        if x < 0:
            raise ValueError("square root is not defined for negative numbers")
        return math.sqrt(x)

    def cube_root(self, x) -> float:
        """Return the real cube root of x.

        Unlike square root, cube root is defined for negative numbers:
        the cube root of a negative number is negative.
        """
        if x < 0:
            return -(abs(x) ** (1 / 3))
        return x ** (1 / 3)

    def power(self, base, exp) -> float:
        """Return base raised to the power of exp."""
        return base ** exp

    def log(self, x) -> float:
        """Return the base-10 logarithm of x.

        Raises:
            ValueError: if x is less than or equal to zero.
        """
        if x <= 0:
            raise ValueError("log is not defined for non-positive numbers")
        return math.log10(x)

    def ln(self, x) -> float:
        """Return the natural logarithm of x.

        Raises:
            ValueError: if x is less than or equal to zero.
        """
        if x <= 0:
            raise ValueError("ln is not defined for non-positive numbers")
        return math.log(x)

    def sin(self, x) -> float:
        """Return the sine of x, where x is in degrees."""
        return math.sin(math.radians(x))

    def cos(self, x) -> float:
        """Return the cosine of x, where x is in degrees."""
        return math.cos(math.radians(x))

    def tan(self, x) -> float:
        """Return the tangent of x, where x is in degrees.

        Raises:
            ValueError: if x is an odd multiple of 90 degrees (cos x = 0).
        """
        cos_val = math.cos(math.radians(x))
        if abs(cos_val) < 1e-10:
            raise ValueError("tan is not defined where cos(x) = 0")
        return math.tan(math.radians(x))

    def cot(self, x) -> float:
        """Return the cotangent of x, where x is in degrees.

        Raises:
            ValueError: if x is a multiple of 180 degrees (sin x = 0).
        """
        sin_val = math.sin(math.radians(x))
        if abs(sin_val) < 1e-10:
            raise ValueError("cot is not defined where sin(x) = 0")
        return math.cos(math.radians(x)) / sin_val

    def asin(self, x) -> float:
        """Return the arcsine of x in degrees.

        Raises:
            ValueError: if x is not in the range [-1, 1].
        """
        if x < -1 or x > 1:
            raise ValueError("asin is not defined for values outside [-1, 1]")
        return math.degrees(math.asin(x))

    def acos(self, x) -> float:
        """Return the arccosine of x in degrees.

        Raises:
            ValueError: if x is not in the range [-1, 1].
        """
        if x < -1 or x > 1:
            raise ValueError("acos is not defined for values outside [-1, 1]")
        return math.degrees(math.acos(x))
