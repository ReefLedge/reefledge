"""Holds the package version number."""

from typing import Final, Dict

import pdoc

__pdoc__: Final[Dict[str, bool]] = {'__version__': True}

__version__: Final[str] = '1.4.0' + '-alpha.0'
"""Package version number"""
