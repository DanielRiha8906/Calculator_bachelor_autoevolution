# Patterns

Recurring patterns, known anti-patterns, and discovered conventions.

## Pattern: Explicit error over raw Python exception

When a method can receive invalid input (e.g., zero divisor), raise a `ValueError` with a descriptive message rather than allowing Python to raise a low-level exception like `ZeroDivisionError`. This makes the public API contract explicit and makes test assertions straightforward (`pytest.raises(ValueError, match=...)`).

**First observed:** cycle 1, `Calculator.divide`

---

## Pattern: Use math.isclose for float assertions

When asserting equality for results that may involve floating-point arithmetic (floats as inputs or outputs), use `math.isclose(result, expected)` rather than `==`. This avoids failures caused by IEEE 754 representation errors (e.g., `1.1 + 2.2 != 3.3` in exact arithmetic).

**First observed:** cycle 2, `tests/test_calculator.py` (add, subtract, multiply, divide float tests)

---

## Pattern: Sign-preserving real cube root for negative inputs

Python's `a ** (1/3)` returns a complex number when `a` is negative (e.g., `(-8) ** (1/3)` is not `-2.0`). To compute a real cube root for negative inputs, use the sign-preserving idiom:

```python
if a < 0:
    return -((-a) ** (1 / 3))
return a ** (1 / 3)
```

**First observed:** cycle 4, `Calculator.cube_root`

---

## Pattern: Isolate I/O into small helpers for testability

When a CLI module uses `input()`, extract each distinct responsibility (`parse_number`, `parse_int`, `run_operation`) into its own function so that each piece can be tested independently with `unittest.mock.patch("builtins.input", ...)`. Keeping `main()` as a thin loop over these helpers makes integration tests straightforward without requiring complex subprocess invocations.

**First observed:** cycle 5, `src/__main__.py` interactive loop

---

## Pattern: Bounded retry loop with TooManyAttemptsError

When prompting for a numeric value from the user, allow a fixed number of attempts (`MAX_ATTEMPTS`) and raise a custom `TooManyAttemptsError` if they are all exhausted. This prevents the session from hanging indefinitely on invalid input and gives the caller a clean way to end the session:

```python
for attempt in range(1, max_attempts + 1):
    raw = input(prompt).strip()
    try:
        return float(raw)
    except ValueError:
        remaining = max_attempts - attempt
        if remaining > 0:
            print(f"  Invalid number: '{raw}'. Please try again ({remaining} attempt(s) left).")
        else:
            print(f"  Invalid number: '{raw}'. No attempts remaining.")
raise TooManyAttemptsError("Too many invalid number inputs. Ending session.")
```

The caller (interactive loop in `main()`) catches `TooManyAttemptsError` and breaks. CLI mode never retries — explicit number validation returns `1` immediately.

**First observed:** cycle 7, `parse_number` and `parse_int` in `src/__main__.py` (replaces unbounded while-True retry from cycle 5)

---

## Pattern: Explicit args parameter to isolate entry points from sys.argv

When a `main()` function conditionally reads `sys.argv[1:]` to select between modes (e.g., interactive vs. CLI), expose an explicit `args: list[str] | None = None` parameter:

```python
def main(args: list[str] | None = None) -> None:
    if args is None:
        args = sys.argv[1:]
    if args:
        sys.exit(cli_mode(args))
    # interactive mode ...
```

