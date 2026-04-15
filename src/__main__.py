"""Entry point for the Calculator application.

Supports two usage modes:

CLI mode (non-interactive)::

    python -m src <operation> [operands...]

    Examples:
        python -m src add 3 4          # prints 7
        python -m src factorial 5      # prints 120

Interactive REPL mode (no arguments)::

    python -m src

    A menu is displayed; the user selects an operation by number, enters
    operands when prompted, and can view history ('h') or quit ('q').
"""
import logging
import sys

from .calculator import Calculator, BINARY_OPS, UNARY_OPS, SCIENTIFIC_UNARY_OPS

logger = logging.getLogger(__name__)


# Maximum number of attempts allowed when prompting the user for a valid number
MAX_INPUT_ATTEMPTS = 3

MENU = """
Operations:
  1. add
  2. subtract
  3. multiply
  4. divide
  5. factorial
  6. square
  7. cube
  8. square_root
  9. cube_root
 10. power
 11. log (base-10)
 12. ln (natural log)
  h. history
  m. switch to scientific mode
  q. quit
"""

SCIENTIFIC_MENU = """
Scientific Operations (angles in radians):
  1. sin
  2. cos
  3. tan
  4. asin
  5. acos
  6. atan
  7. sinh
  8. cosh
  9. tanh
 10. exp (e^x)
  h. history
  m. switch to normal mode
  q. quit
"""

SCIENTIFIC_MENU_MAP = {
    "1": "sin",
    "2": "cos",
    "3": "tan",
    "4": "asin",
    "5": "acos",
    "6": "atan",
    "7": "sinh",
    "8": "cosh",
    "9": "tanh",
    "10": "exp",
}

MENU_MAP = {
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


def parse_number(prompt: str, max_attempts: int = MAX_INPUT_ATTEMPTS) -> float:
    """Prompt the user until a valid number is entered or max_attempts are exhausted.

    Raises ValueError if a valid number is not entered within max_attempts tries.
    """
    for attempt in range(max_attempts):
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            remaining = max_attempts - attempt - 1
            if remaining > 0:
                print(f"  Invalid number: {raw!r}. Please enter a numeric value. ({remaining} attempt(s) remaining)")
            else:
                print(f"  Invalid number: {raw!r}. No more attempts remaining.")
    raise ValueError(f"No valid number entered after {max_attempts} attempt(s)")


def run_operation(calc: Calculator, op: str) -> None:
    """Execute one calculator operation with user-supplied operands."""
    try:
        if op in BINARY_OPS:
            a = parse_number("  Enter first number: ")
            b = parse_number("  Enter second number: ")
            result = calc.execute(op, a, b)
        else:
            a = parse_number("  Enter number: ")
            result = calc.execute(op, a)
        print(f"  Result: {result}")
    except (ValueError, ZeroDivisionError) as exc:
        logger.error("run_operation %s failed: %s", op, exc)
        print(f"  Error: {exc}")


def _show_history(calc: Calculator) -> None:
    """Print the operation history stored in the Calculator instance."""
    if not calc.history:
        print("  No history yet.")
        return
    print("  History:")
    for i, entry in enumerate(calc.history, 1):
        op = entry["op"]
        operands = ", ".join(_format_result(o) for o in entry["operands"])
        result = _format_result(entry["result"])
        print(f"    {i}. {op}({operands}) = {result}")


def _format_result(value: "int | float") -> str:
    """Format a numeric result: whole floats are shown as integers."""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def cli_main(args: list) -> int:
    """Execute a single calculator operation from command-line arguments.

    Usage: python -m src <operation> [operands...]

    Returns 0 on success, 1 on error (message printed to stdout).
    """
    all_ops = UNARY_OPS | BINARY_OPS | SCIENTIFIC_UNARY_OPS
    if not args:
        print("Usage: python -m src <operation> [operands...]")
        print(f"Operations: {', '.join(sorted(all_ops))}")
        return 1

    op = args[0]
    if op not in all_ops:
        print(f"Error: Unknown operation {op!r}. Available: {', '.join(sorted(all_ops))}")
        return 1

    operand_args = args[1:]
    calc = Calculator()

    try:
        if op in BINARY_OPS:
            if len(operand_args) != 2:
                print(f"Error: {op} requires exactly 2 operands, got {len(operand_args)}")
                return 1
            a = float(operand_args[0])
            b = float(operand_args[1])
            result = calc.execute(op, a, b)
        else:
            if len(operand_args) != 1:
                print(f"Error: {op} requires exactly 1 operand, got {len(operand_args)}")
                return 1
            a = float(operand_args[0])
            result = calc.execute(op, a)
    except (ValueError, ZeroDivisionError) as exc:
        logger.error("cli_main %s failed: %s", op, exc)
        print(f"Error: {exc}")
        return 1

    print(_format_result(result))
    return 0


def main() -> None:
    """Configure logging and dispatch to CLI or interactive REPL mode.

    If command-line arguments are present, delegates to :func:`cli_main` and
    exits with its return code.  Otherwise starts the interactive REPL loop.
    """
    logging.basicConfig(
        level=logging.ERROR,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )
    if len(sys.argv) > 1:
        sys.exit(cli_main(sys.argv[1:]))

    calc = Calculator()
    mode = "normal"
    print("Welcome to the Calculator!")
    while True:
        print(MENU if mode == "normal" else SCIENTIFIC_MENU)
        choice = input("Choose an operation: ").strip().lower()
        if choice == "q":
            print("Goodbye!")
            break
        if choice == "h":
            _show_history(calc)
            continue
        if choice == "m":
            mode = "scientific" if mode == "normal" else "normal"
            print(f"  Switched to {mode} mode.")
            continue
        if mode == "normal":
            op = MENU_MAP.get(choice)
            if op is None:
                print(f"  Unknown choice: {choice!r}. Please enter a number from 1-12, 'h', 'm', or 'q'.")
                continue
        else:
            op = SCIENTIFIC_MENU_MAP.get(choice)
            if op is None:
                print(f"  Unknown choice: {choice!r}. Please enter a number from 1-10, 'h', 'm', or 'q'.")
                continue
        run_operation(calc, op)


if __name__ == "__main__":
    main()
