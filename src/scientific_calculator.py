"""ScientificCalculator: designated extension point for a future scientific mode.

This class inherits all operations from Calculator and serves as the location
where scientific-only functions (e.g. trigonometric, hyperbolic, combinatorial)
should be added when a dedicated scientific mode is introduced.

No such operations have been added yet — this stub exists to give the project a
clear, reviewed place to grow into without requiring structural changes later.
"""

from .calculator import Calculator


class ScientificCalculator(Calculator):
    """Calculator extended for scientific-mode operations.

    All current operations (add, subtract, multiply, divide, factorial, square,
    cube, square_root, cube_root, power, log, ln) are inherited from Calculator.

    Future scientific-only methods (sin, cos, tan, sinh, cosh, combinations,
    permutations, …) belong here.
    """
