"""Calculator: unified class combining basic and scientific operations.

All twelve supported operations are inherited from two focused mixin classes:

- :class:`~src.operations.basic.BasicOperations` —
  add, subtract, multiply, divide
- :class:`~src.operations.scientific.ScientificOperations` —
  factorial, square, cube, square_root, cube_root, power, log, ln

This structure keeps the implementation of each category self-contained
and gives future scientific-mode work an obvious home in
``src/operations/scientific.py`` without requiring any changes to the
rest of the codebase.
"""

from .operations.basic import BasicOperations
from .operations.scientific import ScientificOperations


class Calculator(BasicOperations, ScientificOperations):
    """Full calculator combining basic arithmetic and scientific operations.

    Inherits all twelve operations from :class:`BasicOperations` and
    :class:`ScientificOperations`.  The class itself adds no new behaviour;
    its purpose is to provide a single named type that the rest of the
    application (session dispatch, tests, CLI) can depend on.

    Example::

        calc = Calculator()
        calc.add(2, 3)          # 5
        calc.factorial(5)       # 120
        calc.square_root(9)     # 3.0
    """
