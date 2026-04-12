# Patterns and Anti-Patterns

## Patterns

### Use pytest.raises for exception testing
When testing that Calculator methods raise exceptions for invalid inputs, use `pytest.raises(<ExceptionType>)` as a context manager. This is the idiomatic pytest approach for asserting expected exceptions.

### Use pytest.approx for float comparisons
When asserting equality of floating-point results, use `pytest.approx(expected)` instead of `==` to avoid false failures due to floating-point rounding (e.g., `0.1 + 0.2 != 0.3` exactly in IEEE 754).

## Anti-Patterns

(None discovered yet — populated as cycles progress)
