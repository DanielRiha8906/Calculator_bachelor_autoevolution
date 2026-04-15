# Patterns

Recurring patterns, known anti-patterns, and discovered conventions.

<!-- Populated as patterns are discovered across evolution cycles. -->

## Pattern: Python division raises ZeroDivisionError natively

When adding zero-division protection or tests, note that Python's `/` operator
already raises `ZeroDivisionError` for integer or float zero divisors. No
explicit guard is required in Calculator.divide unless a custom error message
or type is needed.

## Pattern: bool is a subclass of int — guard order matters

In Python, `bool` is a subclass of `int`, so `isinstance(True, int)` returns
`True`. When a function should accept integers but reject booleans, check
`isinstance(n, bool)` *before* `isinstance(n, int)`:

```python
if isinstance(n, bool) or not isinstance(n, int):
    raise TypeError(...)
```

Reversing the order causes booleans to pass the integer check silently.
Applied in `Calculator.factorial`.

## Pattern: pytest.approx for floating-point assertions

Calculator operations on floats (e.g. `0.1 + 0.2`, `1.0 / 3.0`) must be
compared with `pytest.approx` rather than `==` to avoid IEEE 754 precision
failures. Apply this pattern to any test involving float operands or results.

## Pattern: cube root of negative numbers requires sign-preservation

Python cannot raise negative floats to fractional powers: `(-8) ** (1/3)` raises
`ValueError` at runtime. The correct approach is:

```python
if x < 0:
    return -(abs(x) ** (1 / 3))
return x ** (1 / 3)
```

This is different from square root: square root of a negative has no real result,
so `ValueError` is correct. Cube root of a negative number *does* have a real result.

## Pattern: mock builtins.input with side_effect list for CLI tests

When testing an interactive loop driven by `input()`, patch `builtins.input`
with `side_effect=list_of_strings`. Each call to `input()` consumes the next
element. If the list runs out before the loop exits, `StopIteration` is raised
— which means every test must include exactly enough inputs (including the
final `"q"`) to reach a clean exit. Patch `builtins.print` in the same
context manager to capture all output without console noise.

```python
with patch("builtins.input", side_effect=["1", "3", "4", "q"]), \
     patch("builtins.print") as mock_print:
    main()
output = [str(a) for call in mock_print.call_args_list for a in call.args]
```

Applied in `tests/test_main.py`.

## Pattern: guard-then-delegate for math domain errors

For operations like log, ln, square_root that have restricted domains, raise
`ValueError` explicitly before calling `math.*` functions. This provides
controlled error messages and makes the contract explicit in the source code,
even though `math.sqrt(-1)` and `math.log(0)` also raise `ValueError`.

## Pattern: internal sentinel exception for loop-break signals

When a helper function inside a loop needs to signal "abort the loop" without
conflating that signal with a normal error, raise a private exception class
(e.g. `_SessionExpired`) that does NOT inherit from the exceptions the loop
already catches. The loop's outer except block catches it and breaks.

```python
class _SessionExpired(Exception):
    """Raised internally when retries are exhausted."""

def get_number_with_retry(prompt):
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            return get_number(prompt)
        except ValueError:
            if attempt == MAX_ATTEMPTS:
                raise _SessionExpired()

# In main():
try:
    a = get_number_with_retry("Enter number: ")
except _SessionExpired:
    break
except (ValueError, TypeError, ZeroDivisionError) as exc:
    print(f"Error: {exc}")
```

Applied in `src/__main__.py` for operand-input retry termination.

## Pattern: import MAX_ATTEMPTS in tests instead of hardcoding retry counts

When testing retry-count-dependent behaviour, import the constant from the
module under test so tests do not need to be updated when the constant changes.

```python
from src.__main__ import main, MAX_ATTEMPTS

def test_session_terminates():
    inputs = ["99"] * MAX_ATTEMPTS
    output = run_main_with_inputs(inputs)
    assert output_contains(output, "Maximum attempts")
```

Applied in `tests/test_main.py`.

## Pattern: avoid default-arg capture for patchable module constants

When a module-level constant (e.g. `HISTORY_FILE`) needs to be patchable in
tests, do NOT use it as a default argument value:

```python
# Anti-pattern: default captured at definition time — patch has no effect
def save_history(history, path=HISTORY_FILE):
    ...

# Correct: look up constant at call time
def save_history(history, path=None):
    if path is None:
        path = HISTORY_FILE
    ...
```

