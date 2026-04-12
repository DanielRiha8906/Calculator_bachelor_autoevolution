import math


class Calculator:
    def __init__(self):
        self.history: list[dict] = []

    def get_history(self) -> list[dict]:
        """Return a copy of the operation history list."""
        return list(self.history)

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        return a / b

    def factorial(self, n):
        return math.factorial(n)

    def square(self, n):
        return n ** 2

    def cube(self, n):
        return n ** 3

    def square_root(self, n):
        return math.sqrt(n)

    def cube_root(self, n):
        return math.cbrt(n)

    def power(self, base, exp):
        return base ** exp

    def log(self, n):
        return math.log10(n)

    def ln(self, n):
        return math.log(n)

