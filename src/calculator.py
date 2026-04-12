import logging
import math

logger = logging.getLogger(__name__)


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
        try:
            return a / b
        except ZeroDivisionError:
            logger.error("divide error: division by zero (a=%s, b=%s)", a, b)
            raise

    def factorial(self, n):
        try:
            return math.factorial(n)
        except ValueError as exc:
            logger.error("factorial error: %s (n=%s)", exc, n)
            raise

    def square(self, n):
        return n ** 2

    def cube(self, n):
        return n ** 3

    def square_root(self, n):
        try:
            return math.sqrt(n)
        except ValueError as exc:
            logger.error("square_root error: %s (n=%s)", exc, n)
            raise

    def cube_root(self, n):
        return math.cbrt(n)

    def power(self, base, exp):
        return base ** exp

    def log(self, n):
        try:
            return math.log10(n)
        except ValueError as exc:
            logger.error("log error: %s (n=%s)", exc, n)
            raise

    def ln(self, n):
        try:
            return math.log(n)
        except ValueError as exc:
            logger.error("ln error: %s (n=%s)", exc, n)
            raise

