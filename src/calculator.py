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
        if not isinstance(n, int):
            raise TypeError("Factorial is only defined for integers")
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    def square(self, x):
        return x ** 2

    def cube(self, x):
        return x ** 3

    def square_root(self, x):
        if x < 0:
            raise ValueError("Square root is not defined for negative numbers")
        return math.sqrt(x)

    def cube_root(self, x):
        return math.copysign(abs(x) ** (1 / 3), x)

    def power(self, base, exp):
        return base ** exp

    def log(self, x):
        if x <= 0:
            raise ValueError("Logarithm is not defined for non-positive numbers")
        return math.log10(x)

    def ln(self, x):
        if x <= 0:
            raise ValueError("Natural logarithm is not defined for non-positive numbers")
        return math.log(x)

