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

