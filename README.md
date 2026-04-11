# Calculator — Bachelor Thesis Prototype

A command-line calculator application with two usage modes: a **bash CLI** for scripting and one-off calculations, and a **guided interactive session** for step-by-step use.

This application is part of a bachelor thesis on self-evolving software and serves as the evolving code artefact for experimental runs.

---

## Requirements

- Python 3.12
- No third-party packages are required to run or test the calculator itself

Install development dependencies (testing only):

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## Running the calculator

### CLI mode

Pass the operation name and operand(s) directly on the command line:

```bash
python main.py <operation> [operand1] [operand2]
```

Results are printed to stdout. Errors are printed to stderr and the process exits with code 1.

**Examples:**

```bash
python main.py add 5 7          # 12
python main.py subtract 10 3    # 7
python main.py multiply 4 6     # 24
python main.py divide 15 4      # 3.75
python main.py factorial 5      # 120
python main.py square 9         # 81
python main.py cube 3           # 27
python main.py sqrt 16          # 4.0
python main.py cbrt 27          # 3.0
python main.py power 2 10       # 1024.0
python main.py log10 1000       # 3.0
python main.py ln 1             # 0.0
```

### Interactive mode

Start a guided session that prompts for each value:

```bash
python -m src
# or equivalently
python src/__main__.py
```

The session displays a numbered menu, collects operands one at a time, shows the result, and keeps a running history for the duration of the session.

**Available menu commands:**

| Key | Operation             |
|-----|-----------------------|
| 1   | Add (a + b)           |
| 2   | Subtract (a − b)      |
| 3   | Multiply (a × b)      |
| 4   | Divide (a / b)        |
| 5   | Factorial (n!)        |
| 6   | Square (n²)           |
| 7   | Cube (n³)             |
| 8   | Square root (√n)      |
| 9   | Cube root (∛n)        |
| 10  | Power (base ^ exp)    |
| 11  | Log base-10 (log₁₀n)  |
| 12  | Natural log (ln n)    |
| h   | Show session history  |
| q   | Quit                  |

**Example session:**

```
=== Interactive Calculator ===

Available operations:
   1. Add             (a + b)
   2. Subtract        (a - b)
   ...
  12. ln              Natural log     (ln n)
   h. Show history
   q. Quit

Select operation: 1
Enter first value: 5
Enter second value: 7
Result: 12

Select operation: h
Session history:
  add(5, 7) = 12

Select operation: q
Goodbye!
```

---

## Available operations

### Basic arithmetic (two operands)

| Operation  | Description           | Raises on               |
|------------|-----------------------|-------------------------|
| `add`      | a + b                 | —                       |
| `subtract` | a − b                 | —                       |
| `multiply` | a × b                 | —                       |
| `divide`   | a / b                 | `ZeroDivisionError` when b = 0 |

### Scientific operations (one operand unless noted)

| Operation   | Description             | Raises on                                          |
|-------------|-------------------------|----------------------------------------------------|
| `factorial` | n! (integer only)       | `TypeError` for non-int / bool, `ValueError` for n < 0 |
| `square`    | n²                      | —                                                  |
| `cube`      | n³                      | —                                                  |
| `sqrt`      | √n                      | `ValueError` for n < 0                             |
| `cbrt`      | ∛n (all reals)          | —                                                  |
| `power`     | base ^ exp (two operands)| `ValueError` for complex result (negative base, fractional exp) |
| `log10`     | log₁₀(n)               | `ValueError` for n ≤ 0                             |
| `ln`        | ln(n)                   | `ValueError` for n ≤ 0                             |

**Notes:**
- `factorial` requires a non-negative integer. Floats (e.g., `5.0`) and booleans are rejected.
- `cbrt` works for negative numbers (e.g., `cbrt(-8)` = −2).
- `power` uses `math.pow`; passing a negative base with a fractional exponent raises `ValueError`.
- `divide` performs true division; `divide(7, 2)` returns `3.5`, not `3`.

---

## Session behaviour

### History

Interactive mode records every successful calculation to a session history list. When you press `h`, the current history is displayed in function-call notation:

```
add(5, 7) = 12
sqrt(16) = 4.0
factorial(5) = 120
```

On exit (via `q`, exhausted retries, or keyboard interrupt handled at OS level), the history is written to **`history.txt`** in the working directory. Each session **overwrites** the previous file, so `history.txt` always contains exactly the last session's successful calculations. Calculations that raised an error are not recorded in the history.

### Error logging

Both the CLI and the interactive session write error events to **`error.log`** in the working directory. Log entries are tagged with a source prefix:

- `[cli]` — error originated in CLI mode
- `[interactive]` — error originated in interactive mode

