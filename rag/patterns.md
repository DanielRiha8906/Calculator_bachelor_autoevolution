# Patterns

Recurring patterns, known anti-patterns, and discovered conventions.

## Pattern: Explicit error over raw Python exception

When a method can receive invalid input (e.g., zero divisor), raise a `ValueError` with a descriptive message rather than allowing Python to raise a low-level exception like `ZeroDivisionError`. This makes the public API contract explicit and makes test assertions straightforward (`pytest.raises(ValueError, match=...)`).

**First observed:** cycle 1, `Calculator.divide`

---

<!-- Add further patterns here as they are discovered -->
