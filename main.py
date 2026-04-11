"""Command-line interface entry point for the Calculator.

All CLI logic lives in src.cli; this module is a thin wrapper that provides
the conventional ``python main.py`` entry point and keeps the project layout
consistent with standard Python packaging conventions.

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

from src.cli import CLIHandler
from src.error_logger import setup_error_logging


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
