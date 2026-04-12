# Patterns

Recurring patterns, known anti-patterns, and discovered conventions.

<!-- Populated as patterns are discovered across evolution cycles. -->

## Pattern: str * int is valid Python — use str * str to trigger TypeError

When writing invalid-type tests for `multiply`, passing a string and an integer
(`"x" * 3`) does NOT raise `TypeError` because Python supports string repetition
via `*`. Use `str * str` (`"x" * "y"`) instead to reliably get `TypeError`.
This quirk applies only to `multiply`; the other three operators (`+`, `-`, `/`)
all raise `TypeError` when given `str` operands with numeric ones.

## Pattern: Use math.isclose for float arithmetic assertions

Never assert exact equality for floating-point results of multiply or divide.
Use `math.isclose(result, expected, rel_tol=1e-9)` to tolerate IEEE-754 rounding
(e.g., `0.1 * 3` ≠ `0.3` exactly in binary floating-point).

## Pattern: Python division raises ZeroDivisionError natively

When adding zero-division protection or tests, note that Python's `/` operator
already raises `ZeroDivisionError` for integer or float zero divisors. No
explicit guard is required in Calculator.divide unless a custom error message
or type is needed.
