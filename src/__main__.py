import argparse
import sys
from .calculator import Calculator


OPERATIONS = {
    "1":  ("add",       2, "Addition (a + b)"),
    "2":  ("subtract",  2, "Subtraction (a - b)"),
    "3":  ("multiply",  2, "Multiplication (a * b)"),
    "4":  ("divide",    2, "Division (a / b)"),
    "5":  ("power",     2, "Power (base ^ exp)"),
    "6":  ("factorial", 1, "Factorial (n!)"),
    "7":  ("square",    1, "Square (x^2)"),
    "8":  ("cube",      1, "Cube (x^3)"),
    "9":  ("sqrt",      1, "Square Root (sqrt x)"),
    "10": ("cbrt",      1, "Cube Root (cbrt x)"),
    "11": ("log",       1, "Logarithm base 10 (log x)"),
    "12": ("ln",        1, "Natural Logarithm (ln x)"),
}

# Derived lookup: operation name → required number of arguments
OP_MAP = {name: num_args for _, (name, num_args, _) in OPERATIONS.items()}


def run_cli(argv=None, print_fn=print):
    """Run the calculator in non-interactive bash mode.

    Parses operation and operands from command-line arguments and prints
    the result to stdout. Exits with code 1 on math errors, code 2 on
    argument errors.

    Usage:
        python -m src <operation> <value1> [value2]

    Examples:
        python -m src add 5 3
        python -m src factorial 7
        python -m src divide 10 0
    """
    parser = argparse.ArgumentParser(
        prog="python -m src",
        description=(
            "Calculator — non-interactive (bash) mode.\n"
            "Run without arguments to start the interactive menu instead."
        ),
    )
    parser.add_argument(
        "operation",
        choices=sorted(OP_MAP),
        metavar="operation",
        help=(
            "Operation to perform. Binary (two values): add, divide, multiply, power, subtract. "
            "Unary (one value): cbrt, cube, factorial, ln, log, sqrt, square."
        ),
    )
    parser.add_argument(
        "values",
        nargs="+",
        type=float,
        help="Operand(s) for the operation.",
    )

    args = parser.parse_args(argv)
    op_name = args.operation
    num_args = OP_MAP[op_name]

    if len(args.values) != num_args:
        parser.error(
            f"'{op_name}' requires exactly {num_args} value(s), got {len(args.values)}"
        )

    calc = Calculator()
    method = getattr(calc, op_name)

    try:
        if op_name == "factorial":
            val = args.values[0]
            if val != int(val):
                raise ValueError("Factorial requires a whole number.")
            result = method(int(val))
        elif num_args == 1:
            result = method(args.values[0])
        else:
            result = method(args.values[0], args.values[1])
        print_fn(f"Result: {result}")
    except ValueError as e:
        print_fn(f"Error: {e}")
        raise SystemExit(1)


def run_calculator(input_fn=input, print_fn=print):
    """Run the interactive calculator loop.

    Accepts optional input_fn and print_fn for testability.
    Loops until the user quits.
    """
    calc = Calculator()

    while True:
        print_fn("\nSelect an operation:")
        for key, (_, _, label) in OPERATIONS.items():
            print_fn(f"  {key}. {label}")
        print_fn("  q. Quit")

        choice = input_fn("Enter choice: ").strip().lower()

        if choice == "q":
            print_fn("Goodbye!")
            break

        if choice not in OPERATIONS:
            print_fn("Invalid choice. Please try again.")
            continue

        op_name, num_args, _ = OPERATIONS[choice]
        method = getattr(calc, op_name)

        try:
            if num_args == 1:
                raw = input_fn("Enter value: ").strip()
                if op_name == "factorial":
                    val = float(raw)
                    if val != int(val):
                        raise ValueError("Factorial requires a whole number.")
                    x = int(val)
                else:
                    x = float(raw)
                result = method(x)
            else:
                a = float(input_fn("Enter first value: ").strip())
                b = float(input_fn("Enter second value: ").strip())
                result = method(a, b)
            print_fn(f"Result: {result}")
        except ValueError as e:
            print_fn(f"Error: {e}")

        again = input_fn("Continue? (y/n): ").strip().lower()
        if again != "y":
            print_fn("Goodbye!")
            break


def main():
    """Entry point: routes to bash CLI mode or interactive mode based on arguments."""
    if len(sys.argv) > 1:
        run_cli()
    else:
        run_calculator()


if __name__ == "__main__":
    main()
