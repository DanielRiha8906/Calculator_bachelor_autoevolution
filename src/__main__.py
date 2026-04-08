from .calculator import Calculator

MAX_ATTEMPTS = 5

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


def run_session(calc: Calculator) -> None:
    """Run an interactive calculator session until the user quits."""
    print("Calculator — enter 0 to quit.")
    choice_failures = 0

    while True:
        print("\nOperations:")
        for key, (_, _, label) in OPERATIONS.items():
            print(f"  {key:>2}. {label}")
        print("   0. Quit")

        choice = input("\nEnter choice: ").strip()

        if choice == "0":
            print("Goodbye!")
            break

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
                    result = getattr(calc, method_name)(int(a))
                else:
                    result = getattr(calc, method_name)(a)
            else:
                a = _read_number("  Enter first value: ")
                b = _read_number("  Enter second value: ")
                result = getattr(calc, method_name)(a, b)

            print(f"  Result: {result}")
        except TooManyAttemptsError as exc:
            print(f"  {exc}")
            break
        except (ValueError, ZeroDivisionError, TypeError) as exc:
            print(f"  Error: {exc}")


def main() -> None:
    calc = Calculator()
    run_session(calc)


if __name__ == "__main__":
    main()
