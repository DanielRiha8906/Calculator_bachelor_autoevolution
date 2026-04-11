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

    def square(self, a):
        return a ** 2

    def cube(self, a):
        return a ** 3

    def square_root(self, a):
        if a < 0:
            raise ValueError("Square root is not defined for negative numbers")
        return math.sqrt(a)

    def cube_root(self, a):
        if a < 0:
            return -((-a) ** (1 / 3))
        return a ** (1 / 3)

    def power(self, base, exp):
        return base ** exp

    def log(self, a, base=10):
        if a <= 0:
            raise ValueError("Logarithm is not defined for non-positive values")
        return math.log(a, base)

    def ln(self, a):
        if a <= 0:
            raise ValueError("Natural logarithm is not defined for non-positive values")
        return math.log(a)

