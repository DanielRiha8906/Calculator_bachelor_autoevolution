"""Calculator class providing arithmetic and scientific operations.

The Calculator wraps the pure functions in the ``operations`` sub-package
with a stateful history log.  Every successful operation is recorded in an
internal list that can be retrieved via :meth:`get_history` or cleared via
:meth:`clear_history`.  Failed operations (those that raise an exception)
are *not* recorded.

Supported operations
--------------------
Basic arithmetic:
    add, subtract, multiply, divide

Scientific:
    factorial, square, cube, square_root, cube_root, power, log, ln
"""

from .operations import basic, scientific


class Calculator:
    """Stateful calculator with operation history.

    All arithmetic and scientific operations delegate to the pure functions
    in :mod:`src.operations.basic` and :mod:`src.operations.scientific`.
    The class itself is responsible only for history management; it does not
    catch or suppress any exceptions raised by those functions.

    Attributes:
        _history: Internal list of operation records.  Each record is a dict
            with keys ``operation`` (str), ``args`` (list), and
            ``result`` (numeric).
    """

    def __init__(self) -> None:
        """Initialise the calculator with an empty operation history."""
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

    # ------------------------------------------------------------------
    # Basic arithmetic
    # ------------------------------------------------------------------

    def add(self, a: float, b: float) -> float:
        """Return the sum of *a* and *b* and record the operation.

        Args:
            a: First operand.
            b: Second operand.

        Returns:
            a + b
        """
        result = basic.add(a, b)
        self._record("add", [a, b], result)
        return result

    def subtract(self, a: float, b: float) -> float:
        """Return *a* minus *b* and record the operation.

        Args:
            a: Minuend.
            b: Subtrahend.

        Returns:
            a - b
        """
        result = basic.subtract(a, b)
        self._record("subtract", [a, b], result)
        return result

    def multiply(self, a: float, b: float) -> float:
        """Return the product of *a* and *b* and record the operation.

        Args:
            a: First factor.
            b: Second factor.

        Returns:
            a * b
        """
        result = basic.multiply(a, b)
        self._record("multiply", [a, b], result)
        return result

    def divide(self, a: float, b: float) -> float:
        """Return *a* divided by *b* and record the operation.

        Args:
            a: Dividend.
            b: Divisor.

        Returns:
            a / b

        Raises:
            ZeroDivisionError: If *b* is zero.
        """
        result = basic.divide(a, b)
        self._record("divide", [a, b], result)
        return result

    # ------------------------------------------------------------------
    # Scientific operations
    # ------------------------------------------------------------------

    def factorial(self, n: int) -> int:
        """Return *n* factorial (*n*!) and record the operation.

        Args:
            n: Non-negative integer.

        Returns:
            n!

        Raises:
            ValueError: If *n* is negative.
            TypeError: If *n* is not an integer.
        """
        result = scientific.factorial(n)
        self._record("factorial", [n], result)
        return result

    def square(self, x: float) -> float:
        """Return *x* squared (*x* ** 2) and record the operation.

        Args:
            x: Input value.

        Returns:
            x ** 2
        """
        result = scientific.square(x)
        self._record("square", [x], result)
        return result

    def cube(self, x: float) -> float:
        """Return *x* cubed (*x* ** 3) and record the operation.

        Args:
            x: Input value.

        Returns:
            x ** 3
        """
        result = scientific.cube(x)
        self._record("cube", [x], result)
        return result

    def square_root(self, x: float) -> float:
        """Return the square root of *x* and record the operation.

        Args:
            x: Non-negative input value.

        Returns:
            sqrt(x)

        Raises:
            ValueError: If *x* is negative.
        """
        result = scientific.square_root(x)
        self._record("square_root", [x], result)
        return result

    def cube_root(self, x: float) -> float:
        """Return the real cube root of *x* and record the operation.

        Supports negative inputs (unlike :func:`math.sqrt`).

        Args:
            x: Input value.

        Returns:
            cbrt(x)
        """
        result = scientific.cube_root(x)
        self._record("cube_root", [x], result)
        return result

    def power(self, base: float, exp: float) -> float:
        """Return *base* raised to *exp* and record the operation.

        Args:
            base: The base value.
            exp: The exponent.

        Returns:
            base ** exp
        """
        result = scientific.power(base, exp)
        self._record("power", [base, exp], result)
        return result

    def log(self, x: float) -> float:
        """Return the base-10 logarithm of *x* and record the operation.

        Args:
            x: Positive input value.

        Returns:
            log10(x)

        Raises:
            ValueError: If *x* is zero or negative.
        """
        result = scientific.log(x)
        self._record("log", [x], result)
        return result

    def ln(self, x: float) -> float:
        """Return the natural logarithm of *x* and record the operation.

        Args:
            x: Positive input value.

        Returns:
            ln(x)

        Raises:
            ValueError: If *x* is zero or negative.
        """
        result = scientific.ln(x)
        self._record("ln", [x], result)
        return result
