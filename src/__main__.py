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

# Maps operation name → number of required arguments, for bash mode lookup.
OP_BY_NAME = {name: num_args for _, (name, num_args, _) in OPERATIONS.items()}


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


def run_bash_mode(args, print_fn=print):
    """Execute a single calculator operation from command-line arguments.

    Args:
        args: list of strings, e.g. ["add", "5", "3"] or ["sqrt", "16"]
        print_fn: callable used for output (injectable for testing)

    Returns:
        0 on success, 1 on error.
    """
    if not args:
        print_fn("Usage: python -m src <operation> <value1> [<value2>]")
        print_fn("Operations: " + ", ".join(OP_BY_NAME.keys()))
        return 1

    op_name = args[0].lower()
    if op_name not in OP_BY_NAME:
        print_fn(f"Error: Unknown operation '{op_name}'")
        print_fn("Operations: " + ", ".join(OP_BY_NAME.keys()))
        return 1

    num_args = OP_BY_NAME[op_name]
    calc = Calculator()
    method = getattr(calc, op_name)

    try:
        if num_args == 1:
            if len(args) != 2:
                print_fn(f"Error: '{op_name}' requires exactly 1 value")
                return 1
            if op_name == "factorial":
                val = float(args[1])
                if val != int(val):
                    raise ValueError("Factorial requires a whole number.")
                x = int(val)
            else:
                x = float(args[1])
            result = method(x)
        else:
            if len(args) != 3:
                print_fn(f"Error: '{op_name}' requires exactly 2 values")
                return 1
            a = float(args[1])
            b = float(args[2])
            result = method(a, b)
        print_fn(f"Result: {result}")
        return 0
    except ValueError as e:
        print_fn(f"Error: {e}")
        return 1


def main():
    """Entry point: bash mode if arguments provided, interactive mode otherwise."""
    if len(sys.argv) > 1:
        sys.exit(run_bash_mode(sys.argv[1:]))
    run_calculator()


if __name__ == "__main__":
    main()
