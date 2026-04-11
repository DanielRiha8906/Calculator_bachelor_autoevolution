"""Calculator controller: routes operation requests to the Calculator.

Separates computation dispatch from user interaction and argument parsing.
Both the interactive mode (``src/__main__.py``) and the CLI (``src/cli.py``)
use :class:`CalculatorController` as the single dispatch point, so each UI
layer focuses only on how to collect and present data — not which
:class:`~src.calculator.Calculator` method to call.
"""

from .calculator import Calculator

#: Maps interactive-mode choice strings (``"1"``–``"12"``) to canonical
#: operation names used by :meth:`CalculatorController.execute`.
CHOICE_TO_OPERATION: dict[str, str] = {
    "1": "add",
    "2": "subtract",
    "3": "multiply",
    "4": "divide",
    "5": "factorial",
    "6": "square",
    "7": "cube",
    "8": "square_root",
    "9": "cube_root",
    "10": "power",
    "11": "log",
    "12": "ln",
}


class CalculatorController:
    """Routes named operations to the Calculator and returns string results.

    Serves as the bridge between user interfaces (interactive mode, CLI)
    and the :class:`~src.calculator.Calculator` computation layer.  Each UI
    layer is responsible only for collecting operands and displaying results;
    all dispatch logic lives here.
    """

    def __init__(self) -> None:
        self._calc = Calculator()

    def execute(
        self,
        operation: str,
        a: "float | int | None" = None,
        b: "float | None" = None,
        base: float = 10.0,
    ) -> str:
        """Execute a named calculator operation and return the result.

        Args:
            operation: Canonical operation name (e.g. ``"add"``, ``"divide"``).
            a: Primary operand (required by most operations).
            b: Secondary operand (used by binary operations such as ``"add"``
                and ``"power"``).
            base: Logarithm base, used only for ``"log"`` (default ``10``).

        Returns:
            Computation result formatted as a string.

        Raises:
            ValueError: For invalid inputs (e.g. negative factorial, non-positive
                logarithm argument).
            ZeroDivisionError: When dividing by zero.
        """
        ops = {
            "add": lambda: self._calc.add(a, b),
            "subtract": lambda: self._calc.subtract(a, b),
            "multiply": lambda: self._calc.multiply(a, b),
            "divide": lambda: self._calc.divide(a, b),
            "factorial": lambda: self._calc.factorial(a),
            "square": lambda: self._calc.square(a),
            "cube": lambda: self._calc.cube(a),
            "square_root": lambda: self._calc.square_root(a),
            "cube_root": lambda: self._calc.cube_root(a),
            "power": lambda: self._calc.power(a, b),
            "log": lambda: self._calc.log(a, base),
            "ln": lambda: self._calc.ln(a),
        }
        if operation not in ops:
            raise ValueError(f"Unknown operation: {operation!r}")
        result = ops[operation]()
        return str(result)
