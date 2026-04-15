"""Interactive menu-driven mode components.

Exports
-------
TooManyAttemptsError       : exception raised after too many invalid inputs.
MAX_ATTEMPTS               : maximum consecutive invalid inputs before session ends.
NORMAL_MODE_OPERATIONS     : mapping of menu keys to basic operation names.
SCIENTIFIC_MODE_OPERATIONS : mapping of menu keys to all operation names.
OPERATIONS                 : alias for SCIENTIFIC_MODE_OPERATIONS (backward compat).
_ONE_ARG_OPS               : operations that take one float argument.
_INT_ARG_OPS               : operations that take one integer argument.
_TWO_ARG_OPS               : operations that take two float arguments.
_ALL_OPS                   : union of all operation sets.
_OP_PROMPTS                : prompt strings for each operation (UI layer only).
show_menu                  : print the operation menu for the given mode.
parse_number               : prompt for and return a float, with retry logic.
parse_int                  : prompt for and return an int, with retry logic.
run_operation              : collect inputs, run the operation, print the result.
"""
from ..calculator import Calculator
from .history import append_to_error_log

MAX_ATTEMPTS = 3


class TooManyAttemptsError(Exception):
    """Raised when the user exceeds the maximum number of invalid input attempts."""


NORMAL_MODE_OPERATIONS = {
    "1": "add",
    "2": "subtract",
    "3": "multiply",
    "4": "divide",
}

SCIENTIFIC_MODE_OPERATIONS = {
    "1": "add",
    "2": "subtract",
    "3": "multiply",
    "4": "divide",
    "5": "factorial",
    "6": "square",
    "7": "cube",
    "8": "square_root",
    "9": "cube_root",
    "10": "power",
    "11": "log",
    "12": "ln",
}

# Backward-compatible alias — callers that imported OPERATIONS still work.
OPERATIONS = SCIENTIFIC_MODE_OPERATIONS

# Operations grouped by arity and argument type.
_ONE_ARG_OPS = {"square", "cube", "square_root", "cube_root", "ln"}
_INT_ARG_OPS = {"factorial"}
_TWO_ARG_OPS = {"add", "subtract", "multiply", "divide", "power", "log"}
_ALL_OPS = _ONE_ARG_OPS | _INT_ARG_OPS | _TWO_ARG_OPS

# Prompt strings for interactive mode, keyed by operation name.
# Each tuple holds one prompt per required argument, in argument order.
# Keeping prompts here (UI layer) keeps Calculator free of display concerns.
_OP_PROMPTS: dict[str, tuple[str, ...]] = {
    "add":         ("  Enter first number: ",           "  Enter second number: "),
    "subtract":    ("  Enter first number: ",           "  Enter second number: "),
    "multiply":    ("  Enter first number: ",           "  Enter second number: "),
    "divide":      ("  Enter dividend: ",               "  Enter divisor: "),
    "factorial":   ("  Enter non-negative integer: ",),
    "square":      ("  Enter number: ",),
    "cube":        ("  Enter number: ",),
    "square_root": ("  Enter number: ",),
    "cube_root":   ("  Enter number: ",),
    "power":       ("  Enter base: ",                   "  Enter exponent: "),
    "log":         ("  Enter number: ",                 "  Enter base: "),
    "ln":          ("  Enter number: ",),
}


def show_menu(
    operations: "dict | None" = None,
    mode: str = "normal",
) -> None:
    """Print the operation menu to stdout.

    Parameters
    ----------
    operations:
        Mapping of menu keys to operation names to display.  Defaults to
        ``NORMAL_MODE_OPERATIONS`` when ``None``.
    mode:
        Current mode label shown in the header.  Either ``"normal"`` or
        ``"scientific"``.  Controls the mode-switch prompt at the bottom.
    """
    if operations is None:
        operations = NORMAL_MODE_OPERATIONS
    print(f"\n--- Calculator ({mode.title()} Mode) ---")
    for key, name in operations.items():
        print(f"  {key}. {name}")
    print("  h. show history")
    if mode == "normal":
        print("  s. switch to scientific mode")
    else:
        print("  s. switch to normal mode")
    print("  q. quit")


def parse_number(prompt: str, max_attempts: int = MAX_ATTEMPTS) -> float:
    """Prompt the user until a valid number is entered and return it as float.

    Raises TooManyAttemptsError after *max_attempts* consecutive invalid inputs.
    """
    for attempt in range(1, max_attempts + 1):
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            append_to_error_log(f"invalid_input: '{raw}' is not a valid number")
            remaining = max_attempts - attempt
            if remaining > 0:
                print(f"  Invalid number: '{raw}'. Please try again ({remaining} attempt(s) left).")
            else:
                print(f"  Invalid number: '{raw}'. No attempts remaining.")
    raise TooManyAttemptsError("Too many invalid number inputs. Ending session.")


def parse_int(prompt: str, max_attempts: int = MAX_ATTEMPTS) -> int:
    """Prompt the user until a valid integer is entered and return it.

    Raises TooManyAttemptsError after *max_attempts* consecutive invalid inputs.
    """
    for attempt in range(1, max_attempts + 1):
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            append_to_error_log(f"invalid_input: '{raw}' is not a valid integer")
            remaining = max_attempts - attempt
            if remaining > 0:
                print(f"  Invalid integer: '{raw}'. Please try again ({remaining} attempt(s) left).")
            else:
                print(f"  Invalid integer: '{raw}'. No attempts remaining.")
    raise TooManyAttemptsError("Too many invalid integer inputs. Ending session.")


def run_operation(calc: Calculator, operation: str) -> "str | None":
    """Collect inputs for *operation*, execute it, and print the result.

    User interaction (prompting) is separated from calculation: prompts are
    looked up in *_OP_PROMPTS* (UI layer); the actual computation is
    delegated to *Calculator.execute* (logic layer).

    Returns a history entry string (e.g. ``"add(3.0, 4.0) = 7.0"``) on
    success, or ``None`` when the operation fails or is not recognised.
    """
    if operation not in _OP_PROMPTS:
        append_to_error_log(f"unsupported_operation: '{operation}'")
        print(f"  Unknown operation: {operation}")
        return None

    try:
        prompts = _OP_PROMPTS[operation]
        if operation in _INT_ARG_OPS:
            n = parse_int(prompts[0])
            result = calc.execute(operation, n)
            entry = f"{operation}({n}) = {result}"
        elif operation in _ONE_ARG_OPS:
            a = parse_number(prompts[0])
            result = calc.execute(operation, a)
            entry = f"{operation}({a}) = {result}"
        else:  # _TWO_ARG_OPS
            a = parse_number(prompts[0])
            b = parse_number(prompts[1])
            result = calc.execute(operation, a, b)
            entry = f"{operation}({a}, {b}) = {result}"
        print(f"  Result: {result}")
        return entry
    except ValueError as exc:
        append_to_error_log(f"calculation_error: {exc}")
        print(f"  Error: {exc}")
        return None
