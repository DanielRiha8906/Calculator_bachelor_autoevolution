from .calculator import Calculator

# Maps menu keys to (operation_name, arity) pairs.
# arity=1 means one operand; arity=2 means two operands.
OPERATIONS = {
    "1":  ("add",         2),
    "2":  ("subtract",    2),
    "3":  ("multiply",    2),
    "4":  ("divide",      2),
    "5":  ("factorial",   1),
    "6":  ("square",      1),
    "7":  ("cube",        1),
    "8":  ("square_root", 1),
    "9":  ("cube_root",   1),
    "10": ("power",       2),
    "11": ("log",         1),
    "12": ("ln",          1),
}


def display_menu() -> None:
    """Print the operation menu to stdout."""
    print("Available operations:")
    for key, (name, _) in OPERATIONS.items():
        print(f"  {key}. {name}")
    print("  q. quit")


def get_number(prompt: str, require_int: bool = False):
    """Read a number from stdin.

    Args:
        prompt: The text shown to the user before reading.
        require_int: When True, parse the input strictly as an integer.

    Returns:
        An int if the input is a whole number (or require_int is True),
        otherwise a float.

    Raises:
        ValueError: if the input cannot be parsed as a number.
    """
    raw = input(prompt).strip()
    if require_int:
        return int(raw)
    try:
        return int(raw)
    except ValueError:
        return float(raw)


def main() -> None:
    """Run an interactive calculator session.

    Displays a menu of operations, reads the user's selection and the
    required operands, computes the result, and prints it. The loop
    continues until the user enters 'q'.
    """
    calc = Calculator()
    display_menu()

    while True:
        choice = input("\nEnter operation number (or 'q' to quit): ").strip()

        if choice.lower() == "q":
            print("Goodbye!")
            break

        if choice not in OPERATIONS:
            print(f"Unknown operation '{choice}'. Please enter a number from the menu.")
            continue

        name, arity = OPERATIONS[choice]
        method = getattr(calc, name)

        try:
            if arity == 1:
                require_int = name == "factorial"
                prompt = "Enter integer: " if require_int else "Enter number: "
                a = get_number(prompt, require_int=require_int)
                result = method(a)
                print(f"Result: {result}")
            else:
                a = get_number("Enter first number: ")
                b = get_number("Enter second number: ")
                result = method(a, b)
                print(f"Result: {result}")
        except (ValueError, TypeError, ZeroDivisionError) as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
