from .calculator import Calculator

MENU = (
    "\nCalculator Operations:\n"
    "  1.  Add              (a + b)\n"
    "  2.  Subtract         (a - b)\n"
    "  3.  Multiply         (a * b)\n"
    "  4.  Divide           (a / b)\n"
    "  5.  Factorial        (n!)\n"
    "  6.  Square           (a^2)\n"
    "  7.  Cube             (a^3)\n"
    "  8.  Square Root      (sqrt(a))\n"
    "  9.  Cube Root        (cbrt(a))\n"
    " 10.  Power            (base^exp)\n"
    " 11.  Log              (log_base(a), default base 10)\n"
    " 12.  Natural Log      (ln(a))\n"
    "  0.  Exit\n"
)


def display_menu() -> None:
    """Print the operation menu to stdout."""
    print(MENU)


def get_number(prompt: str) -> float:
    """Read a numeric value from stdin, retrying on invalid input."""
    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print(f"Invalid input '{raw}': please enter a numeric value.")


def get_integer(prompt: str) -> int:
    """Read an integer value from stdin, retrying on invalid input."""
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print(f"Invalid input '{raw}': please enter a whole number.")


def perform_operation(calc: Calculator, choice: str) -> "str | None":
    """Execute the calculator operation identified by *choice*.

    Prompts for required operands via stdin.  Returns the result as a
    string, or None if *choice* is not a recognised operation number.
    Propagates ValueError and ZeroDivisionError raised by the Calculator.
    """
    if choice == "1":
        a = get_number("Enter first number: ")
        b = get_number("Enter second number: ")
        return str(calc.add(a, b))
    if choice == "2":
        a = get_number("Enter first number: ")
        b = get_number("Enter second number: ")
        return str(calc.subtract(a, b))
    if choice == "3":
        a = get_number("Enter first number: ")
        b = get_number("Enter second number: ")
        return str(calc.multiply(a, b))
    if choice == "4":
        a = get_number("Enter first number: ")
        b = get_number("Enter second number: ")
        return str(calc.divide(a, b))
    if choice == "5":
        n = get_integer("Enter a non-negative integer: ")
        return str(calc.factorial(n))
    if choice == "6":
        a = get_number("Enter a number: ")
        return str(calc.square(a))
    if choice == "7":
        a = get_number("Enter a number: ")
        return str(calc.cube(a))
    if choice == "8":
        a = get_number("Enter a number: ")
        return str(calc.square_root(a))
    if choice == "9":
        a = get_number("Enter a number: ")
        return str(calc.cube_root(a))
    if choice == "10":
        base = get_number("Enter base: ")
        exp = get_number("Enter exponent: ")
        return str(calc.power(base, exp))
    if choice == "11":
        a = get_number("Enter a number: ")
        base_raw = input("Enter log base (press Enter for base 10): ").strip()
        if base_raw:
            try:
                log_base = float(base_raw)
            except ValueError:
                print(f"Invalid base '{base_raw}': using base 10.")
                log_base = 10.0
        else:
            log_base = 10.0
        return str(calc.log(a, log_base))
    if choice == "12":
        a = get_number("Enter a number: ")
        return str(calc.ln(a))
    return None


def main() -> None:
    """Run the interactive calculator session."""
    calc = Calculator()
    print("Welcome to the Calculator!")

    while True:
        display_menu()
        choice = input("Select operation: ").strip()

        if choice == "0":
            print("Goodbye!")
            break

        try:
            result = perform_operation(calc, choice)
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
            continue

        if result is None:
            print(f"Unknown operation '{choice}'. Please choose a number between 0 and 12.")
        else:
            print(f"Result: {result}")


if __name__ == "__main__":
    import sys
    if sys.argv[1:]:
        from .cli import cli_main
        cli_main()
    else:
        main()
