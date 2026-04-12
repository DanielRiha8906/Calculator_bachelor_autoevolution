import sys
import argparse

from .calculator import Calculator

MAX_ATTEMPTS = 3
HISTORY_FILE = "history.txt"


class TooManyAttemptsError(Exception):
    """Raised when the user exceeds the maximum number of invalid input attempts."""


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


def clear_history(filepath: "str | None" = None) -> None:
    """Clear (or create) the history file, removing any previous session data.

    Uses *HISTORY_FILE* when *filepath* is ``None`` so that monkeypatching the
    module attribute in tests affects the default without needing to re-bind the
    function's default argument.
    """
    if filepath is None:
        filepath = HISTORY_FILE
    with open(filepath, "w", encoding="utf-8") as fh:
        fh.write("")


def append_to_history(entry: str, filepath: "str | None" = None) -> None:
    """Append a single history entry (one line) to the history file."""
    if filepath is None:
        filepath = HISTORY_FILE
    with open(filepath, "a", encoding="utf-8") as fh:
        fh.write(entry + "\n")


def show_history(filepath: "str | None" = None) -> None:
    """Print all history entries from the current session to stdout."""
    if filepath is None:
        filepath = HISTORY_FILE
    try:
        with open(filepath, "r", encoding="utf-8") as fh:
            lines = fh.read().splitlines()
    except FileNotFoundError:
        lines = []
    if not lines:
        print("  No history yet.")
    else:
        print("\n--- History ---")
        for i, line in enumerate(lines, start=1):
            print(f"  {i}. {line}")


def show_menu() -> None:
    """Print the operation menu to stdout."""
    print("\n--- Calculator ---")
    for key, name in OPERATIONS.items():
        print(f"  {key}. {name}")
    print("  h. show history")
    print("  q. quit")


def parse_number(prompt: str, max_attempts: int = MAX_ATTEMPTS) -> float:
    """Prompt the user until a valid number is entered and return it as float.

    Raises TooManyAttemptsError after *max_attempts* consecutive invalid inputs.
    """
    for attempt in range(1, max_attempts + 1):
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            remaining = max_attempts - attempt
            if remaining > 0:
                print(f"  Invalid number: '{raw}'. Please try again ({remaining} attempt(s) left).")
            else:
                print(f"  Invalid number: '{raw}'. No attempts remaining.")
    raise TooManyAttemptsError("Too many invalid number inputs. Ending session.")


def parse_int(prompt: str, max_attempts: int = MAX_ATTEMPTS) -> int:
    """Prompt the user until a valid integer is entered and return it.

    Raises TooManyAttemptsError after *max_attempts* consecutive invalid inputs.
    """
    for attempt in range(1, max_attempts + 1):
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            remaining = max_attempts - attempt
            if remaining > 0:
                print(f"  Invalid integer: '{raw}'. Please try again ({remaining} attempt(s) left).")
            else:
                print(f"  Invalid integer: '{raw}'. No attempts remaining.")
    raise TooManyAttemptsError("Too many invalid integer inputs. Ending session.")


