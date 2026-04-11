import pathlib

from .calculator import Calculator

MAX_RETRIES = 5
HISTORY_FILE = "history.txt"

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


def _format_history_entry(op_name: str, operands: tuple, result) -> str:
    """Format a history entry in function-style notation.

    Args:
        op_name: The calculator operation name (e.g. "add", "sqrt").
        operands: Tuple of operand values passed to the operation.
        result: The return value of the operation.

    Returns:
        A string like ``add(2, 3) = 5`` or ``sqrt(9) = 3.0``.
    """
    args = ", ".join(str(o) for o in operands)
    return f"{op_name}({args}) = {result}"


def _write_history(history: list[str]) -> None:
    """Write session history to HISTORY_FILE, one entry per line.

    Always overwrites the file so each session starts fresh on disk.
    Writes an empty file when no calculations were performed.

    Args:
        history: List of formatted history entry strings.
    """
    pathlib.Path(HISTORY_FILE).write_text("\n".join(history), encoding="utf-8")


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


def _prompt_number(prompt: str, require_int: bool = False) -> int | float | None:
    """Prompt for a number with retry logic up to MAX_RETRIES attempts.

    Re-prompts on invalid input and shows how many attempts remain.
    Returns None after MAX_RETRIES consecutive failures.

    Args:
        prompt: Text displayed before the cursor.
        require_int: When True, only accept integer input.

    Returns:
        Parsed number on success, or None if max retries are exceeded.
    """
    for attempt in range(MAX_RETRIES):
        try:
            return _parse_number(prompt, require_int=require_int)
        except ValueError as exc:
            remaining = MAX_RETRIES - attempt - 1
            if remaining > 0:
                print(f"Error: {exc}. {remaining} attempt(s) remaining.")
            else:
                print(f"Error: {exc}.")
    return None


def main() -> None:
    """Run the interactive calculator session.

    Displays a menu of all available operations, reads the user's selection,
    collects the required operand(s), and prints the result.  Successful
    calculations are recorded in a session history list.  The user can display
    the history at any time by entering 'h'.  When the session ends (user
    enters 'q' or the retry limit is reached) the history is written to
    HISTORY_FILE, overwriting any previous session.  The loop continues until
    the user enters 'q' to quit or the maximum number of consecutive invalid
    inputs (MAX_RETRIES) is reached.
    """
    calc = Calculator()
    history: list[str] = []
    print("=== Interactive Calculator ===")

    available_keys = ", ".join(OPERATIONS.keys())
    menu_failures = 0

    while True:
        print("\nAvailable operations:")
        for key, (_, label, _) in OPERATIONS.items():
            print(f"  {key:>2}. {label}")
        print("   h. Show history")
        print("   q. Quit")

        choice = input("\nSelect operation: ").strip().lower()

        if choice == "q":
            _write_history(history)
            print("Goodbye!")
            break

        if choice == "h":
            if history:
                print("\nSession history:")
                for entry in history:
                    print(f"  {entry}")
            else:
                print("No calculations yet.")
            continue

        if choice not in OPERATIONS:
            menu_failures += 1
            print(
                f"Invalid choice '{choice}'. "
                f"Available options: {available_keys}, h, q."
            )
            if menu_failures >= MAX_RETRIES:
                print("Too many invalid selections. Ending session.")
                _write_history(history)
                break
            remaining = MAX_RETRIES - menu_failures
            print(f"{remaining} attempt(s) remaining.")
            continue

        menu_failures = 0  # reset counter on a valid choice

        op_name, _label, arity = OPERATIONS[choice]
        method = getattr(calc, op_name)
        require_int = op_name == "factorial"

        if arity == 1:
            a = _prompt_number("Enter value: ", require_int=require_int)
            if a is None:
                print("Too many invalid inputs. Ending session.")
                _write_history(history)
                break
            try:
                result = method(a)
                print(f"Result: {result}")
                history.append(_format_history_entry(op_name, (a,), result))
            except (ValueError, TypeError, ZeroDivisionError) as exc:
                print(f"Error: {exc}")
        else:
            a = _prompt_number("Enter first value: ")
            if a is None:
                print("Too many invalid inputs. Ending session.")
                _write_history(history)
                break
            b = _prompt_number("Enter second value: ")
            if b is None:
                print("Too many invalid inputs. Ending session.")
                _write_history(history)
                break
            try:
                result = method(a, b)
                print(f"Result: {result}")
                history.append(_format_history_entry(op_name, (a, b), result))
            except (ValueError, TypeError, ZeroDivisionError) as exc:
                print(f"Error: {exc}")


if __name__ == "__main__":
    main()
