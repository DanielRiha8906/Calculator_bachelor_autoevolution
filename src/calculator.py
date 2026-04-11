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
        return math.factorial(n)

    def square(self, x: float) -> float:
        return x ** 2

    def cube(self, x: float) -> float:
        return x ** 3

    def square_root(self, x: float) -> float:
        return math.sqrt(x)

    def cube_root(self, x: float) -> float:
        return math.cbrt(x)

    def power(self, base: float, exp: float) -> float:
        return math.pow(base, exp)

    def log(self, x: float) -> float:
        return math.log10(x)

    def ln(self, x: float) -> float:
        return math.log(x)

