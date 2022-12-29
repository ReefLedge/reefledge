"""Holds the package version number."""

from typing import Final, Dict

try:
    import pdoc # type: ignore [import]
except ModuleNotFoundError:
    pass
else:
    __pdoc__: Final[Dict[str, bool]] = {'__version__': True}

# Do NOT use double quotes!
# Example (without type annotation): __version__ = '1.4.0' + '-beta.20'
__version__: Final[str] = '1.6.3'
"""Package version number"""
