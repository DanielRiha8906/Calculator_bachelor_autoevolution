# Calculator

A command-line calculator written in Python 3.12 that supports 12 mathematical operations across three categories. It can be used interactively (menu-driven) or non-interactively (single-shot CLI commands).

This application is the baseline subject of a bachelor thesis on self-evolving software — a system capable of autonomously modifying its own source code.

---

## Features

### Arithmetic operations

| Operation    | Description           | Example               |
|--------------|-----------------------|-----------------------|
| `add`        | Addition (a + b)      | `add 3 5` → `8.0`     |
| `subtract`   | Subtraction (a - b)   | `subtract 10 4` → `6.0` |
| `multiply`   | Multiplication (a * b) | `multiply 3 7` → `21.0` |
| `divide`     | Division (a / b)      | `divide 10 4` → `2.5` |

### Algebraic operations

| Operation     | Description                              | Example                      |
|---------------|------------------------------------------|------------------------------|
| `power`       | Exponentiation (base ^ exp)              | `power 2 10` → `1024.0`      |
| `square`      | Square (a²)                              | `square 5` → `25.0`          |
| `cube`        | Cube (a³)                                | `cube 3` → `27.0`            |
| `sqrt`        | Square root (√a, a ≥ 0)                  | `sqrt 16` → `4.0`            |
| `cbrt`        | Cube root (∛a, supports negatives)       | `cbrt -8` → `-2.0`           |
| `factorial`   | Factorial (n!, n must be a non-negative integer) | `factorial 5` → `120` |

### Transcendental operations

| Operation  | Description                              | Example                         |
|------------|------------------------------------------|---------------------------------|
| `log`      | Logarithm in a given base (default 10)   | `log 1000` → `3.0`              |
| `ln`       | Natural logarithm (log base e)           | `ln 1` → `0.0`                  |

---

## Requirements

- Python 3.12
- No third-party dependencies are needed to run the calculator itself

To install the development and testing dependencies:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## Usage

### Interactive mode

Run without arguments to start a menu-driven session:

```bash
python -m src
```

A numbered menu is displayed. Enter the number of the operation you want to perform, supply the requested values, and the result is printed. The session loops until you choose **0** (Exit).

```
Welcome to the Calculator!

Calculator Operations:
  1.  Add              (a + b)
  2.  Subtract         (a - b)
  3.  Multiply         (a * b)
  4.  Divide           (a / b)
  5.  Factorial        (n!)
  6.  Square           (a^2)
  7.  Cube             (a^3)
  8.  Square Root      (sqrt(a))
  9.  Cube Root        (cbrt(a))
 10.  Power            (base^exp)
 11.  Log              (log_base(a), default base 10)
 12.  Natural Log      (ln(a))
 13.  Show History
  0.  Exit

Select operation: 1
Enter first number: 3
Enter second number: 5
Result: 8.0
```

**Interactive mode notes:**

- Menu option **13** shows the history of all operations performed in the current session.
- Invalid numeric input is retried up to **3 times** before the session ends.
- Three consecutive unknown menu choices also end the session.
- History is cleared at the start of each new session and written to `history.txt`.
- Errors are logged to `calculator_errors.log`.

### CLI (non-interactive) mode

Pass the operation name and required values directly as arguments for single-shot use:

```bash
python -m src <operation> [arguments]
```

The result is printed to stdout and the process exits with code `0`. On error, the message is written to stderr and the process exits with code `1`.

#### Two-operand arithmetic

```bash
python -m src add 3 5          # → 8.0
python -m src subtract 10 4    # → 6.0
python -m src multiply 3 7     # → 21.0
python -m src divide 10 4      # → 2.5
```

#### Power

```bash
python -m src power 2 10       # → 1024.0
```

#### Single-operand operations

```bash
python -m src square 5         # → 25.0
python -m src cube 3           # → 27.0
python -m src sqrt 16          # → 4.0
python -m src cbrt -8          # → -2.0
python -m src ln 1             # → 0.0
```

#### Logarithm (optional base)

```bash
python -m src log 1000         # → 3.0   (base 10 by default)
python -m src log 8 --base 2   # → 3.0   (log₂ 8)
```

#### Factorial

```bash
python -m src factorial 5      # → 120
```

#### Help

```bash
python -m src --help
python -m src add --help
```

---

## Error handling

Each operation raises a descriptive error when given invalid input:

| Situation                                     | Error raised        | Message                                                  |
|-----------------------------------------------|---------------------|----------------------------------------------------------|
| Division by zero                              | `ZeroDivisionError` | "Cannot divide by zero"                                  |
| Square root of a negative number              | `ValueError`        | "Square root is not defined for negative numbers"        |
| Logarithm of a non-positive number            | `ValueError`        | "Logarithm is not defined for non-positive values"       |
| Natural logarithm of a non-positive number    | `ValueError`        | "Natural logarithm is not defined for non-positive values" |
| Factorial of a negative or non-integer number | `ValueError`        | "Factorial requires a non-negative integer"              |

In interactive mode these errors are printed with an `Error:` prefix and the session continues. In CLI mode they are written to stderr and the process exits with code `1`.

---

## Project structure

```
src/
├── __init__.py             # Package init; exports Calculator
├── __main__.py             # Entry point; routes to interactive or CLI mode
├── calculator.py           # Calculator facade (delegates to operations/)
├── controller.py           # CalculatorController — operation dispatch
├── cli.py                  # CLI argument parsing and dispatch
├── error_logger.py         # File-based error logging (calculator_errors.log)
├── history.py              # Session history management (history.txt)
└── operations/
    ├── __init__.py
    ├── arithmetic.py       # add, subtract, multiply, divide
    ├── algebraic.py        # power, square, cube, square_root, cube_root, factorial
    └── transcendental.py   # log, ln

tests/
├── conftest.py
├── test_calculator.py
├── test_controller.py
├── test_cli.py
├── test_main.py
├── test_error_logger.py
├── test_history.py
└── operations/
    ├── test_arithmetic.py
    ├── test_algebraic.py
    └── test_transcendental.py
```

### Architecture overview

`Calculator` is a thin **facade** that exposes all operations as instance methods while delegating computation to the pure functions in `src/operations/`. Adding a new category of operations only requires creating a new module under `src/operations/` and importing it in `calculator.py`.

The **controller** (`CalculatorController`) sits between the UI layers and the `Calculator` instance, mapping operation names to the correct method calls. The two UI layers — interactive (`__main__.py`) and CLI (`cli.py`) — are fully independent and share no code beyond the controller.

---

## Running tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run a specific test file
pytest tests/test_calculator.py

# Run tests for a specific operation category
pytest tests/operations/
```

The test suite contains over 250 tests covering all operations, both UI modes, error logging, and session history.

---

## Generated files

The following files are created at runtime and are excluded from version control:

| File                      | Contents                                         |
|---------------------------|--------------------------------------------------|
| `history.txt`             | Operations and results from the current session  |
| `calculator_errors.log`   | Error log entries with timestamps                |
