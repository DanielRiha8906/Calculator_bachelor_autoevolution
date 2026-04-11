"""Entry point for the interactive calculator session.

All session logic lives in src.session; this module is a thin wrapper that
provides the conventional ``python -m src`` and ``python src/__main__.py``
entry points.

MAX_RETRIES is re-exported here so that existing imports from this module
continue to work without modification.
"""
from .session import InteractiveSession, MAX_RETRIES  # noqa: F401


def main() -> None:
    """Run the interactive calculator session."""
    InteractiveSession().run()


if __name__ == "__main__":
    main()
