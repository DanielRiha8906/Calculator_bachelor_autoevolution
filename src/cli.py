"""Bash CLI mode for the Calculator.

Allows the calculator to be invoked directly from the terminal by passing
the operation and required values as command-line arguments:

    python -m src add 5 3
    python -m src factorial 5
    python -m src log 100
    python -m src log 8 --base 2
    python -m src sqrt 9

On success the result is printed to stdout and the process exits with
code 0.  On error (invalid input, domain error) the error message is
printed to stderr and the process exits with code 1.
"""
import argparse
import sys

from .controller import CalculatorController
from .error_logger import get_error_logger


def build_parser() -> argparse.ArgumentParser:
    """Create and return the argument parser for bash CLI mode."""
    parser = argparse.ArgumentParser(
        prog="python -m src",
        description="Calculator — perform a single operation and print the result.",
    )
    subparsers = parser.add_subparsers(dest="operation", metavar="OPERATION")
    subparsers.required = True

    # Two-operand arithmetic
    for name, help_text in [
        ("add", "Add two numbers (a + b)"),
        ("subtract", "Subtract b from a (a - b)"),
        ("multiply", "Multiply two numbers (a * b)"),
        ("divide", "Divide a by b (a / b)"),
    ]:
        sub = subparsers.add_parser(name, help=help_text)
        sub.add_argument("a", type=float, help="First number")
        sub.add_argument("b", type=float, help="Second number")

    # Power — two-operand with distinct names
    power_sub = subparsers.add_parser("power", help="Raise base to the power of exp (base ^ exp)")
    power_sub.add_argument("base", type=float, help="Base value")
    power_sub.add_argument("exp", type=float, help="Exponent value")

    # Single-operand operations
    for name, help_text in [
        ("square", "Square a number (a ^ 2)"),
        ("cube", "Cube a number (a ^ 3)"),
        ("sqrt", "Square root of a number"),
        ("cbrt", "Cube root of a number"),
        ("ln", "Natural logarithm of a number"),
    ]:
        sub = subparsers.add_parser(name, help=help_text)
        sub.add_argument("a", type=float, help="Input value")

    # Log — one required arg plus optional base flag
    log_sub = subparsers.add_parser("log", help="Logarithm of a (default base 10)")
    log_sub.add_argument("a", type=float, help="Input value")
    log_sub.add_argument("--base", type=float, default=10.0, help="Logarithm base (default: 10)")

    # Factorial — integer argument
    fact_sub = subparsers.add_parser("factorial", help="Factorial of a non-negative integer (n!)")
    fact_sub.add_argument("n", type=int, help="Non-negative integer")

    return parser


def _dispatch(controller: CalculatorController, args: argparse.Namespace) -> str:
    """Dispatch parsed CLI arguments to the controller and return the result.

    Extracts operands from *args* and forwards them to
    :meth:`~src.controller.CalculatorController.execute`, keeping argument
    parsing separate from computation dispatch.

    Returns the result as a string.  Raises ValueError or ZeroDivisionError
    when the Calculator detects an invalid input.
    """
    op = args.operation
    if op in ("add", "subtract", "multiply", "divide"):
        return controller.execute(op, a=args.a, b=args.b)
    if op == "power":
        return controller.execute("power", a=args.base, b=args.exp)
    if op in ("square", "cube", "ln"):
        return controller.execute(op, a=args.a)
    if op == "sqrt":
        return controller.execute("square_root", a=args.a)
    if op == "cbrt":
        return controller.execute("cube_root", a=args.a)
    if op == "log":
        return controller.execute("log", a=args.a, base=args.base)
    if op == "factorial":
        return controller.execute("factorial", a=args.n)
    # Unreachable: argparse enforces valid subcommands
    raise ValueError(f"Unknown operation: {op}")


def cli_main() -> None:
    """Entry point for bash CLI mode.

    Parses sys.argv, dispatches the operation via the controller, and prints
    the result.  Errors are written to stderr; the process exits with code 1
    on failure.
    """
    parser = build_parser()
    args = parser.parse_args()
    controller = CalculatorController()

    try:
        result = _dispatch(controller, args)
    except (ValueError, ZeroDivisionError) as exc:
        get_error_logger().error("[cli] %s: %s", args.operation, exc)
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(result)
