import logging

from .operations import arithmetic, advanced

logger = logging.getLogger(__name__)

UNARY_OPS = {"factorial", "square", "cube", "square_root", "cube_root", "log", "ln"}
BINARY_OPS = {"add", "subtract", "multiply", "divide", "power"}
# Operations that require integer operands
INTEGER_OPS = {"factorial"}


def _to_int_if_needed(op: str, value: float) -> "float | int":
    """Convert value to int for operations that require integer operands."""
    if op not in INTEGER_OPS:
        return value
    if value != int(value):
        raise ValueError(f"{op} requires a whole number, got {value}")
    return int(value)


class Calculator:
    def __init__(self):
        self.history: list[dict] = []

    def get_history(self) -> list[dict]:
        """Return a copy of the operation history list."""
        return list(self.history)

    def add(self, a, b):
        return arithmetic.add(a, b)

    def subtract(self, a, b):
        return arithmetic.subtract(a, b)

    def multiply(self, a, b):
        return arithmetic.multiply(a, b)

    def divide(self, a, b):
        try:
            return arithmetic.divide(a, b)
        except ZeroDivisionError:
            logger.error("divide error: division by zero (a=%s, b=%s)", a, b)
            raise

    def factorial(self, n):
        try:
            return advanced.factorial(n)
        except ValueError as exc:
            logger.error("factorial error: %s (n=%s)", exc, n)
            raise

    def square(self, n):
        return advanced.square(n)

    def cube(self, n):
        return advanced.cube(n)

    def square_root(self, n):
        try:
            return advanced.square_root(n)
        except ValueError as exc:
            logger.error("square_root error: %s (n=%s)", exc, n)
            raise

    def cube_root(self, n):
        return advanced.cube_root(n)

    def power(self, base, exp):
        return advanced.power(base, exp)

    def log(self, n):
        try:
            return advanced.log(n)
        except ValueError as exc:
            logger.error("log error: %s (n=%s)", exc, n)
            raise

    def ln(self, n):
        try:
            return advanced.ln(n)
        except ValueError as exc:
            logger.error("ln error: %s (n=%s)", exc, n)
            raise

    def execute(self, op: str, *operands: "float | int") -> "float | int":
        """Dispatch an operation by name, record it in history on success, and return the result.

        Raises ValueError for unknown operations or invalid operand types.
        Propagates ZeroDivisionError or ValueError from the underlying method unchanged.
        """
        if op in BINARY_OPS:
            a, b = operands
            result = getattr(self, op)(a, b)
            self.history.append({"op": op, "operands": (a, b), "result": result})
        elif op in UNARY_OPS:
            a = _to_int_if_needed(op, operands[0])
            result = getattr(self, op)(a)
            self.history.append({"op": op, "operands": (a,), "result": result})
        else:
            raise ValueError(f"Unknown operation: {op!r}")
        return result
