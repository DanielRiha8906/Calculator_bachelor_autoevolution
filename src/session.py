"""CalculatorSession: operation dispatch and session history management.

Separates computation and session state from interface concerns so the
calculator operations can be reused independently of how the user
interacts with the application (interactive menu, CLI arguments, etc.).
"""
from .calculator import Calculator

# Shared operation arity metadata.  Both the interactive CLI and the bash
# CLI import from here so that the sets are defined in exactly one place.
BINARY_OPS: frozenset[str] = frozenset(
    {"add", "subtract", "multiply", "divide", "power"}
)
UNARY_OPS: frozenset[str] = frozenset(
    {"factorial", "square", "cube", "square_root", "cube_root", "log", "ln"}
)
ALL_OPS: frozenset[str] = BINARY_OPS | UNARY_OPS


class CalculatorSession:
    """Manages calculator operations and records session history.

    Decouples computation and history tracking from any specific user
    interface.  Clients call :meth:`execute` to run operations and
    :meth:`save` to persist history to disk.

    Example::

        session = CalculatorSession()
        result = session.execute("add", 2, 3)   # 5
        session.save("history.txt")
    """

    def __init__(self) -> None:
        self._calc = Calculator()
        self._history: list[str] = []

    def execute(self, name: str, *args):
        """Dispatch a named operation and append the result to history.

        Args:
            name: Operation name (e.g. ``"add"``, ``"factorial"``).
            *args: Operands to pass to the operation.

        Returns:
            The numeric result of the operation.

        Raises:
            ValueError: for domain errors (negative sqrt, log of zero, etc.).
            TypeError: for type errors (e.g. float passed to factorial).
            ZeroDivisionError: when dividing by zero.
        """
        method = getattr(self._calc, name)
        result = method(*args)
        self._history.append(self.format_entry(name, args, result))
        return result

    @staticmethod
    def format_entry(name: str, args: tuple, result) -> str:
        """Format a completed calculation as a function-style string.

        Args:
            name: Operation name.
            args: Operand tuple.
            result: Computed result.

        Returns:
            A string like ``"add(2, 3) = 5"``.
        """
        args_str = ", ".join(str(a) for a in args)
        return f"{name}({args_str}) = {result}"

    def history(self) -> list[str]:
        """Return a copy of the current session history list."""
        return list(self._history)

    def save(self, path: str) -> None:
        """Write session history to *path*, overwriting any previous content.

        Args:
            path: Destination file path.
        """
        with open(path, "w", encoding="utf-8") as fh:
            for entry in self._history:
                fh.write(entry + "\n")
