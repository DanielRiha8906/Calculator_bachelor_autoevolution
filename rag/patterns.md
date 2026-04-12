# Patterns

Recurring patterns, known anti-patterns, and discovered conventions.

<!-- Populated as patterns are discovered across evolution cycles. -->

## Pattern: Python division raises ZeroDivisionError natively

When adding zero-division protection or tests, note that Python's `/` operator
already raises `ZeroDivisionError` for integer or float zero divisors. No
explicit guard is required in Calculator.divide unless a custom error message
or type is needed.
