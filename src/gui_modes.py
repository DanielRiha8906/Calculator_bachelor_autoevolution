"""Calculator mode abstractions for the GUI.

Defines the shared CalculatorMode base class and the concrete SimpleMode
and ScientificMode implementations.  Kept in a separate module so the
mode logic can be imported and tested independently of the tkinter GUI.
"""
from abc import ABC, abstractmethod


class CalculatorMode(ABC):
    """Abstract base class for calculator modes.

    Each mode exposes its human-readable name and the set of operations it
    supports.  The GUI uses this interface uniformly; adding a new mode
    requires only a new subclass — no changes to CalculatorGUI itself.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name shown in the mode selector."""

    @property
    @abstractmethod
    def operations(self) -> dict[str, tuple[str, int]]:
        """Ordered mapping of display label to (operation_name, arity).

        operation_name must be a valid method name on Calculator.
        arity is 1 for unary operations and 2 for binary operations.
        """


class SimpleMode(CalculatorMode):
    """Normal/Simple mode: basic arithmetic plus square and square root."""

    @property
    def name(self) -> str:
        return "Simple"

    @property
    def operations(self) -> dict[str, tuple[str, int]]:
        return {
            "Add":         ("add",         2),
            "Subtract":    ("subtract",    2),
            "Multiply":    ("multiply",    2),
            "Divide":      ("divide",      2),
            "Square":      ("square",      1),
            "Square Root": ("square_root", 1),
        }


class ScientificMode(CalculatorMode):
    """Scientific mode: all simple operations plus advanced functions."""

    @property
    def name(self) -> str:
        return "Scientific"

    @property
    def operations(self) -> dict[str, tuple[str, int]]:
        return {
            "Add":           ("add",         2),
            "Subtract":      ("subtract",    2),
            "Multiply":      ("multiply",    2),
            "Divide":        ("divide",      2),
            "Square":        ("square",      1),
            "Square Root":   ("square_root", 1),
            "Factorial":     ("factorial",   1),
            "Cube":          ("cube",        1),
            "Cube Root":     ("cube_root",   1),
            "Power":         ("power",       2),
            "Log (base 10)": ("log",         1),
            "Natural Log":   ("ln",          1),
            "Sin":           ("sin",         1),
            "Cos":           ("cos",         1),
            "Tan":           ("tan",         1),
            "Cot":           ("cot",         1),
            "Arcsin":        ("asin",        1),
            "Arccos":        ("acos",        1),
        }


def parse_number(raw: str):
    """Parse a string to int or float.

    Tries int first so that whole-number inputs are not widened to float.

    Args:
        raw: The string to parse.

    Returns:
        An int if the string represents a whole number, otherwise a float.

    Raises:
        ValueError: if the string cannot be parsed as a number.
    """
    try:
        return int(raw)
    except ValueError:
        return float(raw)
