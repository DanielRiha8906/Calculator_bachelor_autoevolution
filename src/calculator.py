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

    def square(self, a: float) -> float:
        """Return a squared (a²)."""
        return a * a

    def cube(self, a: float) -> float:
        """Return a cubed (a³)."""
        return a * a * a

    def square_root(self, a: float) -> float:
        """Return the square root of a.

        Raises:
            ValueError: if a is negative.
        """
        if a < 0:
            raise ValueError("square root is not defined for negative numbers")
        return math.sqrt(a)

    def cube_root(self, a: float) -> float:
        """Return the real cube root of a.

        Unlike square root, cube root is defined for negative numbers.
        """
        if a < 0:
            return -((-a) ** (1 / 3))
        return a ** (1 / 3)

    def power(self, base: float, exponent: float) -> float:
        """Return base raised to the power of exponent."""
        return base ** exponent

    def log(self, a: float) -> float:
        """Return the base-10 logarithm of a.

        Raises:
            ValueError: if a is zero or negative.
        """
        if a <= 0:
            raise ValueError("log is not defined for zero or negative numbers")
        return math.log10(a)

    def ln(self, a: float) -> float:
        """Return the natural logarithm of a.

        Raises:
            ValueError: if a is zero or negative.
        """
        if a <= 0:
            raise ValueError("ln is not defined for zero or negative numbers")
        return math.log(a)

