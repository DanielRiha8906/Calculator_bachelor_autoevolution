from .calculator import Calculator


UNARY_OPS = {"factorial", "square", "cube", "square_root", "cube_root", "log", "ln"}
BINARY_OPS = {"add", "subtract", "multiply", "divide", "power"}
# Operations that require integer operands
INTEGER_OPS = {"factorial"}

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


def parse_number(prompt: str) -> float:
    """Prompt the user until a valid number is entered."""
    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print(f"  Invalid number: {raw!r}. Please enter a numeric value.")


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


def main() -> None:
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
