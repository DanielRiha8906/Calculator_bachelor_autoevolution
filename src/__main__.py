from .calculator import Calculator

MAX_ATTEMPTS = 5
HISTORY_FILE = "history.txt"

OPERATIONS = {
    "1":  ("add",         2, "Add"),
    "2":  ("subtract",    2, "Subtract"),
    "3":  ("multiply",    2, "Multiply"),
    "4":  ("divide",      2, "Divide"),
    "5":  ("power",       2, "Power"),
    "6":  ("factorial",   1, "Factorial"),
    "7":  ("square",      1, "Square"),
    "8":  ("cube",        1, "Cube"),
    "9":  ("square_root", 1, "Square root"),
    "10": ("cube_root",   1, "Cube root"),
    "11": ("log",         1, "Log (base-10)"),
    "12": ("ln",          1, "Natural log (ln)"),
}


class TooManyAttemptsError(Exception):
    """Raised when the user exceeds the maximum number of invalid input attempts."""


def _fmt_num(x) -> str:
    """Format a number, omitting the decimal point for whole-number floats."""
    if isinstance(x, float) and x.is_integer():
        return str(int(x))
    return str(x)


def _format_entry(method_name: str, operands: tuple, result) -> str:
    """Return a history entry in function-call style, e.g. add(2, 3) = 5."""
    operand_str = ", ".join(_fmt_num(o) for o in operands)
    return f"{method_name}({operand_str}) = {_fmt_num(result)}"


def _write_history(history: list[str], path: str) -> None:
    """Write session history entries to *path*, one entry per line."""
    with open(path, "w") as f:
        for entry in history:
            f.write(entry + "\n")


def _read_number(prompt: str, max_attempts: int = MAX_ATTEMPTS) -> float:
    """Prompt the user until a valid float is entered or attempts are exhausted.

    Raises:
        TooManyAttemptsError: if the user fails to enter a valid number
            max_attempts times in a row.
    """
    for attempt in range(1, max_attempts + 1):
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            remaining = max_attempts - attempt
            if remaining == 0:
                raise TooManyAttemptsError(
                    "Too many invalid inputs — ending session."
                )
            print(
                f"  '{raw}' is not a valid number — please try again "
                f"({remaining} attempt(s) left)."
            )


def run_session(calc: Calculator, history_file: str = HISTORY_FILE) -> None:
    """Run an interactive calculator session until the user quits.

    Tracks all successful calculations in a session history list. On exit,
    the history is written to *history_file* (one entry per line). During
    the session, the user can type 'h' to display the current history.
    """
    print("Calculator — enter 0 to quit.")
    choice_failures = 0
    history: list[str] = []

    while True:
        print("\nOperations:")
        for key, (_, _, label) in OPERATIONS.items():
            print(f"  {key:>2}. {label}")
        print("   0. Quit")
        print("   h. Show history")

        choice = input("\nEnter choice: ").strip()

        if choice == "0":
            print("Goodbye!")
            break

        if choice == "h":
            if not history:
                print("  No history yet.")
            else:
                print("  History:")
                for entry in history:
                    print(f"    {entry}")
            continue

        if choice not in OPERATIONS:
            choice_failures += 1
            available = ", ".join(
                f"{key}: {label}"
                for key, (_, _, label) in sorted(
                    OPERATIONS.items(), key=lambda x: int(x[0])
                )
            )
            if choice_failures >= MAX_ATTEMPTS:
                print(
                    f"  Unknown choice '{choice}'. "
                    f"Too many invalid choices — ending session."
                )
                break
            remaining = MAX_ATTEMPTS - choice_failures
            print(
                f"  Unknown choice '{choice}'. "
                f"Available operations: {available}. "
                f"({remaining} attempt(s) left)"
            )
            continue

        choice_failures = 0
        method_name, operand_count, _ = OPERATIONS[choice]

        try:
            if operand_count == 1:
                a = _read_number("  Enter value: ")
                if method_name == "factorial":
                    if a != int(a):
                        print("  Error: factorial requires a whole number.")
                        continue
                    operand = int(a)
                    result = getattr(calc, method_name)(operand)
                    history.append(_format_entry(method_name, (operand,), result))
                else:
                    result = getattr(calc, method_name)(a)
                    history.append(_format_entry(method_name, (a,), result))
            else:
                a = _read_number("  Enter first value: ")
                b = _read_number("  Enter second value: ")
                result = getattr(calc, method_name)(a, b)
                history.append(_format_entry(method_name, (a, b), result))

            print(f"  Result: {result}")
        except TooManyAttemptsError as exc:
            print(f"  {exc}")
            break
        except (ValueError, ZeroDivisionError, TypeError) as exc:
            print(f"  Error: {exc}")

    _write_history(history, history_file)


def main() -> None:
    calc = Calculator()
    run_session(calc)


if __name__ == "__main__":
    main()
