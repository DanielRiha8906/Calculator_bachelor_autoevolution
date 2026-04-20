"""GUI mode abstractions for the calculator.

Provides a shared base class (CalculatorMode) and two concrete implementations
(SimpleMode and ScientificMode) so the GUI layer can handle both modes through
a common interface while keeping their operation sets separate.

Each mode exposes an ordered list of OperationSpec objects that describe how
the GUI should label inputs and which Calculator method to invoke.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class OperationSpec:
    """Specification for a single calculator operation in the GUI.

    Attributes:
        name: Human-readable display name shown in the operation selector.
        method: Name of the corresponding method on Calculator.
        arity: Number of operands (1 for unary, 2 for binary).
        label_a: Label text for the first operand input field.
        label_b: Label text for the second operand input field (arity == 2 only).
        require_int: When True the first operand must be a whole integer (e.g. factorial).
    """

    name: str
    method: str
    arity: int
    label_a: str = "Value"
    label_b: str = ""
    require_int: bool = False


def parse_number(text: str, *, require_int: bool = False) -> int | float:
    """Parse a text string into a numeric value.

    Args:
        text: Raw string from an input field.
        require_int: When True the value must represent a whole integer.
            A string like "5.0" is accepted but "3.5" is not.

    Returns:
        int when the value is a whole number, float otherwise.

    Raises:
        ValueError: If the text is empty, non-numeric, or fails the
            require_int constraint.
    """
    text = text.strip()
    if not text:
        raise ValueError("Input field is empty")
    if require_int:
        val = float(text)
        if val != int(val):
            raise ValueError(f"Expected a whole number, got '{text}'")
        return int(val)
    try:
        return int(text)
    except ValueError:
        return float(text)


class CalculatorMode(ABC):
    """Abstract base for a calculator GUI mode.

    Each concrete mode defines a display name and an ordered list of
    OperationSpec objects.  The GUI uses these to populate the operation
    selector and to render the correct input fields for the chosen operation.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the human-readable name of this mode."""

    @property
    @abstractmethod
    def operations(self) -> list[OperationSpec]:
        """Return the ordered list of operations available in this mode."""


class SimpleMode(CalculatorMode):
    """Basic arithmetic mode: the standard four operations plus square and square root."""

    @property
    def name(self) -> str:
        return "Simple"

    @property
    def operations(self) -> list[OperationSpec]:
        return [
            OperationSpec("Add", "add", 2, "a", "b"),
            OperationSpec("Subtract", "subtract", 2, "a", "b"),
            OperationSpec("Multiply", "multiply", 2, "a", "b"),
            OperationSpec("Divide", "divide", 2, "a", "b"),
            OperationSpec("Square", "square", 1),
            OperationSpec("Square Root", "sqrt", 1),
        ]


class ScientificMode(CalculatorMode):
    """Scientific mode: powers, roots, logarithms, factorial, and trig functions."""

    @property
    def name(self) -> str:
        return "Scientific"

    @property
    def operations(self) -> list[OperationSpec]:
        return [
            OperationSpec("Power", "power", 2, "Base", "Exponent"),
            OperationSpec("Cube", "cube", 1),
            OperationSpec("Cube Root", "cbrt", 1),
            OperationSpec("Factorial", "factorial", 1, "n (integer)", require_int=True),
            OperationSpec("Log\u2081\u2080", "log10", 1),
            OperationSpec("Ln", "ln", 1),
            OperationSpec("Sin", "sin", 1, "Angle (degrees)"),
            OperationSpec("Cos", "cos", 1, "Angle (degrees)"),
            OperationSpec("Tan", "tan", 1, "Angle (degrees)"),
            OperationSpec("Cot", "cot", 1, "Angle (degrees)"),
            OperationSpec("Arcsin", "asin", 1, "Value \u2208 [-1, 1]"),
            OperationSpec("Arccos", "acos", 1, "Value \u2208 [-1, 1]"),
        ]
