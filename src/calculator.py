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
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b

    def factorial(self, n):
        if not isinstance(n, int) or isinstance(n, bool):
            raise ValueError("Factorial requires a non-negative integer")
        if n < 0:
            raise ValueError("Factorial is not defined for negative integers")
        return math.factorial(n)