Example log lines:

```
2026-04-11T10:32:01 ERROR [cli] unknown operation 'foobar'
2026-04-11T10:33:15 ERROR [interactive] invalid operand input: invalid literal for int() with base 10: 'abc'
2026-04-11T10:33:45 ERROR [interactive] calculation error in sqrt: square root is not defined for negative numbers
```

The logger is shared across both modes. If both are used in the same process (unusual but possible in tests), log entries from both appear in the same `error.log` file and are distinguishable by the prefix.

### Retry logic

Both modes validate input and retry on bad values:

- **Interactive mode — menu selection:** up to 5 consecutive invalid menu choices are tolerated before the session ends automatically.
- **Interactive mode — operand input:** up to 5 consecutive invalid operand values are tolerated per operand. If all attempts fail, the session ends and history is written.
- **CLI mode:** no retry — a single invalid argument causes an immediate error message and exit code 1.

---

## Code structure

```
Calculator_bachelor_autoevolution/
├── main.py                   # CLI entry point (thin wrapper → src.cli.CLIHandler)
├── src/
│   ├── __init__.py           # Exports Calculator
│   ├── __main__.py           # Interactive entry point (thin wrapper → src.session.InteractiveSession)
│   ├── calculator.py         # Calculator class (inherits BasicOperations + ScientificOperations)
│   ├── cli.py                # CLIHandler, CLI_OPERATIONS map, argument parsing
│   ├── session.py            # InteractiveSession, session history, retry logic
│   ├── error_logger.py       # Shared error logger, setup_error_logging(), get_error_logger()
│   └── operations/
│       ├── __init__.py       # Exports BasicOperations, ScientificOperations
│       ├── basic.py          # BasicOperations mixin: add, subtract, multiply, divide
│       └── scientific.py     # ScientificOperations mixin: factorial, square, cube, sqrt,
│                             #   cbrt, power, log10, ln
├── tests/
│   ├── test_calculator.py    # Unit tests for all Calculator methods
│   ├── test_cli.py           # Integration tests for CLIHandler / CLI argument parsing
│   ├── test_main.py          # Integration tests for InteractiveSession (input mocking)
│   └── test_error_logging.py # Tests for error logger setup, prefixes, and file output
├── artifacts/                # PlantUML architecture diagrams (auto-updated by workflow)
├── progress.md               # Autonomous run logs (required for thesis reproducibility)
└── CLAUDE.md                 # Project safety rules and governance
```

### Module responsibilities

| Module | Responsibility |
|--------|---------------|
| `src/operations/basic.py` | The four arithmetic operations as a mixin |
| `src/operations/scientific.py` | Powers, roots, logarithms, factorial as a mixin |
| `src/calculator.py` | Combines both mixins via multiple inheritance into `Calculator` |
| `src/cli.py` | Argument validation, operand parsing, operation dispatch for CLI |
| `src/session.py` | REPL loop, menu display, operand prompting with retry, history management |
| `src/error_logger.py` | Shared `logging.Logger` instance; file handler attached at startup |
| `main.py` | `python main.py` entry point — sets up logging, delegates to `CLIHandler` |
| `src/__main__.py` | `python -m src` entry point — delegates to `InteractiveSession` |

### Design notes

- `Calculator` uses **mixin-based multiple inheritance**: `BasicOperations` and `ScientificOperations` are separate classes that each provide a focused set of methods. `Calculator` inherits from both and adds no methods of its own.
- Entry points (`main.py`, `src/__main__.py`) are intentionally thin. All logic lives in `src/cli.py` and `src/session.py` so it can be tested independently of `sys.argv` and the process lifecycle.
- Error logging is set up at application startup via `setup_error_logging()`. It is safe to call multiple times (the file handler is added only once). Tests patch this function to avoid writing files during the test run.

---

## Running tests

```bash
pytest
```

All tests are in the `tests/` directory. The test suite covers:

- **`test_calculator.py`** — all 12 operations, edge cases, and error conditions
- **`test_cli.py`** — CLI argument validation, all operations via CLI, error handling
- **`test_main.py`** — interactive session flow, retry logic, history display and persistence
- **`test_error_logging.py`** — error log content, source prefixes, file output

Tests mock `builtins.input` to drive interactive sessions without a terminal, and patch `setup_error_logging` to prevent log files from being created during runs.

---

## Architecture diagrams

PlantUML source files are in `artifacts/`:

- `class_diagram.puml` — class relationships and module structure
- `activity_diagram.puml` — control flow through CLI vs interactive entry points
- `sequence_diagram.puml` — message sequence between entry points, CLI/session modules, and Calculator

These are updated automatically by the `update-diagrams` workflow after each implementation run.
