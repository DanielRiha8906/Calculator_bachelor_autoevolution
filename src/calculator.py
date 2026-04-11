import logging
import math

logger = logging.getLogger(__name__)


class Calculator:
    def __init__(self):
        self._history: list[dict] = []

    def _record(self, operation: str, args: list, result) -> None:
        """Append a successful operation to the history list."""
        self._history.append({"operation": operation, "args": args, "result": result})

    def get_history(self) -> list[dict]:
        """Return a copy of the operation history."""
        return list(self._history)

    def clear_history(self) -> None:
        """Clear all recorded history entries."""
        self._history.clear()

    def add(self, a, b):
        try:
            result = a + b
        except TypeError as e:
            logger.error("add(%r, %r) failed: %s", a, b, e)
            raise
        self._record("add", [a, b], result)
        return result

    def subtract(self, a, b):
        try:
            result = a - b
        except TypeError as e:
            logger.error("subtract(%r, %r) failed: %s", a, b, e)
            raise
        self._record("subtract", [a, b], result)
        return result

    def multiply(self, a, b):
        try:
            result = a * b
        except TypeError as e:
            logger.error("multiply(%r, %r) failed: %s", a, b, e)
            raise
        self._record("multiply", [a, b], result)
        return result

    def divide(self, a, b):
        try:
            result = a / b
        except (ZeroDivisionError, TypeError) as e:
            logger.error("divide(%r, %r) failed: %s", a, b, e)
            raise
        self._record("divide", [a, b], result)
        return result

    def factorial(self, n: int) -> int:
        try:
            result = math.factorial(n)
        except (ValueError, TypeError) as e:
            logger.error("factorial(%r) failed: %s", n, e)
            raise
        self._record("factorial", [n], result)
        return result

    def square(self, x: float) -> float:
        try:
            result = x ** 2
        except TypeError as e:
            logger.error("square(%r) failed: %s", x, e)
            raise
        self._record("square", [x], result)
        return result

    def cube(self, x: float) -> float:
        try:
            result = x ** 3
        except TypeError as e:
            logger.error("cube(%r) failed: %s", x, e)
            raise
        self._record("cube", [x], result)
        return result

    def square_root(self, x: float) -> float:
        try:
            result = math.sqrt(x)
        except (ValueError, TypeError) as e:
            logger.error("square_root(%r) failed: %s", x, e)
            raise
        self._record("square_root", [x], result)
        return result

    def cube_root(self, x: float) -> float:
        try:
            result = math.cbrt(x)
        except TypeError as e:
            logger.error("cube_root(%r) failed: %s", x, e)
            raise
        self._record("cube_root", [x], result)
        return result

    def power(self, base: float, exp: float) -> float:
        try:
            result = math.pow(base, exp)
        except (ValueError, TypeError) as e:
            logger.error("power(%r, %r) failed: %s", base, exp, e)
            raise
        self._record("power", [base, exp], result)
        return result

    def log(self, x: float) -> float:
        try:
            result = math.log10(x)
        except (ValueError, TypeError) as e:
            logger.error("log(%r) failed: %s", x, e)
            raise
        self._record("log", [x], result)
        return result

    def ln(self, x: float) -> float:
        try:
            result = math.log(x)
        except (ValueError, TypeError) as e:
            logger.error("ln(%r) failed: %s", x, e)
            raise
        self._record("ln", [x], result)
        return result
