"""Basic arithmetic operations for the Calculator.

Contains the four standard arithmetic operations that form the core of
any calculator mode (normal or scientific).
"""


class BasicOperations:
    """Standard arithmetic: addition, subtraction, multiplication, division.

    These operations are the common foundation shared by both the normal
    and any future scientific calculator mode.
    """

    def add(self, a, b):
        """Return a + b."""
        return a + b

    def subtract(self, a, b):
        """Return a - b."""
        return a - b

    def multiply(self, a, b):
        """Return a * b."""
        return a * b

    def divide(self, a, b):
        """Return a / b.

        Raises:
            ZeroDivisionError: if b is zero (raised by Python's / operator).
        """
        return a / b
