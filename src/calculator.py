"""Core calculator module.

Provides the Calculator class and operation-classification constants.
All operation implementations live in the src.operations sub-package;
this module owns the cross-cutting concerns: history recording, error
logging, and operand type coercion.
"""
import logging

from .operations import arithmetic, advanced, scientific

logger = logging.getLogger(__name__)

UNARY_OPS = {"factorial", "square", "cube", "square_root", "cube_root", "log", "ln"}
BINARY_OPS = {"add", "subtract", "multiply", "divide", "power"}
# Operations that require integer operands
INTEGER_OPS = {"factorial"}
# Scientific mode unary operations (angles in radians)
SCIENTIFIC_UNARY_OPS = {"sin", "cos", "tan", "asin", "acos", "atan", "sinh", "cosh", "tanh", "exp"}


def _to_int_if_needed(op: str, value: float) -> "float | int":
    """Convert value to int for operations that require integer operands."""
    if op not in INTEGER_OPS:
        return value
    if value != int(value):
        raise ValueError(f"{op} requires a whole number, got {value}")
    return int(value)


class Calculator:
    """A calculator with per-instance operation history.

    Supports 12 operations across two arity groups:
    - Binary (two operands): add, subtract, multiply, divide, power
    - Unary (one operand): factorial, square, cube, square_root, cube_root,
      log (base-10), ln (natural log)

    Use :meth:`execute` to dispatch operations by name, which also records
    each successful call in the instance history.  Individual methods can
    be called directly but do not record history themselves.
    """

    def __init__(self):
        """Initialise the Calculator with an empty operation history."""
        self.history: list[dict] = []

    def get_history(self) -> list[dict]:
        """Return a copy of the operation history list."""
        return list(self.history)

    def add(self, a, b):
        """Return the sum of a and b."""
        return arithmetic.add(a, b)

    def subtract(self, a, b):
        """Return a minus b."""
        return arithmetic.subtract(a, b)

    def multiply(self, a, b):
        """Return the product of a and b."""
        return arithmetic.multiply(a, b)

    def divide(self, a, b):
        """Return a divided by b. Raises ZeroDivisionError if b is zero."""
        try:
            return arithmetic.divide(a, b)
        except ZeroDivisionError:
            logger.error("divide error: division by zero (a=%s, b=%s)", a, b)
            raise

    def factorial(self, n):
        """Return n factorial (n!). Raises ValueError for negative n."""
        try:
            return advanced.factorial(n)
        except ValueError as exc:
            logger.error("factorial error: %s (n=%s)", exc, n)
            raise

    def square(self, n):
        """Return n squared (n ** 2)."""
        return advanced.square(n)

    def cube(self, n):
        """Return n cubed (n ** 3)."""
        return advanced.cube(n)

    def square_root(self, n):
        """Return the square root of n. Raises ValueError for negative n."""
        try:
            return advanced.square_root(n)
        except ValueError as exc:
            logger.error("square_root error: %s (n=%s)", exc, n)
            raise

    def cube_root(self, n):
        """Return the cube root of n. Handles negative inputs (requires Python 3.11+)."""
        return advanced.cube_root(n)

    def power(self, base, exp):
        """Return base raised to the power exp."""
        return advanced.power(base, exp)

    def log(self, n):
        """Return the base-10 logarithm of n. Raises ValueError for n <= 0."""
        try:
            return advanced.log(n)
        except ValueError as exc:
            logger.error("log error: %s (n=%s)", exc, n)
            raise

    def ln(self, n):
        """Return the natural logarithm of n. Raises ValueError for n <= 0."""
        try:
            return advanced.ln(n)
        except ValueError as exc:
            logger.error("ln error: %s (n=%s)", exc, n)
            raise

    def sin(self, x):
        """Return the sine of x (x in radians)."""
        return scientific.sin(x)

    def cos(self, x):
        """Return the cosine of x (x in radians)."""
        return scientific.cos(x)

    def tan(self, x):
        """Return the tangent of x (x in radians)."""
        return scientific.tan(x)

    def asin(self, x):
        """Return the arcsine of x in radians. Raises ValueError for |x| > 1."""
        try:
            return scientific.asin(x)
        except ValueError as exc:
            logger.error("asin error: %s (x=%s)", exc, x)
            raise

    def acos(self, x):
        """Return the arccosine of x in radians. Raises ValueError for |x| > 1."""
        try:
            return scientific.acos(x)
        except ValueError as exc:
            logger.error("acos error: %s (x=%s)", exc, x)
            raise

    def atan(self, x):
        """Return the arctangent of x in radians."""
        return scientific.atan(x)

    def sinh(self, x):
        """Return the hyperbolic sine of x."""
        return scientific.sinh(x)

    def cosh(self, x):
        """Return the hyperbolic cosine of x."""
        return scientific.cosh(x)

    def tanh(self, x):
        """Return the hyperbolic tangent of x."""
        return scientific.tanh(x)

    def exp(self, x):
        """Return e raised to the power x."""
        return scientific.exp(x)

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
        elif op in SCIENTIFIC_UNARY_OPS:
            a = operands[0]
            result = getattr(self, op)(a)
            self.history.append({"op": op, "operands": (a,), "result": result})
        else:
            raise ValueError(f"Unknown operation: {op!r}")
        return result
