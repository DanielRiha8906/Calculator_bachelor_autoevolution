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

from .calculator import Calculator
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


def _dispatch(calc: Calculator, args: argparse.Namespace) -> str:
    """Dispatch parsed arguments to the appropriate Calculator method.

    Returns the result as a string.  Raises ValueError or ZeroDivisionError
    when the Calculator detects an invalid input.
    """
    op = args.operation
    if op == "add":
        return str(calc.add(args.a, args.b))
    if op == "subtract":
        return str(calc.subtract(args.a, args.b))
    if op == "multiply":
        return str(calc.multiply(args.a, args.b))
    if op == "divide":
        return str(calc.divide(args.a, args.b))
    if op == "power":
        return str(calc.power(args.base, args.exp))
    if op == "square":
        return str(calc.square(args.a))
    if op == "cube":
        return str(calc.cube(args.a))
    if op == "sqrt":
        return str(calc.square_root(args.a))
    if op == "cbrt":
        return str(calc.cube_root(args.a))
    if op == "ln":
        return str(calc.ln(args.a))
    if op == "log":
        return str(calc.log(args.a, args.base))
    if op == "factorial":
        return str(calc.factorial(args.n))
    # Unreachable: argparse enforces valid subcommands
    raise ValueError(f"Unknown operation: {op}")


def cli_main() -> None:
    """Entry point for bash CLI mode.

    Parses sys.argv, dispatches the operation, and prints the result.
    Errors are written to stderr; the process exits with code 1 on failure.
    """
    parser = build_parser()
    args = parser.parse_args()
    calc = Calculator()

    try:
        result = _dispatch(calc, args)
    except (ValueError, ZeroDivisionError) as exc:
        get_error_logger().error("[cli] %s: %s", args.operation, exc)
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(result)
