import sys
import argparse

from .calculator import Calculator

OPERATIONS = {
    "1": "add",
    "2": "subtract",
    "3": "multiply",
    "4": "divide",
    "5": "factorial",
    "6": "square",
    "7": "cube",
    "8": "square_root",
    "9": "cube_root",
    "10": "power",
    "11": "log",
    "12": "ln",
}

# Operations grouped by arity and argument type for CLI mode.
_ONE_ARG_OPS = {"square", "cube", "square_root", "cube_root", "ln"}
_INT_ARG_OPS = {"factorial"}
_TWO_ARG_OPS = {"add", "subtract", "multiply", "divide", "power", "log"}
_ALL_OPS = _ONE_ARG_OPS | _INT_ARG_OPS | _TWO_ARG_OPS


def show_menu() -> None:
    """Print the operation menu to stdout."""
    print("\n--- Calculator ---")
    for key, name in OPERATIONS.items():
        print(f"  {key}. {name}")
    print("  q. quit")


def parse_number(prompt: str) -> float:
    """Prompt the user until a valid number is entered and return it as float."""
    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print(f"  Invalid number: '{raw}'. Please try again.")


def parse_int(prompt: str) -> int:
    """Prompt the user until a valid integer is entered and return it."""
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print(f"  Invalid integer: '{raw}'. Please try again.")


def run_operation(calc: Calculator, operation: str) -> None:
    """Collect inputs for *operation*, execute it, and print the result."""
    try:
        if operation == "add":
            a = parse_number("  Enter first number: ")
            b = parse_number("  Enter second number: ")
            result = calc.add(a, b)
        elif operation == "subtract":
            a = parse_number("  Enter first number: ")
            b = parse_number("  Enter second number: ")
            result = calc.subtract(a, b)
        elif operation == "multiply":
            a = parse_number("  Enter first number: ")
            b = parse_number("  Enter second number: ")
            result = calc.multiply(a, b)
        elif operation == "divide":
            a = parse_number("  Enter dividend: ")
            b = parse_number("  Enter divisor: ")
            result = calc.divide(a, b)
        elif operation == "factorial":
            n = parse_int("  Enter non-negative integer: ")
            result = calc.factorial(n)
        elif operation == "square":
            a = parse_number("  Enter number: ")
            result = calc.square(a)
        elif operation == "cube":
            a = parse_number("  Enter number: ")
            result = calc.cube(a)
        elif operation == "square_root":
            a = parse_number("  Enter number: ")
            result = calc.square_root(a)
        elif operation == "cube_root":
            a = parse_number("  Enter number: ")
            result = calc.cube_root(a)
        elif operation == "power":
            a = parse_number("  Enter base: ")
            b = parse_number("  Enter exponent: ")
            result = calc.power(a, b)
        elif operation == "log":
            a = parse_number("  Enter number: ")
            base = parse_number("  Enter base: ")
            result = calc.log(a, base)
        elif operation == "ln":
            a = parse_number("  Enter number: ")
            result = calc.ln(a)
        else:
            print(f"  Unknown operation: {operation}")
            return
        print(f"  Result: {result}")
    except ValueError as exc:
        print(f"  Error: {exc}")


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
    parsed = parser.parse_args(args)
    op = parsed.operation
    raw = parsed.values

    calc = Calculator()
    try:
        if op in _INT_ARG_OPS:
            if len(raw) != 1:
                print(
                    f"Error: '{op}' requires exactly 1 integer argument.",
                    file=sys.stderr,
                )
                return 1
            result = calc.factorial(int(raw[0]))
        elif op in _ONE_ARG_OPS:
            if len(raw) != 1:
                print(
                    f"Error: '{op}' requires exactly 1 argument.",
                    file=sys.stderr,
                )
                return 1
            result = getattr(calc, op)(float(raw[0]))
        else:  # two-argument operations
            if len(raw) != 2:
                print(
                    f"Error: '{op}' requires exactly 2 arguments.",
                    file=sys.stderr,
                )
                return 1
            result = getattr(calc, op)(float(raw[0]), float(raw[1]))
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(result)
    return 0


def main(args: list[str] | None = None) -> None:
    """Run the calculator in CLI or interactive mode.

    If *args* is provided (or ``sys.argv[1:]`` is non-empty when *args* is
    ``None``), execute a single operation via :func:`cli_mode` and exit.
    Otherwise start the interactive menu-driven loop.
    """
    if args is None:
        args = sys.argv[1:]
    if args:
        sys.exit(cli_mode(args))

    # Interactive loop
    calc = Calculator()
    while True:
        show_menu()
        choice = input("Select operation: ").strip().lower()
        if choice == "q":
            print("Goodbye!")
            break
        if choice not in OPERATIONS:
            print(f"  Invalid choice: '{choice}'. Please select a valid option.")
            continue
        run_operation(calc, OPERATIONS[choice])


if __name__ == "__main__":
    main()
