"""GUI entry point for the Calculator application.

Usage:
    python gui.py

Opens the tkinter calculator window.  All arithmetic is handled by the
existing CalculatorSession; this file is a thin launcher only.
"""
from src.gui import main

if __name__ == "__main__":
    main()