def run_operation(calc: Calculator, operation: str) -> "str | None":
    """Collect inputs for *operation*, execute it, and print the result.

    Returns a history entry string (e.g. ``"add(3.0, 4.0) = 7.0"``) on
    success, or ``None`` when the operation fails or is not recognised.
    """
    try:
        if operation == "add":
            a = parse_number("  Enter first number: ")
            b = parse_number("  Enter second number: ")
            result = calc.add(a, b)
            entry = f"add({a}, {b}) = {result}"
        elif operation == "subtract":
            a = parse_number("  Enter first number: ")
            b = parse_number("  Enter second number: ")
            result = calc.subtract(a, b)
            entry = f"subtract({a}, {b}) = {result}"
        elif operation == "multiply":
            a = parse_number("  Enter first number: ")
            b = parse_number("  Enter second number: ")
            result = calc.multiply(a, b)
            entry = f"multiply({a}, {b}) = {result}"
        elif operation == "divide":
            a = parse_number("  Enter dividend: ")
            b = parse_number("  Enter divisor: ")
            result = calc.divide(a, b)
            entry = f"divide({a}, {b}) = {result}"
        elif operation == "factorial":
            n = parse_int("  Enter non-negative integer: ")
            result = calc.factorial(n)
            entry = f"factorial({n}) = {result}"
        elif operation == "square":
            a = parse_number("  Enter number: ")
            result = calc.square(a)
            entry = f"square({a}) = {result}"
        elif operation == "cube":
            a = parse_number("  Enter number: ")
            result = calc.cube(a)
            entry = f"cube({a}) = {result}"
        elif operation == "square_root":
            a = parse_number("  Enter number: ")
            result = calc.square_root(a)
            entry = f"square_root({a}) = {result}"
        elif operation == "cube_root":
            a = parse_number("  Enter number: ")
            result = calc.cube_root(a)
            entry = f"cube_root({a}) = {result}"
        elif operation == "power":
            a = parse_number("  Enter base: ")
            b = parse_number("  Enter exponent: ")
            result = calc.power(a, b)
            entry = f"power({a}, {b}) = {result}"
        elif operation == "log":
            a = parse_number("  Enter number: ")
            base = parse_number("  Enter base: ")
            result = calc.log(a, base)
            entry = f"log({a}, {base}) = {result}"
        elif operation == "ln":
            a = parse_number("  Enter number: ")
            result = calc.ln(a)
            entry = f"ln({a}) = {result}"
        else:
            print(f"  Unknown operation: {operation}")
            return None
        print(f"  Result: {result}")
        return entry
    except ValueError as exc:
        print(f"  Error: {exc}")
        return None


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
                print(
                    f"Error: '{op}' requires exactly 1 integer argument.",
                    file=sys.stderr,
                )
                return 1
            try:
                n = int(raw[0])
            except ValueError:
                print(f"Error: '{raw[0]}' is not a valid integer.", file=sys.stderr)
                return 1
            result = calc.factorial(n)
        elif op in _ONE_ARG_OPS:
            if len(raw) != 1:
                print(
                    f"Error: '{op}' requires exactly 1 argument.",
                    file=sys.stderr,
                )
                return 1
            try:
                a = float(raw[0])
            except ValueError:
                print(f"Error: '{raw[0]}' is not a valid number.", file=sys.stderr)
                return 1
            result = getattr(calc, op)(a)
        else:  # two-argument operations
            if len(raw) != 2:
                print(
                    f"Error: '{op}' requires exactly 2 arguments.",
                    file=sys.stderr,
                )
                return 1
            parsed: list[float] = []
            for v in raw[:2]:
                try:
                    parsed.append(float(v))
                except ValueError:
                    print(f"Error: '{v}' is not a valid number.", file=sys.stderr)
                    return 1
            result = getattr(calc, op)(*parsed)
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
    clear_history()
    invalid_op_count = 0
    while True:
        show_menu()
        choice = input("Select operation: ").strip().lower()
        if choice == "q":
            print("Goodbye!")
            break
        if choice == "h":
            show_history()
            continue
        if choice not in OPERATIONS:
            invalid_op_count += 1
            remaining = MAX_ATTEMPTS - invalid_op_count
            if remaining <= 0:
                print(f"  Invalid choice: '{choice}'. Too many invalid choices. Ending session.")
                break
            print(f"  Invalid choice: '{choice}'. Please select a valid option ({remaining} attempt(s) left).")
            continue
        invalid_op_count = 0
        try:
            entry = run_operation(calc, OPERATIONS[choice])
            if entry is not None:
                append_to_history(entry)
        except TooManyAttemptsError as exc:
            print(f"  {exc}")
            break


if __name__ == "__main__":
    main()
