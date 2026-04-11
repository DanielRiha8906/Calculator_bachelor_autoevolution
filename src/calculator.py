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

