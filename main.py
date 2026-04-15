"""Command-line interface for the Calculator.

Usage:
    python main.py <operation> <operand>              # unary operations
    python main.py <operation> <operand1> <operand2>  # binary operations

Examples:
    python main.py add 5 7
    python main.py factorial 5
    python main.py square_root 16

Supported operations:
    Binary (two operands): add, subtract, multiply, divide, power
    Unary  (one operand):  factorial, square, cube, square_root, cube_root, log, ln

Exit codes:
    0  — success
    1  — argument error or calculation error
"""

import sys

from src.session import CalculatorSession, ALL_OPS, BINARY_OPS
from src.error_logger import log_error

_USAGE = (
    "Usage: python main.py <operation> <operand> [operand2]\n"
    "  Binary ops (two operands): add, subtract, multiply, divide, power\n"
    "  Unary  ops (one operand):  factorial, square, cube, square_root, cube_root, log, ln"
)


def _parse_operand(value: str, require_int: bool = False):
    """Parse a string operand into a number.

    Args:
        value: The raw string from the command line.
        require_int: When True, the value must parse as a plain integer.

    Returns:
        An int when the string represents a whole number (or require_int is
        True); otherwise a float.

    Raises:
        ValueError: if the string cannot be parsed as the required type.
    """
    if require_int:
        return int(value)
    try:
        return int(value)
    except ValueError:
        return float(value)


def main(argv: list[str] | None = None) -> int:
    """Entry point for the command-line calculator.

    Args:
        argv: Argument list (defaults to sys.argv[1:]).

    Returns:
        Exit code: 0 on success, 1 on error.
    """
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        log_error("cli", "no arguments provided")
        print(_USAGE, file=sys.stderr)
        return 1

    operation = argv[0]

    if operation not in ALL_OPS:
        log_error("cli", f"unknown operation '{operation}'")
        print(f"Error: unknown operation '{operation}'.", file=sys.stderr)
        print(_USAGE, file=sys.stderr)
        return 1

    is_binary = operation in BINARY_OPS

    if is_binary:
        if len(argv) != 3:
            log_error("cli", f"'{operation}' requires two operands, got {len(argv) - 1}")
            print(
                f"Error: '{operation}' requires exactly two operands.",
                file=sys.stderr,
            )
            print(_USAGE, file=sys.stderr)
            return 1
    else:
        if len(argv) != 2:
            log_error("cli", f"'{operation}' requires one operand, got {len(argv) - 1}")
            print(
                f"Error: '{operation}' requires exactly one operand.",
                file=sys.stderr,
            )
            print(_USAGE, file=sys.stderr)
            return 1

    session = CalculatorSession()

    try:
        if is_binary:
            a = _parse_operand(argv[1])
            b = _parse_operand(argv[2])
            result = session.execute(operation, a, b)
        else:
            require_int = operation == "factorial"
            a = _parse_operand(argv[1], require_int=require_int)
            result = session.execute(operation, a)
    except (ValueError, TypeError, ZeroDivisionError) as exc:
        log_error("cli", f"error in '{operation}': {exc}")
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
