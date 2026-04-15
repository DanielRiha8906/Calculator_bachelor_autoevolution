"""Basic arithmetic operations: add, subtract, multiply, divide."""


def add(a: "float | int", b: "float | int") -> "float | int":
    """Return a + b."""
    return a + b


def subtract(a: "float | int", b: "float | int") -> "float | int":
    """Return a - b."""
    return a - b


def multiply(a: "float | int", b: "float | int") -> "float | int":
    """Return a * b."""
    return a * b


def divide(a: "float | int", b: "float | int") -> float:
    """Return a / b. Raises ZeroDivisionError if b is zero."""
    return a / b
