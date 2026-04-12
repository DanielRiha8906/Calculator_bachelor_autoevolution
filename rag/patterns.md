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
