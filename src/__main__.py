import sys

from .cli import cli_mode
from .user_input import interactive_mode

if __name__ == "__main__":
    if len(sys.argv) > 1:
        sys.exit(cli_mode())
    else:
        interactive_mode()
