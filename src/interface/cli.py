"""Non-interactive CLI mode: execute a single operation from command-line arguments."""
import sys
import argparse

from ..calculator import Calculator
from .history import append_to_error_log
from .interactive import _ONE_ARG_OPS, _INT_ARG_OPS, _TWO_ARG_OPS, _ALL_OPS


def cli_mode(args: list[str]) -> int:
    """Execute a single operation from command-line arguments.

    Parses *args* (e.g. ``["add", "3", "4"]``), runs the requested
    Calculator operation, and prints the result to stdout.

    Returns 0 on success, 1 on error.  Errors are written to stderr so that
    the numeric result is always the only line on stdout.
    """
    parser = argparse.ArgumentParser(
        prog="python -m src",
        description="Calculator — execute a single operation and print the result.",
    )
    parser.add_argument(
        "operation",
        choices=sorted(_ALL_OPS),
        help="Operation to perform.",
    )
    parser.add_argument(
        "values",
        nargs="+",
        metavar="VALUE",
        help="Numeric argument(s) required by the operation.",
    )
    namespace = parser.parse_args(args)
    op = namespace.operation
    raw = namespace.values

    calc = Calculator()
    try:
        if op in _INT_ARG_OPS:
            if len(raw) != 1:
                msg = f"'{op}' requires exactly 1 integer argument"
                append_to_error_log(f"invalid_input: {msg}")
                print(f"Error: {msg}.", file=sys.stderr)
                return 1
            try:
                n = int(raw[0])
            except ValueError:
                append_to_error_log(f"invalid_input: '{raw[0]}' is not a valid integer")
                print(f"Error: '{raw[0]}' is not a valid integer.", file=sys.stderr)
                return 1
            result = calc.execute(op, n)
        elif op in _ONE_ARG_OPS:
            if len(raw) != 1:
                msg = f"'{op}' requires exactly 1 argument"
                append_to_error_log(f"invalid_input: {msg}")
                print(f"Error: {msg}.", file=sys.stderr)
                return 1
            try:
                a = float(raw[0])
            except ValueError:
                append_to_error_log(f"invalid_input: '{raw[0]}' is not a valid number")
                print(f"Error: '{raw[0]}' is not a valid number.", file=sys.stderr)
                return 1
            result = calc.execute(op, a)
        else:  # two-argument operations
            if len(raw) != 2:
                msg = f"'{op}' requires exactly 2 arguments"
                append_to_error_log(f"invalid_input: {msg}")
                print(f"Error: {msg}.", file=sys.stderr)
                return 1
            parsed: list[float] = []
            for v in raw[:2]:
                try:
                    parsed.append(float(v))
                except ValueError:
                    append_to_error_log(f"invalid_input: '{v}' is not a valid number")
                    print(f"Error: '{v}' is not a valid number.", file=sys.stderr)
                    return 1
            result = calc.execute(op, *parsed)
    except ValueError as exc:
        append_to_error_log(f"calculation_error: {exc}")
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(result)
    return 0
