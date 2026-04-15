"""Calculator entry point.

Dispatches between interactive menu-driven mode, non-interactive CLI mode,
and the optional graphical interface (``--gui`` flag).
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
    NORMAL_MODE_OPERATIONS,
    SCIENTIFIC_MODE_OPERATIONS,
    OPERATIONS,
    TooManyAttemptsError,
    show_menu,
    parse_number,
    parse_int,
    run_operation,
)
from .interface.cli import cli_mode
from .interface.gui import launch_gui


def main(args: list[str] | None = None) -> None:
    """Run the calculator in CLI, interactive, or GUI mode.

    * ``--gui``: launch the tkinter graphical interface (blocks until closed).
    * Non-empty *args* without ``--gui``: execute a single operation via
      :func:`cli_mode` and exit.
    * No args: start the interactive menu-driven loop.
    """
    if args is None:
        args = sys.argv[1:]
    if args and args[0] == "--gui":
        launch_gui()
        return
    if args:
        sys.exit(cli_mode(args))

    # Interactive loop
    calc = Calculator()
    clear_history()
    mode = "normal"
    current_ops = NORMAL_MODE_OPERATIONS
    invalid_op_count = 0
    while True:
        show_menu(current_ops, mode)
        choice = input("Select operation: ").strip().lower()
        if choice == "q":
            print("Goodbye!")
            break
        if choice == "h":
            show_history()
            continue
        if choice == "s":
            if mode == "normal":
                mode = "scientific"
                current_ops = SCIENTIFIC_MODE_OPERATIONS
                print("  Switched to scientific mode.")
            else:
                mode = "normal"
                current_ops = NORMAL_MODE_OPERATIONS
                print("  Switched to normal mode.")
            continue
        if choice not in current_ops:
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
            entry = run_operation(calc, current_ops[choice])
            if entry is not None:
                append_to_history(entry)
        except TooManyAttemptsError as exc:
            print(f"  {exc}")
            break


if __name__ == "__main__":
    main()
