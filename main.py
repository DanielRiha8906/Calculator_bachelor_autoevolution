"""Command-line interface for the Calculator.

Allows the calculator to be used from bash by passing the operation and
operand values as command-line arguments.

Usage:
    python main.py <operation> [operand1] [operand2]

Operations requiring one operand:
    factorial, square, cube, sqrt, cbrt, log10, ln

Operations requiring two operands:
    add, subtract, multiply, divide, power

Examples:
    python main.py add 5 7
    python main.py factorial 5
    python main.py divide 10 2
    python main.py sqrt 9
"""
import sys

from src.calculator import Calculator
from src.error_logger import get_error_logger, setup_error_logging

# Maps operation name -> (method_name, arity)
CLI_OPERATIONS = {
    "add":       ("add",       2),
    "subtract":  ("subtract",  2),
    "multiply":  ("multiply",  2),
    "divide":    ("divide",    2),
    "factorial": ("factorial", 1),
    "square":    ("square",    1),
    "cube":      ("cube",      1),
    "sqrt":      ("sqrt",      1),
    "cbrt":      ("cbrt",      1),
    "power":     ("power",     2),
    "log10":     ("log10",     1),
    "ln":        ("ln",        1),
}

USAGE = """\
Usage: python main.py <operation> [operand1] [operand2]

Operations (one operand):  factorial, square, cube, sqrt, cbrt, log10, ln
Operations (two operands): add, subtract, multiply, divide, power

Examples:
    python main.py add 5 7
    python main.py factorial 5
"""


def _parse_operand(value: str, require_int: bool = False) -> int | float:
    """Parse a command-line operand string into a number.

    Args:
        value: The string value to parse.
        require_int: When True, parse strictly as an integer and raise
            ValueError for non-integer strings such as "3.5".

    Returns:
        int if the value represents a whole number or require_int is True,
        float otherwise.

    Raises:
        ValueError: if the string cannot be parsed as the required type.
    """
    if require_int:
        try:
            return int(value)
        except ValueError:
            raise ValueError(f"'{value}' is not a valid integer")
    try:
        return int(value)
    except ValueError:
        return float(value)


class CLIHandler:
    """Handles CLI-based calculator operation execution.

    Separates argument validation, operation dispatch, and output formatting
    from the Calculator core so CLI concerns are isolated from calculation logic.
    """

    def __init__(self, calc: Calculator | None = None) -> None:
        """Initialise the handler with an optional Calculator instance.

        Args:
            calc: Calculator to use for operations.  A new instance is created
                  when None is passed.
        """
        self._calc = calc if calc is not None else Calculator()

    def run(self, argv: list[str]) -> None:
        """Parse argv, execute the requested operation, and print the result.

        Prints results to stdout and errors to stderr.  Exits with code 1 on
        any failure.

        Args:
            argv: Argument list excluding the program name.
        """
        logger = get_error_logger()

        if not argv:
            logger.error("[cli] missing required operation argument")
            print(USAGE, end="", file=sys.stderr)
            sys.exit(1)

        operation = argv[0]

        if operation not in CLI_OPERATIONS:
            logger.error("[cli] unknown operation: %s", operation)
            print(f"Error: unknown operation '{operation}'", file=sys.stderr)
            print(USAGE, end="", file=sys.stderr)
            sys.exit(1)

        method_name, arity = CLI_OPERATIONS[operation]
        expected_total = arity + 1  # operation name + operands
        if len(argv) != expected_total:
            operand_word = "operand" if arity == 1 else "operands"
            logger.error(
                "[cli] incorrect argument count for '%s': expected %d, got %d",
                operation, arity, len(argv) - 1,
            )
            print(
                f"Error: '{operation}' requires {arity} {operand_word}.",
                file=sys.stderr,
            )
            print(USAGE, end="", file=sys.stderr)
            sys.exit(1)

        require_int = operation == "factorial"
        try:
            operands = [_parse_operand(v, require_int=require_int) for v in argv[1:]]
        except ValueError as exc:
            logger.error("[cli] invalid operand for '%s': %s", operation, exc)
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)

        method = getattr(self._calc, method_name)
        try:
            result = method(*operands)
            print(result)
        except (ValueError, TypeError, ZeroDivisionError) as exc:
            logger.error("[cli] calculation error in %s: %s", operation, exc)
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)


def main(argv: list[str] | None = None) -> None:
    """Entry point for the bash CLI.

    Parses command-line arguments, invokes the appropriate Calculator method,
    and prints the result to stdout.  Errors are written to stderr and the
    process exits with code 1.

    Args:
        argv: Argument list (excluding the program name).
            Defaults to sys.argv[1:] when None.
    """
    if argv is None:
        argv = sys.argv[1:]
    setup_error_logging()
    CLIHandler().run(argv)


if __name__ == "__main__":
    main()
