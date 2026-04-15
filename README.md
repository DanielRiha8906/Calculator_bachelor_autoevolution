# Calculator

A Python calculator application that supports both an interactive menu-driven mode and a non-interactive command-line (CLI) mode. The calculator provides twelve arithmetic and scientific operations with input validation, session history, and error logging.

---

## Project structure

```
src/
  __init__.py           — package root; exports Calculator
  __main__.py           — entry point; main() dispatches CLI vs interactive mode
  calculator.py         — Calculator class with execute() dispatch method
  operations/
    basic.py            — add, subtract, multiply, divide
    scientific.py       — factorial, square, cube, square_root, cube_root, power, log, ln
  interface/
    history.py          — history.txt and error.log file helpers
    interactive.py      — interactive menu loop components
    cli.py              — non-interactive CLI mode
tests/
  test_calculator.py    — unit tests for Calculator (68 tests)
  test_main.py          — unit tests for interactive and CLI modes (84 tests)
rag/                    — RAG knowledge base (maintained by the evolution engine)
```

---

## Requirements

- Python 3.12 or later
- No third-party dependencies

---

## Running the calculator

### Interactive mode

Start the interactive menu by running the package without arguments:

```bash
python -m src
```

A numbered menu is displayed. Enter the number of the desired operation, then supply the required value(s) when prompted. Enter `h` to display the session history or `q` to quit.

Example session:

```
--- Calculator ---
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
  h. show history
  q. quit
Select operation: 1
  Enter first number: 3
  Enter second number: 4
  Result: 7.0
```

### CLI mode

Execute a single operation and print the result by passing the operation name and value(s) as arguments:

```bash
python -m src <operation> <value> [<value2>]
```

Examples:

```bash
python -m src add 3 4          # prints 7.0
python -m src divide 10 4      # prints 2.5
python -m src factorial 5      # prints 120
python -m src square_root 16   # prints 4.0
python -m src power 2 10       # prints 1024
python -m src log 100 10       # prints 2.0
python -m src ln 1             # prints 0.0
```

On success the result is printed to stdout and the process exits with code 0.
On error a message is printed to stderr and the process exits with code 1.

---

## Available operations

| Menu key | Operation     | Arguments          | Description                                      |
|----------|---------------|--------------------|--------------------------------------------------|
| 1        | `add`         | a, b               | a + b                                            |
| 2        | `subtract`    | a, b               | a − b                                            |
| 3        | `multiply`    | a, b               | a × b                                            |
| 4        | `divide`      | a, b               | a ÷ b (raises error when b = 0)                  |
| 5        | `factorial`   | n (integer ≥ 0)    | n! (raises error for negative or non-integer n)  |
| 6        | `square`      | a                  | a²                                               |
| 7        | `cube`        | a                  | a³                                               |
| 8        | `square_root` | a (≥ 0)            | √a (raises error for negative a)                 |
| 9        | `cube_root`   | a                  | ∛a (supports negative input)                     |
| 10       | `power`       | a, b               | a^b                                              |
| 11       | `log`         | a (> 0), base (> 0, ≠ 1) | log_base(a)                             |
| 12       | `ln`          | a (> 0)            | natural logarithm of a                           |

---

## Input validation

**Interactive mode:**
- Invalid number or integer inputs prompt a retry. After three consecutive invalid inputs for a single prompt the session ends with a `TooManyAttemptsError`.
- Invalid menu choices also count toward a three-strike limit; the session ends when the limit is reached.

**CLI mode:**
- Wrong number of arguments prints a usage error to stderr and exits with code 1.
- Non-numeric values print a type error to stderr and exits with code 1.
- Calculation errors (e.g. division by zero) print the error to stderr and exits with code 1.

---

## Session history

In interactive mode the current session's successful operations are stored in `history.txt` (relative to the working directory). The history is cleared at the start of each new session. Enter `h` at the menu to display the history.

History is not available in CLI mode — each CLI invocation is independent.

---

## Error logging

All invalid inputs and calculation errors are appended to `error.log` (relative to the working directory) with a timestamp:

```
[2026-04-15 12:34:56] invalid_input: 'abc' is not a valid number
[2026-04-15 12:34:57] calculation_error: Division by zero is not allowed
```

The error log persists across sessions (unlike the history which is cleared on each start).

---

## Running the tests

```bash
python -m pytest tests/
```

The test suite contains 152 tests: 68 unit tests for `Calculator` and 84 tests for the interactive and CLI modes.
