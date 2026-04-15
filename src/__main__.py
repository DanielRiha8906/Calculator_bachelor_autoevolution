"""Calculator entry point.

Dispatches between interactive menu-driven mode and non-interactive CLI mode.
All implementation lives in the interface sub-package; this module owns only
the top-level :func:`main` function and the ``__main__`` guard.

Re-exports from sub-modules are provided for backward compatibility.
"""
import sys

from .calculator import Calculator
from .interface.history import (
    HISTORY_FILE,
    ERROR_LOG_FILE,
    clear_history,
    append_to_history,
    show_history,
    append_to_error_log,
)
from .interface.interactive import (
    MAX_ATTEMPTS,
    OPERATIONS,
    TooManyAttemptsError,
    show_menu,
    parse_number,
    parse_int,
    run_operation,
)
from .interface.cli import cli_mode


def main(args: list[str] | None = None) -> None:
    """Run the calculator in CLI or interactive mode.

    If *args* is provided (or ``sys.argv[1:]`` is non-empty when *args* is
    ``None``), execute a single operation via :func:`cli_mode` and exit.
    Otherwise start the interactive menu-driven loop.
    """
    if args is None:
        args = sys.argv[1:]
    if args:
        sys.exit(cli_mode(args))

    # Interactive loop
    calc = Calculator()
    clear_history()
    invalid_op_count = 0
    while True:
        show_menu()
        choice = input("Select operation: ").strip().lower()
        if choice == "q":
            print("Goodbye!")
            break
        if choice == "h":
            show_history()
            continue
        if choice not in OPERATIONS:
            append_to_error_log(f"invalid_input: '{choice}' is not a valid menu choice")
            invalid_op_count += 1
            remaining = MAX_ATTEMPTS - invalid_op_count
            if remaining <= 0:
                print(f"  Invalid choice: '{choice}'. Too many invalid choices. Ending session.")
                break
            print(f"  Invalid choice: '{choice}'. Please select a valid option ({remaining} attempt(s) left).")
            continue
        invalid_op_count = 0
        try:
            entry = run_operation(calc, OPERATIONS[choice])
            if entry is not None:
                append_to_history(entry)
        except TooManyAttemptsError as exc:
            print(f"  {exc}")
            break


if __name__ == "__main__":
    main()
