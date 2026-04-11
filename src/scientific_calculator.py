"""ScientificCalculator: extended calculator with trigonometric operations.

This class inherits all operations from Calculator and adds scientific-only
functions (sin, cos, tan) that are only available in scientific mode.

All input angles are in radians.
"""

from .calculator import Calculator
from .operations import scientific


class ScientificCalculator(Calculator):
    """Calculator extended with trigonometric operations for scientific mode.

    All operations from Calculator (add, subtract, multiply, divide, factorial,
    square, cube, square_root, cube_root, power, log, ln) are inherited.

    Scientific-only operations added here:
        sin(x), cos(x), tan(x)  — angles in radians.
    """

    def sin(self, x: float) -> float:
        """Return the sine of *x* (in radians) and record the operation.

        Args:
            x: Angle in radians.

        Returns:
            sin(x)
        """
        result = scientific.sin(x)
        self._record("sin", [x], result)
        return result

    def cos(self, x: float) -> float:
        """Return the cosine of *x* (in radians) and record the operation.

        Args:
            x: Angle in radians.

        Returns:
            cos(x)
        """
        result = scientific.cos(x)
        self._record("cos", [x], result)
        return result

    def tan(self, x: float) -> float:
        """Return the tangent of *x* (in radians) and record the operation.

        Args:
            x: Angle in radians.

        Returns:
            tan(x)

        Raises:
            ValueError: If the result is undefined (cos(x) is effectively zero).
        """
        result = scientific.tan(x)
        self._record("tan", [x], result)
        return result
