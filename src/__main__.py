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

# Maximum number of failed input attempts before the session is terminated.
MAX_ATTEMPTS = 5


class _SessionExpired(Exception):
    """Raised internally when the user exhausts all retry attempts for an input."""


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


def get_number_with_retry(prompt: str, require_int: bool = False):
    """Read a number from stdin, retrying up to MAX_ATTEMPTS times on invalid input.

    On each failed attempt an error message is printed together with the
    number of remaining tries. After MAX_ATTEMPTS failures the session is
    terminated by raising _SessionExpired.

    Args:
        prompt: The text shown to the user before reading.
        require_int: When True, parse the input strictly as an integer.

    Returns:
        The parsed number.

    Raises:
        _SessionExpired: if the user fails MAX_ATTEMPTS times without valid input.
    """
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            return get_number(prompt, require_int=require_int)
        except ValueError as exc:
            remaining = MAX_ATTEMPTS - attempt
            print(f"Error: {exc}")
            if remaining > 0:
                print(f"Please try again ({remaining} attempt(s) remaining).")
            else:
                print("Maximum attempts reached. Ending session.")
                raise _SessionExpired() from exc


def main() -> None:
    """Run an interactive calculator session.

    Displays a menu of operations, reads the user's selection and the
    required operands, computes the result, and prints it. The loop
    continues until the user enters 'q' or the maximum number of failed
    input attempts is reached.

    Invalid operation selections show an error with the list of available
    operations and allow the user to retry; the session ends after
    MAX_ATTEMPTS total invalid selections. Invalid operand inputs also
    allow retries up to MAX_ATTEMPTS per prompt before ending the session.
    """
    calc = Calculator()
    display_menu()
    invalid_op_attempts = 0

    while True:
        choice = input("\nEnter operation number (or 'q' to quit): ").strip()

        if choice.lower() == "q":
            print("Goodbye!")
            break

        if choice not in OPERATIONS:
            invalid_op_attempts += 1
            available = ", ".join(
                f"{k}. {v[0]}"
                for k, v in sorted(OPERATIONS.items(), key=lambda item: int(item[0]))
            )
            print(
                f"Unknown operation '{choice}'. Available operations: {available}"
            )
            if invalid_op_attempts >= MAX_ATTEMPTS:
                print("Maximum attempts reached. Ending session.")
                break
            continue

        name, arity = OPERATIONS[choice]
        method = getattr(calc, name)

        try:
            if arity == 1:
                require_int = name == "factorial"
                prompt = "Enter integer: " if require_int else "Enter number: "
                a = get_number_with_retry(prompt, require_int=require_int)
                result = method(a)
                print(f"Result: {result}")
            else:
                a = get_number_with_retry("Enter first number: ")
                b = get_number_with_retry("Enter second number: ")
                result = method(a, b)
                print(f"Result: {result}")
        except _SessionExpired:
            break
        except (ValueError, TypeError, ZeroDivisionError) as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
