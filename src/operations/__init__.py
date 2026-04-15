"""Operations package for the Calculator.

Organises calculator operations into two modules reflecting the
separation between standard arithmetic and more advanced (scientific)
functionality.  The split establishes a clear structural boundary so
future work on a dedicated scientific-mode interface has an obvious
home in the layout.

Exports:
    BasicOperations — add, subtract, multiply, divide
    ScientificOperations — factorial, square, cube, square_root,
                           cube_root, power, log, ln
"""

from .basic import BasicOperations
from .scientific import ScientificOperations

__all__ = ["BasicOperations", "ScientificOperations"]
