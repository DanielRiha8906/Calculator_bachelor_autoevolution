"""Interactive session module for the calculator.

Manages the full lifecycle of a single interactive calculator session:
menu display, user input collection with retry logic, operation dispatch,
session history tracking, and history persistence on exit.

This module is the primary home for all session-scoped state and behaviour.
The entry point in src/__main__.py is a thin wrapper that delegates to
InteractiveSession.
"""
import pathlib

from .calculator import Calculator
from .error_logger import get_error_logger, setup_error_logging

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
    logger = get_error_logger()
    for attempt in range(MAX_RETRIES):
        try:
            return _parse_number(prompt, require_int=require_int)
        except ValueError as exc:
            logger.error("[interactive] invalid operand input: %s", exc)
            remaining = MAX_RETRIES - attempt - 1
            if remaining > 0:
                print(f"Error: {exc}. {remaining} attempt(s) remaining.")
            else:
                print(f"Error: {exc}.")
    return None


class InteractiveSession:
    """Manages state and control flow for a single interactive calculator session.

    Separates session concerns (history tracking, failure counting, operation
    dispatch) from input/output details so that the Calculator core can be
    exercised independently of how the user interacts with the application.
    """

    def __init__(self, calc: Calculator | None = None) -> None:
        """Initialise the session with an optional Calculator instance.

        Args:
            calc: Calculator to use for all operations.  A new instance is
                  created when None is passed.
        """
        self._calc = calc if calc is not None else Calculator()
        self._history: list[str] = []
        self._menu_failures: int = 0

    def run(self) -> None:
        """Run the interactive session loop until the user quits or retries are exhausted.

        Sets up error logging, displays the menu, reads user selections, and
        dispatches each valid operation to _handle_operation.  Session history
        is written to HISTORY_FILE on every exit path.
        """
        setup_error_logging()
        _logger = get_error_logger()

        print("=== Interactive Calculator ===")
        available_keys = ", ".join(OPERATIONS.keys())

        while True:
            self._display_menu()
            choice = input("\nSelect operation: ").strip().lower()

            if choice == "q":
                print("Goodbye!")
                break

            if choice == "h":
                self._show_history()
                continue

            if choice not in OPERATIONS:
                self._menu_failures += 1
                _logger.error("[interactive] invalid menu choice: %s", choice)
                print(
                    f"Invalid choice '{choice}'. "
                    f"Available options: {available_keys}, h, q."
                )
                if self._menu_failures >= MAX_RETRIES:
                    _logger.error("[interactive] max retries exceeded for menu selection")
                    print("Too many invalid selections. Ending session.")
                    break
                remaining = MAX_RETRIES - self._menu_failures
                print(f"{remaining} attempt(s) remaining.")
                continue

            self._menu_failures = 0
            if not self._handle_operation(choice):
                break

        _write_history(self._history)

    def _display_menu(self) -> None:
        """Print the available operations menu to stdout."""
        print("\nAvailable operations:")
        for key, (_, label, _) in OPERATIONS.items():
            print(f"  {key:>2}. {label}")
        print("   h. Show history")
        print("   q. Quit")

    def _show_history(self) -> None:
        """Display the current session history to stdout."""
        if self._history:
            print("\nSession history:")
            for entry in self._history:
                print(f"  {entry}")
        else:
            print("No calculations yet.")

    def _handle_operation(self, choice: str) -> bool:
        """Collect operands for the chosen operation and execute it.

        Args:
            choice: A valid key from OPERATIONS.

        Returns:
            True if the session should continue, False if max retries were
            exceeded while collecting operands.
        """
        _logger = get_error_logger()
        op_name, _label, arity = OPERATIONS[choice]
        method = getattr(self._calc, op_name)
        require_int = op_name == "factorial"

        if arity == 1:
            a = _prompt_number("Enter value: ", require_int=require_int)
            if a is None:
                _logger.error(
                    "[interactive] max retries exceeded for operand input in %s", op_name
                )
                print("Too many invalid inputs. Ending session.")
                return False
            operands: tuple = (a,)
        else:
            a = _prompt_number("Enter first value: ")
            if a is None:
                _logger.error(
                    "[interactive] max retries exceeded for operand input in %s", op_name
                )
                print("Too many invalid inputs. Ending session.")
                return False
            b = _prompt_number("Enter second value: ")
            if b is None:
                _logger.error(
                    "[interactive] max retries exceeded for operand input in %s", op_name
                )
                print("Too many invalid inputs. Ending session.")
                return False
            operands = (a, b)

        try:
            result = method(*operands)
            print(f"Result: {result}")
            self._history.append(_format_history_entry(op_name, operands, result))
        except (ValueError, TypeError, ZeroDivisionError) as exc:
            _logger.error("[interactive] calculation error in %s: %s", op_name, exc)
            print(f"Error: {exc}")

        return True
