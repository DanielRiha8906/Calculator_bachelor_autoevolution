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
