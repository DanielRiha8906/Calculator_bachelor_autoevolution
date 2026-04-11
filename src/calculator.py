import math


class Calculator:
    def __init__(self):
        self._history: list[dict] = []

    def _record(self, operation: str, args: list, result) -> None:
        """Append a successful operation to the history list."""
        self._history.append({"operation": operation, "args": args, "result": result})

    def get_history(self) -> list[dict]:
        """Return a copy of the operation history."""
        return list(self._history)

    def clear_history(self) -> None:
        """Clear all recorded history entries."""
        self._history.clear()

    def add(self, a, b):
        result = a + b
        self._record("add", [a, b], result)
        return result

    def subtract(self, a, b):
        result = a - b
        self._record("subtract", [a, b], result)
        return result

    def multiply(self, a, b):
        result = a * b
        self._record("multiply", [a, b], result)
        return result

    def divide(self, a, b):
        result = a / b
        self._record("divide", [a, b], result)
        return result

    def factorial(self, n: int) -> int:
        result = math.factorial(n)
        self._record("factorial", [n], result)
        return result

    def square(self, x: float) -> float:
        result = x ** 2
        self._record("square", [x], result)
        return result

    def cube(self, x: float) -> float:
        result = x ** 3
        self._record("cube", [x], result)
        return result

    def square_root(self, x: float) -> float:
        result = math.sqrt(x)
        self._record("square_root", [x], result)
        return result

    def cube_root(self, x: float) -> float:
        result = math.cbrt(x)
        self._record("cube_root", [x], result)
        return result

    def power(self, base: float, exp: float) -> float:
        result = math.pow(base, exp)
        self._record("power", [base, exp], result)
        return result

    def log(self, x: float) -> float:
        result = math.log10(x)
        self._record("log", [x], result)
        return result

    def ln(self, x: float) -> float:
        result = math.log(x)
        self._record("ln", [x], result)
        return result