Callers that need a specific mode (test suites, programmatic use) pass the list directly. The production entry point (`if __name__ == "__main__": main()`) picks up `sys.argv` automatically. This prevents test harnesses (e.g., pytest's own CLI args) from accidentally triggering the wrong mode.

**First observed:** cycle 6, `main()` in `src/__main__.py` (CLI mode addition)

---

## Pattern: Group operations by arity for CLI dispatch

When a CLI accepts multiple operations with different numbers of arguments, define explicit sets grouping them by arity and argument type:

```python
_ONE_ARG_OPS = {"square", "cube", "square_root", "cube_root", "ln"}
_INT_ARG_OPS = {"factorial"}
_TWO_ARG_OPS = {"add", "subtract", "multiply", "divide", "power", "log"}
```

Then dispatch with a simple `if op in _INT_ARG_OPS / elif op in _ONE_ARG_OPS / else` tree and use `getattr(calc, op)(...)` to avoid a full 12-branch if/elif. Keeps argument validation centralized and makes adding new operations straightforward.

**First observed:** cycle 6, `cli_mode()` in `src/__main__.py`

---

## Pattern: None-sentinel default for patchable module-level constants

When a function uses a module-level constant as its default argument, binding the constant at definition time prevents test isolation via `monkeypatch.setattr`. Use `None` as the sentinel and resolve the real value inside the function body:

```python
HISTORY_FILE = "history.txt"

def clear_history(filepath: str | None = None) -> None:
    if filepath is None:
        filepath = HISTORY_FILE   # read module attribute at call time
    with open(filepath, "w") as fh:
        fh.write("")
```

Tests that need a different path simply `monkeypatch.setattr(mod, "HISTORY_FILE", tmp_path / "h.txt")` without touching the function signature. Tests that call the function with an explicit path continue to work as before.

**First observed:** cycle 8, `clear_history` / `append_to_history` / `show_history` in `src/__main__.py`

---

## Pattern: Separate error log from operation history

When a CLI records both successful operations (history) and failures (errors), keep them in distinct files rather than mixing them into a single log. This makes both files easier to read and reason about:

- `history.txt` — one line per successful operation, cleared at session start.
- `error.log` — append-only timestamped error records, never cleared (survives across sessions).

The error log helper mirrors the history helpers in signature and uses the same `None`-sentinel pattern:

```python
ERROR_LOG_FILE = "error.log"

def append_to_error_log(message: str, filepath: str | None = None) -> None:
    if filepath is None:
        filepath = ERROR_LOG_FILE
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filepath, "a", encoding="utf-8") as fh:
        fh.write(f"[{timestamp}] {message}\n")
```

The autouse test fixture must redirect **both** constants to `tmp_path` so tests stay isolated.

**First observed:** cycle 9, `append_to_error_log` in `src/__main__.py`

---

## Pattern: Negative test to verify error-only logging

When a function should write to an error log only on failure, add a negative test that asserts the log file does not exist after a successful call. This is simpler than checking the file is empty (which would require creating the file first) and guarantees no false-positive log entries:

```python
def test_success_does_not_log_error(tmp_path, monkeypatch):
    log_path = str(tmp_path / "e.log")
    monkeypatch.setattr(_main_mod, "ERROR_LOG_FILE", log_path)
    # perform a successful operation
    ...
    import os
    assert not os.path.exists(log_path)
```

**First observed:** cycle 9, error log tests in `tests/test_main.py`

---

## Pattern: Logic-layer dispatch method for name-based operation routing

When a class has multiple operation methods and callers need to route by name (e.g. from a menu choice or a CLI argument), add a single `execute(operation, *args)` method to the logic class rather than requiring callers to use `getattr` directly:

```python
def execute(self, operation: str, *args):
    method = getattr(self, operation, None)
    if method is None or not callable(method):
        raise ValueError(f"Unknown operation: '{operation}'")
    return method(*args)
```

This keeps `getattr` logic inside the logic class, raises a clear `ValueError` for unknown names, and gives callers a stable API that does not expose Python introspection. The UI layer calls `calc.execute(op, *args)` and never needs to import individual method names.

**First observed:** cycle 10, `Calculator.execute` in `src/calculator.py`

---

## Pattern: Separate prompt metadata from arity metadata

When a CLI module collects user input for multiple operations with different prompts and arities, keep these as two separate data structures rather than one combined one:

- `_ONE_ARG_OPS / _INT_ARG_OPS / _TWO_ARG_OPS` — control *how many* arguments to collect and what type.
- `_OP_PROMPTS` — control *what text* to display when collecting each argument.

This keeps single responsibility: arity sets change when new operations are added; prompt sets change when UX copy changes. Merging them into one structure couples two unrelated change axes.

**First observed:** cycle 10, `_OP_PROMPTS` in `src/__main__.py`

---

## Pattern: Monkeypatch targets must follow constants to their owning module

When a module constant (e.g. `HISTORY_FILE`) is used as a default via the None-sentinel pattern, `monkeypatch.setattr` must target the module that **owns** the constant — i.e., the module whose attribute the function reads at call time. Re-exporting the constant in another module (e.g. `src.__main__`) does NOT redirect the read; it only creates a second name binding that is independent of the original.

Example: after moving `HISTORY_FILE` from `src.__main__` to `src.interface.history`, tests must patch `src.interface.history.HISTORY_FILE`:

```python
import src.interface.history as _history_mod

monkeypatch.setattr(_history_mod, "HISTORY_FILE", str(tmp_path / "history.txt"))
```

Patching `src.__main__.HISTORY_FILE` would update the re-exported name but leave `src.interface.history.HISTORY_FILE` unchanged, so `clear_history()` would still write to the original path.

**First observed:** cycle 11, `tests/test_main.py` — splitting `src/__main__.py` into interface sub-modules required updating all monkeypatch targets from `_main_mod` to `_history_mod`.

---

## Pattern: Thin Calculator class wrapping pure operation functions

When operation logic is extracted into standalone pure functions (e.g., `src/operations/basic.py`), the Calculator class becomes a thin object-oriented wrapper:

```python
from .operations.basic import add as _add

class Calculator:
    def add(self, a, b):
        return _add(a, b)
```

This keeps the public `Calculator` API unchanged (existing tests and callers require no update) while separating the computation logic into importable, independently testable functions. Adding new operation categories (e.g., `src/operations/statistics.py`) requires only a new module + Calculator wrapper methods — no changes to interface code.

**First observed:** cycle 11, `src/calculator.py` delegating to `src/operations/basic.py` and `src/operations/scientific.py`.

---

## Pattern: Mode-scoped operation dicts for feature-gating in interactive menus

When an interactive menu should expose different operations to users depending on an active mode (e.g., normal vs. scientific), define one dict per mode rather than a single combined dict with conditional visibility:

```python
NORMAL_MODE_OPERATIONS = {"1": "add", "2": "subtract", ...}
SCIENTIFIC_MODE_OPERATIONS = {**NORMAL_MODE_OPERATIONS, "5": "factorial", ...}
OPERATIONS = SCIENTIFIC_MODE_OPERATIONS  # backward-compatible alias
```

The interactive loop tracks `current_ops = NORMAL_MODE_OPERATIONS` by default and switches to `SCIENTIFIC_MODE_OPERATIONS` on toggle. All choice validation (`if choice not in current_ops`) and dispatch (`current_ops[choice]`) use the same reference. The underlying `run_operation` and `Calculator` layers are mode-agnostic and remain unchanged.

This keeps mode state local to the loop, avoids conditional logic scattered through menu rendering, and lets CLI mode (which has no mode concept) keep using `OPERATIONS` unchanged.

**First observed:** cycle 13, `NORMAL_MODE_OPERATIONS` / `SCIENTIFIC_MODE_OPERATIONS` in `src/interface/interactive.py`.

---

<!-- Add further patterns here as they are discovered -->
