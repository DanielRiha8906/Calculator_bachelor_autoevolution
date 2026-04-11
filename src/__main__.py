"""Entry point for the calculator package.

Dispatches to one of two modes depending on whether command-line arguments
are present:

* **CLI mode** (``python -m src <operation> <operand(s)>``) — single-shot
  execution via :func:`src.cli.cli_mode`.  Returns a Unix exit code (0 on
  success, 1 on error).

* **Interactive mode** (``python -m src``) — starts the REPL loop via
  :func:`src.user_input.interactive_mode`.

Examples::

    python -m src add 3 5          # prints 8.0
    python -m src factorial 7      # prints 5040
    python -m src                  # starts interactive session
"""

import sys

from .cli import cli_mode
from .user_input import interactive_mode

if __name__ == "__main__":
    if len(sys.argv) > 1:
        sys.exit(cli_mode())
    else:
        interactive_mode()
