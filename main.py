"""Command-line entry point for the Calculator.

Supports two modes:
    Bash mode    — pass operation and operand(s) as arguments:
                     python main.py add 5 7
                     python main.py factorial 5
    Interactive  — run without arguments to start the menu-driven session:
                     python main.py
"""
import sys

from src.calculator import Calculator
from src.__main__ import main as interactive_main

# Maps CLI operation name to (operand_count, calculator_method_name).
CLI_OPERATIONS: dict[str, tuple[int, str]] = {
    "add":         (2, "add"),
    "subtract":    (2, "subtract"),
    "multiply":    (2, "multiply"),
    "divide":      (2, "divide"),
    "power":       (2, "power"),
    "factorial":   (1, "factorial"),
    "square":      (1, "square"),
    "cube":        (1, "cube"),
    "square_root": (1, "square_root"),
    "cube_root":   (1, "cube_root"),
    "log":         (1, "log"),
    "ln":          (1, "ln"),
}


def _parse_operand(raw: str) -> float:
    """Parse *raw* as a float; exit with code 1 on failure."""
    try:
        return float(raw)
    except ValueError:
        print(f"Error: '{raw}' is not a valid number.", file=sys.stderr)
        sys.exit(1)


def run_cli(args: list[str]) -> None:
    """Execute one calculator operation from *args* (operation + operands).

    Prints the result to stdout.  Prints error messages to stderr and calls
    ``sys.exit(1)`` for any invalid input or math error.
    """
    operation = args[0].lower()

    if operation not in CLI_OPERATIONS:
        known = ", ".join(sorted(CLI_OPERATIONS))
        print(
            f"Error: unknown operation '{operation}'.\n"
            f"Available operations: {known}",
            file=sys.stderr,
        )
        sys.exit(1)

    operand_count, method_name = CLI_OPERATIONS[operation]
    expected_total = 1 + operand_count  # operation name + operand values

    if len(args) != expected_total:
        print(
            f"Error: '{operation}' requires {operand_count} operand(s), "
            f"got {len(args) - 1}.",
            file=sys.stderr,
        )
        sys.exit(1)

    calc = Calculator()

    try:
        if operand_count == 2:
            a = _parse_operand(args[1])
            b = _parse_operand(args[2])
            result = getattr(calc, method_name)(a, b)
        else:
            a = _parse_operand(args[1])
            if method_name == "factorial":
                if a != int(a):
                    print(
                        "Error: factorial requires a whole number.",
                        file=sys.stderr,
                    )
                    sys.exit(1)
                result = calc.factorial(int(a))
            else:
                result = getattr(calc, method_name)(a)
    except (ValueError, ZeroDivisionError, TypeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(result)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_cli(sys.argv[1:])
    else:
        interactive_main()
