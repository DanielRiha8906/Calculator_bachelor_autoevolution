import sys

from .calculator import Calculator


UNARY_OPS = {"factorial", "square", "cube", "square_root", "cube_root", "log", "ln"}
BINARY_OPS = {"add", "subtract", "multiply", "divide", "power"}
# Operations that require integer operands
INTEGER_OPS = {"factorial"}
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
  q. quit
"""

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


def _to_int_if_needed(op: str, value: float) -> "float | int":
    """Convert value to int for operations that require integer operands."""
    if op not in INTEGER_OPS:
        return value
    if value != int(value):
        raise ValueError(f"{op} requires a whole number, got {value}")
    return int(value)


def run_operation(calc: Calculator, op: str) -> None:
    """Execute one calculator operation with user-supplied operands."""
    try:
        if op in BINARY_OPS:
            a = parse_number("  Enter first number: ")
            b = parse_number("  Enter second number: ")
            result = getattr(calc, op)(a, b)
        else:
            a = _to_int_if_needed(op, parse_number("  Enter number: "))
            result = getattr(calc, op)(a)
        print(f"  Result: {result}")
    except (ValueError, ZeroDivisionError) as exc:
        print(f"  Error: {exc}")


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
    all_ops = UNARY_OPS | BINARY_OPS
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
            result = getattr(calc, op)(a, b)
        else:
            if len(operand_args) != 1:
                print(f"Error: {op} requires exactly 1 operand, got {len(operand_args)}")
                return 1
            a = float(operand_args[0])
            a = _to_int_if_needed(op, a)
            result = getattr(calc, op)(a)
    except (ValueError, ZeroDivisionError) as exc:
        print(f"Error: {exc}")
        return 1

    print(_format_result(result))
    return 0


def main() -> None:
    if len(sys.argv) > 1:
        sys.exit(cli_main(sys.argv[1:]))

    calc = Calculator()
    print("Welcome to the Calculator!")
    while True:
        print(MENU)
        choice = input("Choose an operation: ").strip().lower()
        if choice == "q":
            print("Goodbye!")
            break
        op = MENU_MAP.get(choice)
        if op is None:
            print(f"  Unknown choice: {choice!r}. Please enter a number from 1-12 or 'q'.")
            continue
        run_operation(calc, op)


if __name__ == "__main__":
    main()