Tests can then `patch("src.__main__.HISTORY_FILE", tmp_path)` and the function
will pick up the patched value. Applied in `save_history` / `tests/test_main.py`.

## Pattern: keep thin wrapper functions for test backward compatibility

When refactoring a module-level function into a class method, keep the
original function as a one-line wrapper that delegates to the class method.
This avoids breaking existing tests that import the function directly,
while still achieving the desired separation of concerns.

```python
# Before (in src/__main__.py):
def format_history_entry(name, args, result):
    args_str = ", ".join(str(a) for a in args)
    return f"{name}({args_str}) = {result}"

# After: logic moved to CalculatorSession.format_entry; wrapper preserved
def format_history_entry(name, args, result):
    return CalculatorSession.format_entry(name, args, result)
```

Applied in `src/__main__.py` for `format_history_entry` during the
logic-separation refactor (issue-271).

## Pattern: centralise operation metadata to eliminate duplication

When multiple entry points (interactive CLI, bash CLI) need to know which
operations take one vs two operands, define `BINARY_OPS`/`UNARY_OPS`/`ALL_OPS`
in a single shared module and import from there. Avoid duplicating these sets.

Before issue-271: `main.py` defined `_BINARY_OPS`, `_UNARY_OPS`, `_ALL_OPS`
independently from `__main__.py`'s `OPERATIONS` dict. These could drift.
After: both import from `src.session`.

## Pattern: multiple inheritance for composable operation mixins

When an application needs a unified class that combines disjoint groups
of methods (e.g., basic vs. scientific operations), define each group as
a standalone mixin class and combine them via multiple inheritance:

```python
# src/operations/basic.py
class BasicOperations:
    def add(self, a, b): ...
    def divide(self, a, b): ...

# src/operations/scientific.py
class ScientificOperations:
    def factorial(self, n): ...
    def log(self, x): ...

# src/calculator.py
class Calculator(BasicOperations, ScientificOperations):
    """Thin class: inherits all ops, adds nothing."""
```

Benefits:
- Each mixin is independently testable and importable.
- The module names (`basic.py`, `scientific.py`) make the structural
  boundary visible in the file tree without adding a class hierarchy.
- The unified `Calculator` type remains the single public name for all
  callers; no downstream code requires modification.

Applied in `src/operations/` (issue-275).  The `BINARY_OPS`/`UNARY_OPS`
arity metadata is kept separate in `session.py` because arity is a
session-dispatch concern, not an operation-implementation concern.

## Pattern: mode-keyed operation dicts for multi-mode interactive CLIs

When an interactive CLI needs to support multiple modes with different
operation sets, define separate dicts for each mode and store the active
dict in a variable. The loop dispatches against the active dict, and a
mode-switch command swaps the variable.

```python
NORMAL_OPERATIONS  = {"1": ("add", 2), "5": ("square", 1), ...}
SCIENTIFIC_OPERATIONS = {**NORMAL_OPERATIONS, "7": ("factorial", 1), ...}

current_ops = NORMAL_OPERATIONS
if user_input == "m":
    current_ops = SCIENTIFIC_OPERATIONS   # or back to NORMAL
```

Benefits:
- The loop body is identical for all modes; no if/else per mode.
- `display_menu(current_ops, mode_name)` always shows exactly the right ops.
- Tests for basic ops work without mode-switch input (same keys in both modes).
- Tests for advanced ops prefix inputs with `["m", "2", ...]`.

Applied in `src/__main__.py` (issue-281).

## Pattern: autouse conftest fixture for cross-cutting side effects

When a feature produces side effects (file writes, network calls) on every error path,
patching it per-test is impractical. Instead, place an autouse fixture in `tests/conftest.py`
that applies the patch for the entire test session. The fixture yields any per-test data
(e.g., the temporary path) so individual tests that need to inspect the side effect can
use it as a named fixture argument:

```python
# tests/conftest.py
@pytest.fixture(autouse=True)
def isolate_error_log(tmp_path):
    log_path = str(tmp_path / "error.log")
    with patch("src.error_logger.ERROR_LOG_FILE", log_path):
        yield log_path

# In a test file:
def test_something_is_logged(isolate_error_log, capsys):
    run_cli(["divide", "5", "0"], capsys)
    with open(isolate_error_log) as fh:
        assert "divide" in fh.read()
```

Tests that do not care about logging work unchanged because the autouse patch is invisible.
Applied in `tests/conftest.py` / `tests/test_error_logger.py`, `tests/test_cli.py`, `tests/test_main.py`.
