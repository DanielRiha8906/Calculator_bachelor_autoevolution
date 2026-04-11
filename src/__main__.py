from .calculator import Calculator

# Maps menu key -> (method_name, display_label, number_of_operands)
OPERATIONS = {
    "1":  ("add",       "Add             (a + b)",    2),
    "2":  ("subtract",  "Subtract        (a - b)",    2),
    "3":  ("multiply",  "Multiply        (a * b)",    2),
    "4":  ("divide",    "Divide          (a / b)",    2),
    "5":  ("factorial", "Factorial       (n!)",        1),
    "6":  ("square",    "Square          (n²)",        1),
    "7":  ("cube",      "Cube            (n³)",        1),
    "8":  ("sqrt",      "Square root     (√n)",        1),
    "9":  ("cbrt",      "Cube root       (∛n)",        1),
    "10": ("power",     "Power           (base ^ exp)", 2),
    "11": ("log10",     "Log base-10     (log₁₀ n)",  1),
    "12": ("ln",        "Natural log     (ln n)",      1),
}


def _parse_number(prompt: str, require_int: bool = False):
    """Read a number from stdin.

    Args:
        prompt: Text displayed before the cursor.
        require_int: When True, parse the input strictly as an integer.
            Raises ValueError for non-integer strings (e.g. "3.5").

    Returns:
        int if the input represents a whole number or require_int is True,
        float otherwise.
    """
    raw = input(prompt).strip()
    if require_int:
        return int(raw)
    # Prefer int representation for whole-number strings so results look clean.
    try:
        return int(raw)
    except ValueError:
        return float(raw)


def main() -> None:
    """Run the interactive calculator session.

    Displays a menu of all available operations, reads the user's selection,
    collects the required operand(s), and prints the result.  The loop
    continues until the user enters 'q' to quit.
    """
    calc = Calculator()
    print("=== Interactive Calculator ===")

    while True:
        print("\nAvailable operations:")
        for key, (_, label, _) in OPERATIONS.items():
            print(f"  {key:>2}. {label}")
        print("   q. Quit")

        choice = input("\nSelect operation: ").strip().lower()

        if choice == "q":
            print("Goodbye!")
            break

        if choice not in OPERATIONS:
            print("Invalid choice. Please enter a number from the list or 'q' to quit.")
            continue

        op_name, _label, arity = OPERATIONS[choice]
        method = getattr(calc, op_name)
        require_int = op_name == "factorial"

        try:
            if arity == 1:
                a = _parse_number("Enter value: ", require_int=require_int)
                result = method(a)
            else:
                a = _parse_number("Enter first value: ")
                b = _parse_number("Enter second value: ")
                result = method(a, b)
            print(f"Result: {result}")
        except (ValueError, TypeError, ZeroDivisionError) as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
