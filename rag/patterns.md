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

<!-- Add further patterns here as they are discovered -->
