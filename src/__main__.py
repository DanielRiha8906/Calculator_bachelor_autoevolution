import sys
from .calculator import Calculator


BINARY_OPS = {"add", "subtract", "multiply", "divide", "power"}
UNARY_OPS = {"factorial", "square", "cube", "square_root", "cube_root", "log", "ln"}
ALL_OPS = BINARY_OPS | UNARY_OPS

MAX_INPUT_RETRIES = 3


def _read_number(prompt: str, as_int: bool, input_fn, output_fn) -> float | int | None:
    """Prompt for a number, allowing up to MAX_INPUT_RETRIES attempts.

    Args:
        prompt: The prompt string shown to the user.
        as_int: If True, parse as integer; otherwise parse as float.
        input_fn: Callable used to read user input.
        output_fn: Callable used to display output.

    Returns:
        The parsed number on success, or None if all attempts are exhausted.
    """
    for attempt in range(1, MAX_INPUT_RETRIES + 1):
        raw = input_fn(prompt).strip()
        try:
            return int(raw) if as_int else float(raw)
        except ValueError:
            if as_int:
                msg = "Error: factorial requires a whole number."
            else:
                msg = "Error: input must be a valid number."
            remaining = MAX_INPUT_RETRIES - attempt
            if remaining > 0:
                output_fn(f"{msg} {remaining} attempt(s) remaining.")
            else:
                output_fn(f"{msg} Returning to operation menu.")
    return None


def run_interactive(calc: Calculator, input_fn=input, output_fn=print) -> None:
    """Run an interactive calculator session.

    Args:
        calc: Calculator instance to use.
        input_fn: Callable used to read user input (defaults to built-in input).
        output_fn: Callable used to display output (defaults to built-in print).
    """
    output_fn("Calculator - available operations:")
    output_fn("  Binary (two numbers): " + ", ".join(sorted(BINARY_OPS)))
    output_fn("  Unary  (one number):  " + ", ".join(sorted(UNARY_OPS)))
    output_fn("Type 'quit' to exit.")

    while True:
        operation = input_fn("Operation: ").strip().lower()
        if operation == "quit":
            break
        if operation not in ALL_OPS:
            output_fn(
                f"Unknown operation '{operation}'. "
                f"Try one of: {', '.join(sorted(ALL_OPS))}"
            )
            continue

        if operation in BINARY_OPS:
            a = _read_number("First number: ", False, input_fn, output_fn)
            if a is None:
                continue
            b = _read_number("Second number: ", False, input_fn, output_fn)
            if b is None:
                continue
        else:
            a = _read_number("Number: ", operation == "factorial", input_fn, output_fn)
            if a is None:
                continue

        try:
            if operation in BINARY_OPS:
                result = getattr(calc, operation)(a, b)
            else:
                result = getattr(calc, operation)(a)
            output_fn(f"Result: {result}")
        except (ValueError, TypeError) as e:
            output_fn(f"Error: {e}")


def run_cli(argv: list[str], calc: Calculator, output_fn=print) -> int:
    """Run calculator in non-interactive CLI (bash) mode.

    Parses argv and executes a single operation, printing the result.

    Args:
        argv: Argument list (operation and operands, without the program name).
        calc: Calculator instance to use.
        output_fn: Callable used to display output (defaults to built-in print).

    Returns:
        Exit code: 0 on success, 1 on error.
    """
    if not argv or argv[0] in ("-h", "--help"):
        output_fn("Usage: python -m src <operation> [number1] [number2]")
        output_fn("  Binary (two numbers): " + ", ".join(sorted(BINARY_OPS)))
        output_fn("  Unary  (one number):  " + ", ".join(sorted(UNARY_OPS)))
        return 0

    operation = argv[0].lower()

    if operation not in ALL_OPS:
        output_fn(
            f"Error: Unknown operation '{operation}'. "
            f"Try one of: {', '.join(sorted(ALL_OPS))}"
        )
        return 1

    try:
        if operation in BINARY_OPS:
            if len(argv) < 3:
                output_fn(f"Error: '{operation}' requires two numbers.")
                return 1
            try:
                a = float(argv[1])
                b = float(argv[2])
            except ValueError:
                output_fn("Error: both inputs must be valid numbers.")
                return 1
            result = getattr(calc, operation)(a, b)
        else:
            if len(argv) < 2:
                output_fn(f"Error: '{operation}' requires one number.")
                return 1
            if operation == "factorial":
                try:
                    a = int(argv[1])
                except ValueError:
                    output_fn("Error: factorial requires a whole number.")
                    return 1
            else:
                try:
                    a = float(argv[1])
                except ValueError:
                    output_fn("Error: input must be a valid number.")
                    return 1
            result = getattr(calc, operation)(a)
        output_fn(f"Result: {result}")
        return 0
    except (ValueError, TypeError) as e:
        output_fn(f"Error: {e}")
        return 1


def main():
    calc = Calculator()
    args = sys.argv[1:]
    if args:
        sys.exit(run_cli(args, calc))
    else:
        run_interactive(calc)


if __name__ == "__main__":
    main()
