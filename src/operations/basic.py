"""Basic arithmetic operations for the calculator.

Defines the four fundamental arithmetic operations: addition, subtraction,
multiplication, and division.  These form the standard four-function
calculator feature set, kept separate from the scientific operation set so
that the two groups can be exposed or extended independently in the future.
"""


class BasicOperations:
    """Mixin providing the four basic arithmetic operations."""

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        return a / b
