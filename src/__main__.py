from .controller import CalculatorController, CHOICE_TO_OPERATION
from .error_logger import get_error_logger
from .history import clear_history, display_history, record_entry

MAX_INPUT_ATTEMPTS = 3


class TooManyAttemptsError(Exception):
    """Raised when the user exceeds the maximum number of invalid input attempts."""


MENU = (
    "\nCalculator Operations:\n"
    "  1.  Add              (a + b)\n"
    "  2.  Subtract         (a - b)\n"
    "  3.  Multiply         (a * b)\n"
    "  4.  Divide           (a / b)\n"
    "  5.  Factorial        (n!)\n"
    "  6.  Square           (a^2)\n"
    "  7.  Cube             (a^3)\n"
    "  8.  Square Root      (sqrt(a))\n"
    "  9.  Cube Root        (cbrt(a))\n"
    " 10.  Power            (base^exp)\n"
    " 11.  Log              (log_base(a), default base 10)\n"
    " 12.  Natural Log      (ln(a))\n"
    " 13.  Show History\n"
    "  0.  Exit\n"
)

OPERATION_NAMES = {
    "1": "Add",
    "2": "Subtract",
    "3": "Multiply",
    "4": "Divide",
    "5": "Factorial",
    "6": "Square",
    "7": "Cube",
    "8": "Square Root",
    "9": "Cube Root",
    "10": "Power",
    "11": "Log",
    "12": "Natural Log",
}


def display_menu() -> None:
    """Print the operation menu to stdout."""
    print(MENU)


def get_number(prompt: str, max_attempts: int = MAX_INPUT_ATTEMPTS) -> float:
    """Read a numeric value from stdin, retrying on invalid input.

    Raises TooManyAttemptsError after *max_attempts* consecutive invalid inputs.
    """
    for attempt in range(1, max_attempts + 1):
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            remaining = max_attempts - attempt
            if remaining > 0:
                print(
                    f"Invalid input '{raw}': please enter a numeric value."
                    f" {remaining} attempt(s) remaining."
                )
            else:
                print(f"Invalid input '{raw}': please enter a numeric value.")
    raise TooManyAttemptsError(f"Maximum input attempts ({max_attempts}) exceeded.")


def get_integer(prompt: str, max_attempts: int = MAX_INPUT_ATTEMPTS) -> int:
    """Read an integer value from stdin, retrying on invalid input.

    Raises TooManyAttemptsError after *max_attempts* consecutive invalid inputs.
    """
    for attempt in range(1, max_attempts + 1):
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            remaining = max_attempts - attempt
            if remaining > 0:
                print(
                    f"Invalid input '{raw}': please enter a whole number."
                    f" {remaining} attempt(s) remaining."
                )
            else:
                print(f"Invalid input '{raw}': please enter a whole number.")
    raise TooManyAttemptsError(f"Maximum input attempts ({max_attempts}) exceeded.")


def perform_operation(controller: CalculatorController, choice: str) -> "str | None":
    """Collect operands from stdin and execute the operation identified by *choice*.

    Delegates computation to *controller*, keeping user interaction (prompts,
    input validation) separate from calculation dispatch.  Returns the result
    as a string, or None if *choice* is not a recognised operation number.
    Propagates ValueError and ZeroDivisionError raised by the controller.
    """
    operation = CHOICE_TO_OPERATION.get(choice)
    if operation is None:
        return None

    if operation in ("add", "subtract", "multiply", "divide"):
        a = get_number("Enter first number: ")
        b = get_number("Enter second number: ")
        return controller.execute(operation, a=a, b=b)

    if operation == "factorial":
        n = get_integer("Enter a non-negative integer: ")
        return controller.execute(operation, a=n)

    if operation in ("square", "cube", "square_root", "cube_root", "ln"):
        a = get_number("Enter a number: ")
        return controller.execute(operation, a=a)

    if operation == "power":
        base_val = get_number("Enter base: ")
        exp_val = get_number("Enter exponent: ")
        return controller.execute(operation, a=base_val, b=exp_val)

    if operation == "log":
        a = get_number("Enter a number: ")
        base_raw = input("Enter log base (press Enter for base 10): ").strip()
        if base_raw:
            try:
                log_base = float(base_raw)
            except ValueError:
                get_error_logger().error(
                    "[interactive] Invalid log base '%s': using base 10", base_raw
                )
                print(f"Invalid base '{base_raw}': using base 10.")
                log_base = 10.0
        else:
            log_base = 10.0
        return controller.execute(operation, a=a, base=log_base)

    return None  # unreachable; all operations in CHOICE_TO_OPERATION are handled above


def main() -> None:
    """Run the interactive calculator session."""
    controller = CalculatorController()
    clear_history()
    print("Welcome to the Calculator!")
    consecutive_invalid_choices = 0
    valid_choices = {str(i) for i in range(1, 14)}

    while True:
        display_menu()
        choice = input("Select operation: ").strip()

        if choice == "0":
            print("Goodbye!")
            break

        if choice not in valid_choices:
            consecutive_invalid_choices += 1
            get_error_logger().error(
                "[interactive] Unknown operation choice: '%s'", choice
            )
            print(f"Unknown operation '{choice}'. Please choose a number between 0 and 13.")
            if consecutive_invalid_choices >= MAX_INPUT_ATTEMPTS:
                print("Too many invalid choices. Ending session.")
                break
            continue

        consecutive_invalid_choices = 0

        if choice == "13":
            display_history()
            continue

        try:
            result = perform_operation(controller, choice)
        except TooManyAttemptsError as e:
            get_error_logger().error("[interactive] %s", e)
            print(str(e))
            break
        except (ValueError, ZeroDivisionError) as e:
            get_error_logger().error(
                "[interactive] %s: %s", OPERATION_NAMES.get(choice, choice), e
            )
            print(f"Error: {e}")
            continue

        if result is None:
            print(f"Unknown operation '{choice}'. Please choose a number between 0 and 13.")
        else:
            record_entry(f"{OPERATION_NAMES[choice]}: {result}")
            print(f"Result: {result}")


if __name__ == "__main__":
    import sys
    if sys.argv[1:]:
        from .cli import cli_main
        cli_main()
    else:
        main()
