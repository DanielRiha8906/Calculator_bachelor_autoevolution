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


def main():
    calc = Calculator()
    run_interactive(calc)


if __name__ == "__main__":
    main()
