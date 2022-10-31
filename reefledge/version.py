"""Holds the package version number."""

from typing import Final, Dict

try:
    import pdoc
except ModuleNotFoundError:
    pass
else:
    __pdoc__: Final[Dict[str, bool]] = {'__version__': True}

# Do NOT use double quotes!
# Example: __version__ = '1.4.0-beta.20'
__version__: Final[str] = '1.4.0'
"""Package version number"""
