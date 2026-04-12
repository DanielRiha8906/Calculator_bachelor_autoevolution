from .calculator import Calculator

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


def show_menu() -> None:
    """Print the operation menu to stdout."""
    print("\n--- Calculator ---")
    for key, name in OPERATIONS.items():
        print(f"  {key}. {name}")
    print("  q. quit")


def parse_number(prompt: str) -> float:
    """Prompt the user until a valid number is entered and return it as float."""
    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print(f"  Invalid number: '{raw}'. Please try again.")


def parse_int(prompt: str) -> int:
    """Prompt the user until a valid integer is entered and return it."""
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print(f"  Invalid integer: '{raw}'. Please try again.")


def run_operation(calc: Calculator, operation: str) -> None:
    """Collect inputs for *operation*, execute it, and print the result."""
    try:
        if operation == "add":
            a = parse_number("  Enter first number: ")
            b = parse_number("  Enter second number: ")
            result = calc.add(a, b)
        elif operation == "subtract":
            a = parse_number("  Enter first number: ")
            b = parse_number("  Enter second number: ")
            result = calc.subtract(a, b)
        elif operation == "multiply":
            a = parse_number("  Enter first number: ")
            b = parse_number("  Enter second number: ")
            result = calc.multiply(a, b)
        elif operation == "divide":
            a = parse_number("  Enter dividend: ")
            b = parse_number("  Enter divisor: ")
            result = calc.divide(a, b)
        elif operation == "factorial":
            n = parse_int("  Enter non-negative integer: ")
            result = calc.factorial(n)
        elif operation == "square":
            a = parse_number("  Enter number: ")
            result = calc.square(a)
        elif operation == "cube":
            a = parse_number("  Enter number: ")
            result = calc.cube(a)
        elif operation == "square_root":
            a = parse_number("  Enter number: ")
            result = calc.square_root(a)
        elif operation == "cube_root":
            a = parse_number("  Enter number: ")
            result = calc.cube_root(a)
        elif operation == "power":
            a = parse_number("  Enter base: ")
            b = parse_number("  Enter exponent: ")
            result = calc.power(a, b)
        elif operation == "log":
            a = parse_number("  Enter number: ")
            base = parse_number("  Enter base: ")
            result = calc.log(a, base)
        elif operation == "ln":
            a = parse_number("  Enter number: ")
            result = calc.ln(a)
        else:
            print(f"  Unknown operation: {operation}")
            return
        print(f"  Result: {result}")
    except ValueError as exc:
        print(f"  Error: {exc}")


def main() -> None:
    """Run the interactive calculator loop until the user quits."""
    calc = Calculator()
    while True:
        show_menu()
        choice = input("Select operation: ").strip().lower()
        if choice == "q":
            print("Goodbye!")
            break
        if choice not in OPERATIONS:
            print(f"  Invalid choice: '{choice}'. Please select a valid option.")
            continue
        run_operation(calc, OPERATIONS[choice])


if __name__ == "__main__":
    main()
