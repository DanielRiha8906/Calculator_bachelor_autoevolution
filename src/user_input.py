"""Interactive user input interface for the Calculator."""

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

TWO_ARG_OPS = {"add", "subtract", "multiply", "divide", "power"}
INT_OPS = {"factorial"}


def _print_menu() -> None:
    """Print the operations menu."""
    print("Calculator - Interactive Mode")
    print("Operations:")
    for key, name in OPERATIONS.items():
        print(f"  {key}: {name}")
    print("  q: quit")


def interactive_mode() -> None:
    """Run an interactive calculator session reading operands from stdin."""
    calc = Calculator()
    _print_menu()

    while True:
        choice = input("Select operation (or 'q' to quit): ").strip()

        if choice.lower() == "q":
            print("Goodbye!")
            break

        if choice not in OPERATIONS:
            print(f"Unknown operation: {choice!r}. Please choose from the menu.")
            continue

        op_name = OPERATIONS[choice]
        op = getattr(calc, op_name)

        try:
            if op_name in INT_OPS:
                a = int(input("Enter integer: "))
                result = op(a)
            elif op_name in TWO_ARG_OPS:
                a = float(input("Enter first number: "))
                b = float(input("Enter second number: "))
                result = op(a, b)
            else:
                a = float(input("Enter number: "))
                result = op(a)
            print(f"Result: {result}")
        except (ValueError, ZeroDivisionError, TypeError) as e:
            print(f"Error: {e}")
