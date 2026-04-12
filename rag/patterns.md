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

## Pattern: Retry loop for user input validation

When prompting for a numeric value from the user, loop until a valid value is received rather than raising an exception:

```python
while True:
    raw = input(prompt).strip()
    try:
        return float(raw)
    except ValueError:
        print(f"  Invalid number: '{raw}'. Please try again.")
```

This keeps the UX smooth and avoids exposing internal Python exceptions to the user.

**First observed:** cycle 5, `parse_number` and `parse_int` in `src/__main__.py`

---

<!-- Add further patterns here as they are discovered -->
