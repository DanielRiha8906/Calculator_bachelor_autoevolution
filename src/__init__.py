"""Calculator package.

Exports the :class:`~src.calculator.Calculator` class as the primary public
interface. Use ``python -m src`` to start the interactive menu or pass
operation arguments for single-shot CLI mode.
"""
from .calculator import Calculator

__all__ = ["Calculator"]