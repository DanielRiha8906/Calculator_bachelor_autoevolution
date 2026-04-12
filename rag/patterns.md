# Patterns and Anti-Patterns

## Patterns

### Use pytest.raises for exception testing
When testing that Calculator methods raise exceptions for invalid inputs, use `pytest.raises(<ExceptionType>)` as a context manager. This is the idiomatic pytest approach for asserting expected exceptions.

### Use pytest.approx for float comparisons
When asserting equality of floating-point results, use `pytest.approx(expected)` instead of `==` to avoid false failures due to floating-point rounding (e.g., `0.1 + 0.2 != 0.3` exactly in IEEE 754).

### Float-to-int conversion for stdlib functions expecting integers
When user input arrives as `float` (via `parse_number`) but a Calculator method requires `int` (e.g., `factorial` which calls `math.factorial`), check `value != int(value)` and raise `ValueError` for non-whole numbers before casting. This avoids a confusing `TypeError: 'float' object cannot be interpreted as an integer` from the stdlib.

## Anti-Patterns

(None discovered yet — populated as cycles progress)
