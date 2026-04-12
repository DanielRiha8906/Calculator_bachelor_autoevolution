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
            ValueError: if x is negative (square root of a negative number is undefined in reals).
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

