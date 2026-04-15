# Calculator

A Python calculator application that supports both a guided interactive mode and a bash-based CLI. It provides 12 arithmetic and scientific operations, records session history, and logs errors to a local file.

---

## Requirements

- Python 3.12
- `pytest` (for running tests)

Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## Running the calculator

### Interactive mode

Launches a menu-driven session that accepts one operation at a time until you quit or exhaust retries.

```bash
python -m src
```

Example session:

```
Available operations:
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
  11. log
  12. ln
  h. history
  q. quit

Enter operation number (or 'q' to quit): 1
Enter first number: 5
Enter second number: 3
Result: 8

Enter operation number (or 'q' to quit): h
Session history:
  add(5, 3) = 8

Enter operation number (or 'q' to quit): q
Goodbye!
```

**Menu keys:**
- Enter the number shown next to an operation to select it.
- `h` — display the history of all successful calculations in the current session.
- `q` — quit the session (history is saved to `history.txt`).

**Retry behavior:**
- Invalid operation selection: the session allows up to 5 invalid selections in total before terminating.
- Invalid operand input: each individual prompt allows up to 5 failed attempts before the session terminates.
- Each failed attempt logs an entry to `error.log` and shows how many tries remain.

### Bash CLI mode

Runs a single calculation non-interactively and exits. Useful in scripts or pipelines.

```bash
python main.py <operation> <operand>              # unary operations
python main.py <operation> <operand1> <operand2>  # binary operations
```

Examples:

```bash
python main.py add 5 7          # prints: 12
python main.py factorial 5      # prints: 120
python main.py square_root 16   # prints: 4.0
python main.py power 2 10       # prints: 1024
python main.py divide 1 0       # prints error to stderr, exits 1
```

**Exit codes:**
- `0` — success; result is printed to stdout.
- `1` — argument error or calculation error; description is printed to stderr.

---

## Available operations

### Basic arithmetic (two operands)

| Operation  | Description                                | Example                      |
|------------|--------------------------------------------|------------------------------|
| `add`      | Addition                                   | `add 5 3` → `8`              |
| `subtract` | Subtraction                                | `subtract 10 4` → `6`        |
| `multiply` | Multiplication                             | `multiply 3 7` → `21`        |
| `divide`   | Division (raises error when divisor is 0)  | `divide 10 4` → `2.5`        |
| `power`    | Exponentiation                             | `power 2 8` → `256`          |

### Scientific (one operand)

| Operation     | Description                                                          | Example                           |
|---------------|----------------------------------------------------------------------|-----------------------------------|
| `factorial`   | `n!` — integer input only; raises error for negative or float input  | `factorial 5` → `120`             |
| `square`      | `x²`                                                                 | `square 4` → `16`                 |
| `cube`        | `x³`                                                                 | `cube 3` → `27`                   |
| `square_root` | Square root; raises error for negative input                         | `square_root 9` → `3.0`           |
| `cube_root`   | Real cube root; works for negative input (returns negative result)   | `cube_root -8` → `-2.0`           |
| `log`         | Base-10 logarithm; raises error for non-positive input               | `log 100` → `2.0`                 |
| `ln`          | Natural logarithm; raises error for non-positive input               | `ln 1` → `0.0`                    |

---

## Local session files

### `history.txt`

Written at the end of every interactive session. Contains one entry per successful calculation, in function-call format:

```
add(5, 3) = 8
factorial(5) = 120
square_root(9) = 3.0
```

The file is overwritten at the start of each new session, so it always reflects only the most recent run. The bash CLI mode does not write to this file.

### `error.log`

All errors from both modes are appended to `error.log` in the working directory. Each entry uses ISO-8601 timestamps and identifies the source mode:

```
2026-04-15T12:00:00 [interactive] unknown operation '99'
2026-04-15T12:00:01 [interactive] invalid operand input: invalid literal for int()...
2026-04-15T12:01:00 [cli] error in 'divide': division by zero
```

Sources:
- `interactive` — entries from the menu-driven session (`python -m src`).
- `cli` — entries from the bash CLI (`python main.py`).

The file grows across invocations (append mode). It is never cleared automatically.

---

## Code structure

```
.
├── main.py                        # Bash CLI entry point
├── requirements.txt
├── src/
│   ├── __init__.py                # Re-exports Calculator, CalculatorSession
│   ├── __main__.py                # Interactive CLI (python -m src)
│   ├── calculator.py              # Calculator class (inherits both operation mixins)
│   ├── error_logger.py            # log_error(); writes to error.log
│   ├── session.py                 # CalculatorSession + operation arity metadata
│   └── operations/
│       ├── __init__.py            # Re-exports BasicOperations, ScientificOperations
│       ├── basic.py               # add, subtract, multiply, divide
│       └── scientific.py          # factorial, square, cube, square_root, cube_root, power, log, ln
└── tests/
    ├── conftest.py                # autouse fixture: redirects error.log to tmp_path
    ├── test_calculator.py         # 76 tests for Calculator
    ├── test_cli.py                # 34 tests for main.py (bash CLI)
    ├── test_error_logger.py       # 7 tests for error_logger
    ├── test_main.py               # 56 tests for src/__main__.py (interactive CLI)
    └── test_session.py            # 37 tests for CalculatorSession
```

### Key modules

**`src/operations/basic.py` — `BasicOperations`**
Mixin class with the four standard arithmetic operations. Uses only Python built-in operators; no external imports.

**`src/operations/scientific.py` — `ScientificOperations`**
Mixin class with the eight advanced operations. Uses `math` for `sqrt`, `log`, and `log10`. All domain guards (negative inputs, etc.) are applied explicitly before delegating to `math`.

**`src/calculator.py` — `Calculator`**
Thin class that inherits `BasicOperations` and `ScientificOperations` via multiple inheritance. Adds no methods of its own. Provides the single named type used throughout the rest of the application.

**`src/session.py` — `CalculatorSession`**
Centralises operation dispatch and session history. `execute(name, *args)` calls the appropriate `Calculator` method, records the entry, and returns the result. Failed calls (any exception) are not recorded in history. Also defines the authoritative operation arity metadata (`BINARY_OPS`, `UNARY_OPS`, `ALL_OPS`) used by both CLIs.

**`src/__main__.py` — interactive CLI**
Menu-driven session loop. Reads user input, delegates computation to `CalculatorSession`, and manages retry logic (`MAX_ATTEMPTS = 5`). Writes history to `history.txt` on every exit path.

**`main.py` — bash CLI**
Non-interactive, one-shot entry point. Parses positional arguments, runs the requested operation via `CalculatorSession`, and exits with code 0 or 1.

**`src/error_logger.py` — `log_error`**
Appends timestamped error entries to `error.log`. Called by both CLIs on any invalid input or calculation failure.

---

## Running tests

```bash
pytest
```

All 209 tests run from the repository root. The `conftest.py` autouse fixture redirects `error.log` writes to a temporary directory so tests never touch the real log file.

To run a specific test file:

```bash
pytest tests/test_calculator.py
pytest tests/test_cli.py
pytest tests/test_main.py -v
```
