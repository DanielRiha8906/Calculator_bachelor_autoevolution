"""Calculator — combines basic and scientific operations into a single interface.

The Calculator class inherits from BasicOperations and ScientificOperations,
composing both feature sets into one object.  The operations package provides
a clear module boundary that separates the standard four-function arithmetic
from the scientific and advanced operation set, giving future scientific-mode
work an obvious place to grow without structural changes to this file.
"""
from .operations.basic import BasicOperations
from .operations.scientific import ScientificOperations


class Calculator(BasicOperations, ScientificOperations):
    """Full-featured calculator combining basic and scientific operations."""
