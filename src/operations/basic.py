"""Basic arithmetic operations: add, subtract, multiply, divide."""


def add(a, b):
    """Return a + b."""
    return a + b


def subtract(a, b):
    """Return a - b."""
    return a - b


def multiply(a, b):
    """Return a * b."""
    return a * b


def divide(a, b):
    """Return a / b; raise ValueError when b is zero."""
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    return a / b
