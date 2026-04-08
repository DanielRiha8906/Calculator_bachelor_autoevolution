import logging
import math

logger = logging.getLogger(__name__)


class Calculator:
    def __init__(self):
        self._history: list[dict] = []

    def _record(self, operation: str, operands: tuple, result) -> None:
        """Append a successful operation to the history log."""
        self._history.append({"operation": operation, "operands": operands, "result": result})

    def get_history(self) -> list[dict]:
        """Return a copy of the operation history list.

        Each entry is a dict with keys: 'operation', 'operands', 'result'.
        Only successful operations are recorded; failed ones are omitted.
        """
        return list(self._history)

    def clear_history(self) -> None:
        """Clear the operation history."""
        self._history.clear()

    def add(self, a, b):
        result = a + b
        self._record("add", (a, b), result)
        return result

    def subtract(self, a, b):
        result = a - b
        self._record("subtract", (a, b), result)
        return result

    def multiply(self, a, b):
        result = a * b
        self._record("multiply", (a, b), result)
        return result

    def divide(self, a, b):
        if b == 0:
            logger.error("divide called with b=0 (a=%s)", a)
            raise ValueError("Division by zero is not allowed")
        result = a / b
        self._record("divide", (a, b), result)
        return result

    def factorial(self, n: int) -> int:
        if not isinstance(n, int):
            logger.error("factorial called with non-integer argument (n=%s, type=%s)", n, type(n).__name__)
            raise TypeError("Factorial is only defined for integers")
        if n < 0:
            logger.error("factorial called with negative argument (n=%s)", n)
            raise ValueError("Factorial is not defined for negative numbers")
        result = 1
        for i in range(2, n + 1):
            result *= i
        self._record("factorial", (n,), result)
        return result

    def square(self, x):
        result = x ** 2
        self._record("square", (x,), result)
        return result

    def cube(self, x):
        result = x ** 3
        self._record("cube", (x,), result)
        return result

    def square_root(self, x):
        if x < 0:
            logger.error("square_root called with negative argument (x=%s)", x)
            raise ValueError("Square root is not defined for negative numbers")
        result = math.sqrt(x)
        self._record("square_root", (x,), result)
        return result

    def cube_root(self, x):
        result = math.copysign(abs(x) ** (1 / 3), x)
        self._record("cube_root", (x,), result)
        return result

    def power(self, base, exp):
        result = base ** exp
        self._record("power", (base, exp), result)
        return result

    def log(self, x):
        if x <= 0:
            logger.error("log called with non-positive argument (x=%s)", x)
            raise ValueError("Logarithm is not defined for non-positive numbers")
        result = math.log10(x)
        self._record("log", (x,), result)
        return result

    def ln(self, x):
        if x <= 0:
            logger.error("ln called with non-positive argument (x=%s)", x)
            raise ValueError("Natural logarithm is not defined for non-positive numbers")
        result = math.log(x)
        self._record("ln", (x,), result)
        return result
