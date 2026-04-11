"""Command-line interface (bash mode) for the Calculator.

Allows single-shot calculator operations to be executed directly from
the shell without entering the interactive REPL:

    python -m src add 3 5
    python -m src factorial 5
    python -m src square_root 16

A ``--mode`` flag controls which operations are accepted:

* ``--mode normal``     — only basic arithmetic (add, subtract, multiply, divide).
* ``--mode scientific`` — all operations, including scientific ones (default).
"""

import argparse
import logging
import sys

from .calculator import Calculator

logger = logging.getLogger(__name__)


TWO_ARG_OPS = {"add", "subtract", "multiply", "divide", "power"}
INT_OPS = {"factorial"}
BASIC_OPS = {"add", "subtract", "multiply", "divide"}
VALID_OPS = {
    "add",
    "subtract",
    "multiply",
    "divide",
    "factorial",
    "square",
    "cube",
    "square_root",
    "cube_root",
    "power",
    "log",
    "ln",
}


def _build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser for CLI mode."""
    parser = argparse.ArgumentParser(
        prog="python -m src",
        description="Calculator - Bash CLI Mode",
        epilog="Run without arguments to enter interactive mode.",
    )
    parser.add_argument(
        "--mode",
        choices=["normal", "scientific"],
        default="scientific",
        help=(
            "Calculator mode. "
            "'normal' restricts to basic operations (add, subtract, multiply, divide). "
            "'scientific' allows all operations (default)."
        ),
    )
    parser.add_argument(
        "operation",
        choices=sorted(VALID_OPS),
        metavar="OPERATION",
        help=(
            "Operation to perform. One of: "
            + ", ".join(sorted(VALID_OPS))
        ),
    )
    parser.add_argument(
        "operands",
        nargs="+",
        metavar="NUMBER",
        help=(
            "Operand(s) for the operation. "
            "Two-argument operations (add, subtract, multiply, divide, power) "
            "require two values. All others require one value. "
            "factorial requires an integer."
        ),
    )
    return parser


def cli_mode(argv: list[str] | None = None) -> int:
    """Execute a single calculator operation from command-line arguments.

    Args:
        argv: Argument list to parse. Defaults to sys.argv[1:].

    Returns:
        Exit code: 0 on success, 1 on error.
    """
    parser = _build_parser()
    args = parser.parse_args(argv)

    op = args.operation
    mode = args.mode
    operands_str: list[str] = args.operands

    # Enforce mode restriction before executing the operation.
    if mode == "normal" and op not in BASIC_OPS:
        msg = f"'{op}' is not available in normal mode. Use --mode scientific to enable it."
        logger.error(msg)
        print(f"Error: {msg}", file=sys.stderr)
        return 1

    calc = Calculator()

    try:
        if op in INT_OPS:
            if len(operands_str) != 1:
                msg = f"'{op}' requires exactly 1 integer operand."
                logger.error(msg)
                print(f"Error: {msg}", file=sys.stderr)
                return 1
            a = int(operands_str[0])
            result = getattr(calc, op)(a)
        elif op in TWO_ARG_OPS:
            if len(operands_str) != 2:
                msg = f"'{op}' requires exactly 2 operands."
                logger.error(msg)
                print(f"Error: {msg}", file=sys.stderr)
                return 1
            a = float(operands_str[0])
            b = float(operands_str[1])
            result = getattr(calc, op)(a, b)
        else:
            if len(operands_str) != 1:
                msg = f"'{op}' requires exactly 1 operand."
                logger.error(msg)
                print(f"Error: {msg}", file=sys.stderr)
                return 1
            a = float(operands_str[0])
            result = getattr(calc, op)(a)

        print(result)
        return 0

    except (ValueError, ZeroDivisionError, TypeError) as e:
        logger.error("cli operation '%s' failed: %s", op, e)
        print(f"Error: {e}", file=sys.stderr)
        return 1
