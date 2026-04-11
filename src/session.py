"""Interactive session module for the calculator.

Manages the full lifecycle of a single interactive calculator session:
mode selection, menu display, user input collection with retry logic,
operation dispatch, session history tracking, and history persistence
on exit.

Normal mode exposes the standard four-function set plus square and square
root.  Scientific mode exposes a broader set of advanced operations
including powers, roots, logarithms, factorial, and trigonometry.
The user may switch between modes at any time during the session without
restarting the application.

This module is the primary home for all session-scoped state and behaviour.
The entry point in src/__main__.py is a thin wrapper that delegates to
InteractiveSession.
"""
import pathlib

from .calculator import Calculator
from .error_logger import get_error_logger, setup_error_logging

MAX_RETRIES = 5
HISTORY_FILE = "history.txt"

# Normal mode: standard four-function operations plus square and square root.
# Maps menu key -> (method_name, display_label, number_of_operands)
NORMAL_OPERATIONS: dict[str, tuple[str, str, int]] = {
    "1": ("add",      "Add             (a + b)",  2),
    "2": ("subtract", "Subtract        (a - b)",  2),
    "3": ("multiply", "Multiply        (a * b)",  2),
    "4": ("divide",   "Divide          (a / b)",  2),
    "5": ("square",   "Square          (n²)",      1),
    "6": ("sqrt",     "Square root     (√n)",      1),
}

# Scientific mode: advanced operations including trig, roots, logs, factorial.
# Maps menu key -> (method_name, display_label, number_of_operands)
SCIENTIFIC_OPERATIONS: dict[str, tuple[str, str, int]] = {
    "1":  ("power",     "Power           (base ^ exp)",  2),
    "2":  ("cube",      "Cube            (n³)",           1),
    "3":  ("cbrt",      "Cube root       (∛n)",           1),
    "4":  ("factorial", "Factorial       (n!)",            1),
    "5":  ("log10",     "Log base-10     (log₁₀ n)",     1),
    "6":  ("ln",        "Natural log     (ln n)",          1),
    "7":  ("sin",       "Sine            (sin θ rad)",     1),
    "8":  ("cos",       "Cosine          (cos θ rad)",     1),
    "9":  ("tan",       "Tangent         (tan θ rad)",     1),
    "10": ("cot",       "Cotangent       (cot θ rad)",     1),
    "11": ("asin",      "Arcsine         (asin n → rad)",  1),
    "12": ("acos",      "Arccosine       (acos n → rad)",  1),
}

# Maps user selection key to (display name, operations dict)
_MODES: dict[str, tuple[str, dict[str, tuple[str, str, int]]]] = {
    "1": ("Normal",     NORMAL_OPERATIONS),
    "2": ("Scientific", SCIENTIFIC_OPERATIONS),
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


def _prompt_mode() -> tuple[str, dict] | None:
    """Prompt the user to select a calculator mode.

    Displays the available modes and reads the user's choice with retry
    logic up to MAX_RETRIES attempts.

    Returns:
        ``(mode_name, operations_dict)`` on a valid selection, or ``None``
        after MAX_RETRIES consecutive invalid inputs.
    """
    logger = get_error_logger()
    print("\nSelect mode:")
    print("  1. Normal")
    print("  2. Scientific")
    for attempt in range(MAX_RETRIES):
        choice = input("Mode: ").strip()
        if choice in _MODES:
            mode_name, operations = _MODES[choice]
            return mode_name, operations
        logger.error("[interactive] invalid mode selection: %s", choice)
        remaining = MAX_RETRIES - attempt - 1
        if remaining > 0:
            print(
                f"Invalid choice '{choice}'. "
                f"Please enter 1 (Normal) or 2 (Scientific). "
                f"{remaining} attempt(s) remaining."
            )
        else:
            print(f"Invalid choice '{choice}'.")
    return None


class InteractiveSession:
    """Manages state and control flow for a single interactive calculator session.

    Separates session concerns (history tracking, failure counting, mode
    management, operation dispatch) from input/output details so that the
    Calculator core can be exercised independently of how the user interacts
    with the application.

    The session begins with a mode selection step (Normal or Scientific).
    The user may switch modes at any time via the 'm' menu option without
    restarting the session.
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
        self._mode_name: str = "Normal"
        self._operations: dict[str, tuple[str, str, int]] = NORMAL_OPERATIONS

    def run(self) -> None:
        """Run the interactive session loop until the user quits or retries are exhausted.

        Sets up error logging, prompts for mode selection, displays the menu,
        reads user selections, and dispatches each valid operation to
        _handle_operation.  The user may switch modes mid-session with 'm'.
        Session history is written to HISTORY_FILE on every exit path.
        """
        setup_error_logging()
        _logger = get_error_logger()

        print("=== Interactive Calculator ===")

        result = _prompt_mode()
        if result is None:
            _logger.error("[interactive] max retries exceeded for mode selection")
            print("Too many invalid selections. Ending session.")
            _write_history(self._history)
            return

        self._mode_name, self._operations = result
        print(f"Mode: {self._mode_name}")

        while True:
            self._display_menu()
            choice = input("\nSelect operation: ").strip().lower()

            if choice == "q":
                print("Goodbye!")
                break

            if choice == "h":
                self._show_history()
                continue

            if choice == "m":
                switch_result = _prompt_mode()
                if switch_result is None:
                    _logger.error("[interactive] max retries exceeded for mode selection")
                    print("Too many invalid selections. Ending session.")
                    break
                self._mode_name, self._operations = switch_result
                print(f"Mode: {self._mode_name}")
                continue

            available_keys = ", ".join(self._operations.keys())
            if choice not in self._operations:
                self._menu_failures += 1
                _logger.error("[interactive] invalid menu choice: %s", choice)
                print(
                    f"Invalid choice '{choice}'. "
                    f"Available options: {available_keys}, h, m, q."
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
        """Print the available operations menu for the current mode to stdout."""
        print(f"\n[{self._mode_name} mode] Available operations:")
        for key, (_, label, _) in self._operations.items():
            print(f"  {key:>2}. {label}")
        print("   h. Show history")
        print("   m. Switch mode")
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
            choice: A valid key from the current mode's operations dict.

        Returns:
            True if the session should continue, False if max retries were
            exceeded while collecting operands.
        """
        _logger = get_error_logger()
        op_name, _label, arity = self._operations[choice]
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
