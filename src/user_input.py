"""Interactive user input interface for the Calculator.

Implements a text-based REPL that lets a user perform calculator operations
by selecting numbered menu entries.  Input validation retries up to
:data:`MAX_RETRIES` times before raising a :class:`ValueError`.

Menu choices
------------
1–12
    Named operations (add, subtract, multiply, divide, factorial, square,
    cube, square_root, cube_root, power, log, ln).
h
    Display the full operation history for the current session.
q
    Quit the interactive session.

Usage::

    python -m src          # starts this REPL automatically
"""

import logging

from .calculator import Calculator

logger = logging.getLogger(__name__)


OPERATIONS = {
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

TWO_ARG_OPS = {"add", "subtract", "multiply", "divide", "power"}
INT_OPS = {"factorial"}

MAX_RETRIES = 3


def _print_menu() -> None:
    """Print the operations menu."""
    print("Calculator - Interactive Mode")
    print("Operations:")
    for key, name in OPERATIONS.items():
        print(f"  {key}: {name}")
    print("  h: show history")
    print("  q: quit")


def _print_history(history: list[dict]) -> None:
    """Print the operation history to stdout."""
    if not history:
        print("No history.")
        return
    for i, entry in enumerate(history, start=1):
        args_str = ", ".join(str(a) for a in entry["args"])
        print(f"  {i}. {entry['operation']}({args_str}) = {entry['result']}")


def _get_float(prompt: str) -> float:
    """Prompt for a float, retrying up to MAX_RETRIES times on invalid input."""
    for attempt in range(1, MAX_RETRIES + 1):
        raw = input(prompt)
        try:
            return float(raw)
        except ValueError:
            remaining = MAX_RETRIES - attempt
            if remaining > 0:
                print(f"Invalid input: {raw!r}. Please enter a number. ({remaining} attempt(s) remaining)")
            else:
                print(f"Invalid input: {raw!r}. No more retries.")
    error_msg = f"Failed to get a valid number after {MAX_RETRIES} attempts."
    logger.error(error_msg)
    raise ValueError(error_msg)


def _get_int(prompt: str) -> int:
    """Prompt for an integer, retrying up to MAX_RETRIES times on invalid input."""
    for attempt in range(1, MAX_RETRIES + 1):
        raw = input(prompt)
        try:
            return int(raw)
        except ValueError:
            remaining = MAX_RETRIES - attempt
            if remaining > 0:
                print(f"Invalid input: {raw!r}. Please enter an integer. ({remaining} attempt(s) remaining)")
            else:
                print(f"Invalid input: {raw!r}. No more retries.")
    error_msg = f"Failed to get a valid integer after {MAX_RETRIES} attempts."
    logger.error(error_msg)
    raise ValueError(error_msg)


def interactive_mode() -> None:
    """Run an interactive calculator session reading operands from stdin."""
    calc = Calculator()
    _print_menu()

    while True:
        choice = input("Select operation (or 'q' to quit): ").strip()

        if choice.lower() == "q":
            print("Goodbye!")
            break

        if choice.lower() == "h":
            _print_history(calc.get_history())
            continue

        if choice not in OPERATIONS:
            print(f"Unknown operation: {choice!r}. Please choose from the menu.")
            continue

        op_name = OPERATIONS[choice]
        op = getattr(calc, op_name)

        try:
            if op_name in INT_OPS:
                a = _get_int("Enter integer: ")
                result = op(a)
            elif op_name in TWO_ARG_OPS:
                a = _get_float("Enter first number: ")
                b = _get_float("Enter second number: ")
                result = op(a, b)
            else:
                a = _get_float("Enter number: ")
                result = op(a)
            print(f"Result: {result}")
        except (ValueError, ZeroDivisionError, TypeError) as e:
            print(f"Error: {e}")
