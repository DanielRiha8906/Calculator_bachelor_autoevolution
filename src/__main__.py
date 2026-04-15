from .session import CalculatorSession
from .error_logger import log_error

# Normal mode: standard arithmetic plus square and square root.
NORMAL_OPERATIONS: dict[str, tuple[str, int]] = {
    "1": ("add",         2),
    "2": ("subtract",    2),
    "3": ("multiply",    2),
    "4": ("divide",      2),
    "5": ("square",      1),
    "6": ("square_root", 1),
}

# Scientific mode: all normal operations plus advanced functions.
SCIENTIFIC_OPERATIONS: dict[str, tuple[str, int]] = {
    "1":  ("add",         2),
    "2":  ("subtract",    2),
    "3":  ("multiply",    2),
    "4":  ("divide",      2),
    "5":  ("square",      1),
    "6":  ("square_root", 1),
    "7":  ("factorial",   1),
    "8":  ("cube",        1),
    "9":  ("cube_root",   1),
    "10": ("power",       2),
    "11": ("log",         1),
    "12": ("ln",          1),
    "13": ("sin",         1),
    "14": ("cos",         1),
    "15": ("tan",         1),
    "16": ("cot",         1),
    "17": ("asin",        1),
    "18": ("acos",        1),
}

# Maximum number of failed input attempts before the session is terminated.
MAX_ATTEMPTS = 5

# Path where the session history is written when the session ends.
HISTORY_FILE = "history.txt"


class _SessionExpired(Exception):
    """Raised internally when the user exhausts all retry attempts for an input."""


def display_menu(
    operations: dict | None = None,
    mode_name: str = "Normal",
) -> None:
    """Print the operation menu for the active mode to stdout.

    Args:
        operations: Mapping of menu key to (operation_name, arity).
                    Defaults to NORMAL_OPERATIONS when not supplied.
        mode_name:  Human-readable name of the current mode (e.g. "Normal").
    """
    if operations is None:
        operations = NORMAL_OPERATIONS
    print(f"Mode: {mode_name}")
    print("Available operations:")
    for key, (name, _) in operations.items():
        print(f"  {key}. {name}")
    print("  m. switch mode")
    print("  h. history")
    print("  q. quit")


def format_history_entry(name: str, args: tuple, result) -> str:
    """Format a completed calculation as a function-style history entry.

    Delegates to :meth:`CalculatorSession.format_entry`.

    Examples:
        add(2, 3) = 5
        factorial(5) = 120
        square_root(9) = 3.0
    """
    return CalculatorSession.format_entry(name, args, result)


def save_history(history: list[str], path: str | None = None) -> None:
    """Write the session history list to *path*, one entry per line.

    If *path* is None the module-level HISTORY_FILE constant is used.
    Any previous file at *path* is overwritten so each session starts fresh.
    """
    if path is None:
        path = HISTORY_FILE
    with open(path, "w", encoding="utf-8") as fh:
        for entry in history:
            fh.write(entry + "\n")


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
            log_error("interactive", f"invalid operand input: {exc}")
            print(f"Error: {exc}")
            if remaining > 0:
                print(f"Please try again ({remaining} attempt(s) remaining).")
            else:
                print("Maximum attempts reached. Ending session.")
                raise _SessionExpired() from exc


def main() -> None:
    """Run an interactive calculator session with Normal and Scientific modes.

    The session starts in Normal mode and can be switched to Scientific mode
    at any time by entering 'm'.  Normal mode exposes the standard arithmetic
    operations plus square and square root.  Scientific mode adds advanced
    functions: cube, cube root, factorial, power, log, ln, and trigonometric
    operations (sin, cos, tan, cot, asin, acos — all in degrees).

    The loop continues until the user enters 'q' or the maximum number of
    failed input attempts is reached.

    Successful calculations are recorded in the session history (via
    CalculatorSession) and can be displayed at any time by entering 'h'.
    When the session ends the full history is written to HISTORY_FILE.
    """
    session = CalculatorSession()
    current_mode = "Normal"
    current_ops = NORMAL_OPERATIONS
    display_menu(current_ops, current_mode)
    invalid_op_attempts = 0

    while True:
        choice = input("\nEnter operation number (or 'm' to switch mode, 'h' for history, 'q' to quit): ").strip()

        if choice.lower() == "q":
            save_history(session.history())
            print("Goodbye!")
            break

        if choice.lower() == "h":
            hist = session.history()
            if hist:
                print("Session history:")
                for entry in hist:
                    print(f"  {entry}")
            else:
                print("No history yet.")
            continue

        if choice.lower() == "m":
            print("Select mode:")
            print("  1. Normal")
            print("  2. Scientific")
            mode_choice = input("Enter mode number: ").strip()
            if mode_choice == "1":
                current_mode = "Normal"
                current_ops = NORMAL_OPERATIONS
            elif mode_choice == "2":
                current_mode = "Scientific"
                current_ops = SCIENTIFIC_OPERATIONS
            else:
                print(f"Unknown mode '{mode_choice}'. Keeping {current_mode} mode.")
            display_menu(current_ops, current_mode)
            continue

        if choice not in current_ops:
            invalid_op_attempts += 1
            log_error("interactive", f"unknown operation '{choice}'")
            available = ", ".join(
                f"{k}. {v[0]}"
                for k, v in sorted(current_ops.items(), key=lambda item: int(item[0]))
            )
            print(
                f"Unknown operation '{choice}'. Available operations: {available}"
            )
            if invalid_op_attempts >= MAX_ATTEMPTS:
                save_history(session.history())
                print("Maximum attempts reached. Ending session.")
                break
            continue

        name, arity = current_ops[choice]

        try:
            if arity == 1:
                require_int = name == "factorial"
                prompt = "Enter integer: " if require_int else "Enter number: "
                a = get_number_with_retry(prompt, require_int=require_int)
                result = session.execute(name, a)
                print(f"Result: {result}")
            else:
                a = get_number_with_retry("Enter first number: ")
                b = get_number_with_retry("Enter second number: ")
                result = session.execute(name, a, b)
                print(f"Result: {result}")
        except _SessionExpired:
            save_history(session.history())
            break
        except (ValueError, TypeError, ZeroDivisionError) as exc:
            log_error("interactive", f"calculation error in {name}: {exc}")
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
