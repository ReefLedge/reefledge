"""Holds the package version number."""

from typing import Final, Dict

import pdoc

__pdoc__: Final[Dict[str, bool]] = {'__version__': True}

# Do NOT use double quotes!
__version__: Final[str] = '1.4.0' + '-beta.6'
"""Package version number"""
