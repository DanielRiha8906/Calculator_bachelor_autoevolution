import math


class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Division by zero is not allowed")
        return a / b

    def factorial(self, n: int) -> int:
        """Return n! for non-negative integers; raise ValueError otherwise."""
        if not isinstance(n, int):
            raise ValueError("Factorial is only defined for non-negative integers")
        if n < 0:
            raise ValueError("Factorial is not defined for negative integers")
        return math.factorial(n)

