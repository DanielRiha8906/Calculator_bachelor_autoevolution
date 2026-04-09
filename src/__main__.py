import datetime
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

# Maximum number of consecutive invalid inputs before the interactive session ends.
MAX_ATTEMPTS = 3

# File used to persist history within an interactive session.
HISTORY_FILE = "history.txt"

# File used to record errors and invalid-usage events.
ERROR_LOG_FILE = "calculator_errors.log"


def _log_error(path: str, message: str) -> None:
    """Append a timestamped error entry to the error log file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(path, "a") as f:
        f.write(f"[{timestamp}] ERROR: {message}\n")


def _parse_float(s: str) -> float:
    """Parse a string as float, raising ValueError with a clear message on failure."""
    try:
        return float(s)
    except ValueError:
        raise ValueError(f"'{s}' is not a valid number")


def _clear_history(path: str) -> None:
    """Create or truncate the history file at the start of a new session."""
    with open(path, "w") as f:
        pass


def _append_history(path: str, entry: str) -> None:
    """Append one operation entry to the history file."""
    with open(path, "a") as f:
        f.write(entry + "\n")


def _show_history(path: str, print_fn) -> None:
    """Print all history entries recorded so far in this session."""
    try:
        with open(path, "r") as f:
            lines = [line.rstrip("\n") for line in f if line.strip()]
    except FileNotFoundError:
        lines = []
    if not lines:
        print_fn("No history yet.")
    else:
        print_fn("History:")
        for line in lines:
            print_fn(f"  {line}")


def run_calculator(input_fn=input, print_fn=print, history_file=HISTORY_FILE, error_log_file=ERROR_LOG_FILE):
    """Run the interactive calculator loop.

    Accepts optional input_fn and print_fn for testability, history_file
    to override where session history is written (defaults to HISTORY_FILE),
    and error_log_file to override where errors are logged (defaults to
    ERROR_LOG_FILE).
    Clears the history file at the start of each session so history does not
    persist between runs.
    Loops until the user quits, answers 'n' to continue, or exceeds
    MAX_ATTEMPTS consecutive invalid inputs for a choice or operand.
    """
    calc = Calculator()
    _clear_history(history_file)

    while True:
        print_fn("\nSelect an operation:")
        for key, (_, _, label) in OPERATIONS.items():
            print_fn(f"  {key}. {label}")
        print_fn("  h. Show history")
        print_fn("  q. Quit")

        # Prompt for operation choice, retrying up to MAX_ATTEMPTS on invalid input.
        # Entering 'h' displays history without consuming an attempt.
        op_name = None
        num_args = None
        attempt = 0
        while attempt < MAX_ATTEMPTS:
            choice = input_fn("Enter choice: ").strip().lower()
            if choice == "q":
                print_fn("Goodbye!")
                return
            if choice == "h":
                _show_history(history_file, print_fn)
                continue
            if choice in OPERATIONS:
                op_name, num_args, _ = OPERATIONS[choice]
                break
            attempt += 1
            _log_error(error_log_file, f"Invalid operation choice: '{choice}'")
            remaining = MAX_ATTEMPTS - attempt
            if remaining > 0:
                print_fn("Invalid choice. Please try again.")
            else:
                print_fn("Invalid choice. Too many invalid attempts. Ending session.")
                return

        method = getattr(calc, op_name)

        # Prompt for operand(s), retrying up to MAX_ATTEMPTS on invalid input.
        for attempt in range(MAX_ATTEMPTS):
            try:
                if num_args == 1:
                    raw = input_fn("Enter value: ").strip()
                    if op_name == "factorial":
                        val = _parse_float(raw)
                        if val != int(val):
                            raise ValueError("Factorial requires a whole number.")
                        x = int(val)
                    else:
                        x = _parse_float(raw)
                    result = method(x)
                    _append_history(history_file, f"{op_name}({x}) = {result}")
                else:
                    a = _parse_float(input_fn("Enter first value: ").strip())
                    b = _parse_float(input_fn("Enter second value: ").strip())
                    result = method(a, b)
                    _append_history(history_file, f"{op_name}({a}, {b}) = {result}")
                print_fn(f"Result: {result}")
                break
            except (ValueError, ZeroDivisionError) as e:
                _log_error(error_log_file, f"Error in '{op_name}': {e}")
                remaining = MAX_ATTEMPTS - attempt - 1
                print_fn(f"Error: {e}")
                if remaining > 0:
                    print_fn("Please try again.")
                else:
                    print_fn("Too many invalid inputs. Ending session.")
                    return

        again = input_fn("Continue? (y/n): ").strip().lower()
        if again != "y":
            print_fn("Goodbye!")
            break


def run_bash_mode(args, print_fn=print, error_log_file=ERROR_LOG_FILE):
    """Execute a single calculator operation from command-line arguments.

    Args:
        args: list of strings, e.g. ["add", "5", "3"] or ["sqrt", "16"]
        print_fn: callable used for output (injectable for testing)
        error_log_file: path to the error log file (defaults to ERROR_LOG_FILE)

    Returns:
        0 on success, 1 on error.
    """
    if not args:
        print_fn("Usage: python -m src <operation> <value1> [<value2>]")
        print_fn("Operations: " + ", ".join(OP_BY_NAME.keys()))
        _log_error(error_log_file, "No arguments provided to bash mode")
        return 1

    op_name = args[0].lower()
    if op_name not in OP_BY_NAME:
        print_fn(f"Error: Unknown operation '{op_name}'")
        print_fn("Operations: " + ", ".join(OP_BY_NAME.keys()))
        _log_error(error_log_file, f"Unknown operation: '{op_name}'")
        return 1

    num_args = OP_BY_NAME[op_name]
    calc = Calculator()
    method = getattr(calc, op_name)

    try:
        if num_args == 1:
            if len(args) != 2:
                print_fn(f"Error: '{op_name}' requires exactly 1 value")
                _log_error(error_log_file, f"Wrong argument count for '{op_name}': expected 1 value")
                return 1
            if op_name == "factorial":
                val = _parse_float(args[1])
                if val != int(val):
                    raise ValueError("Factorial requires a whole number.")
                x = int(val)
            else:
                x = _parse_float(args[1])
            result = method(x)
        else:
            if len(args) != 3:
                print_fn(f"Error: '{op_name}' requires exactly 2 values")
                _log_error(error_log_file, f"Wrong argument count for '{op_name}': expected 2 values")
                return 1
            a = _parse_float(args[1])
            b = _parse_float(args[2])
            result = method(a, b)
        print_fn(f"Result: {result}")
        return 0
    except (ValueError, ZeroDivisionError) as e:
        print_fn(f"Error: {e}")
        _log_error(error_log_file, f"Calculation error in bash mode ('{op_name}'): {e}")
        return 1


def main():
    """Entry point: bash mode if arguments provided, interactive mode otherwise."""
    if len(sys.argv) > 1:
        sys.exit(run_bash_mode(sys.argv[1:]))
    run_calculator()


if __name__ == "__main__":
    main()
