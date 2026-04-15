# Calculator

A Python calculator application that supports arithmetic and advanced mathematical
operations via an interactive REPL or a non-interactive CLI.

## Requirements

- Python 3.11+
- Dependencies: see `requirements.txt`

## Installation

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### Interactive REPL

```bash
python -m src
```

A menu is shown. Enter the number of the desired operation, then provide the
requested operand(s).  Special commands:

| Input | Action |
|-------|--------|
| `h`   | Show operation history |
| `q`   | Quit |

### CLI (non-interactive)

```bash
python -m src <operation> [operands...]
```

Binary operations (two operands):

```bash
python -m src add 3 4          # 7
python -m src subtract 10 3    # 7
python -m src multiply 6 7     # 42
python -m src divide 22 7      # 3.142857142857143
python -m src power 2 10       # 1024
```

Unary operations (one operand):

```bash
python -m src factorial 5      # 120
python -m src square 9         # 81
python -m src cube 3           # 27
python -m src square_root 16   # 4
python -m src cube_root 27     # 3.0
python -m src log 100          # 2.0
python -m src ln 1             # 0.0
```

Exit codes: `0` on success, `1` on error (message printed to stdout).

## Supported Operations

| Operation    | Arity  | Description                        |
|--------------|--------|------------------------------------|
| `add`        | binary | a + b                              |
| `subtract`   | binary | a − b                              |
| `multiply`   | binary | a × b                              |
| `divide`     | binary | a ÷ b (raises error if b = 0)      |
| `power`      | binary | base ^ exp                         |
| `factorial`  | unary  | n! (integer n ≥ 0 required)        |
| `square`     | unary  | n²                                 |
| `cube`       | unary  | n³                                 |
| `square_root`| unary  | √n (n ≥ 0 required)               |
| `cube_root`  | unary  | ∛n (handles negative values)       |
| `log`        | unary  | log₁₀(n) (n > 0 required)         |
| `ln`         | unary  | ln(n) (n > 0 required)             |

## Project Structure

```
src/
  __init__.py          # Package init; exports Calculator
  __main__.py          # CLI and interactive REPL entry point
  calculator.py        # Calculator class: history, logging, dispatch
  operations/
    __init__.py        # Re-exports all operation functions
    arithmetic.py      # add, subtract, multiply, divide
    advanced.py        # factorial, square, cube, roots, power, log, ln
    scientific.py      # Placeholder for future scientific operations
tests/
  test_calculator.py   # Unit/integration tests for Calculator class
  test_main.py         # Tests for CLI and REPL interface layer
```

## Running Tests

```bash
pytest
```
