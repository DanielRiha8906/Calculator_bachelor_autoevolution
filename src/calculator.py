import math


class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        return a / b

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

