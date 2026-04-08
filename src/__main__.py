import sys
from .calculator import Calculator


BINARY_OPS = {"add", "subtract", "multiply", "divide", "power"}
UNARY_OPS = {"factorial", "square", "cube", "square_root", "cube_root", "log", "ln"}
ALL_OPS = BINARY_OPS | UNARY_OPS


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

        try:
            if operation in BINARY_OPS:
                a_raw = input_fn("First number: ").strip()
                b_raw = input_fn("Second number: ").strip()
                try:
                    a = float(a_raw)
                    b = float(b_raw)
                except ValueError:
                    output_fn("Error: both inputs must be valid numbers.")
                    continue
                result = getattr(calc, operation)(a, b)
            else:
                raw = input_fn("Number: ").strip()
                if operation == "factorial":
                    try:
                        a = int(raw)
                    except ValueError:
                        output_fn("Error: factorial requires a whole number.")
                        continue
                else:
                    try:
                        a = float(raw)
                    except ValueError:
                        output_fn("Error: input must be a valid number.")
                        continue
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
