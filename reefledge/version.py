"""Holds the package version number."""

from typing import Final, Dict

import pdoc

__pdoc__: Final[Dict[str, bool]] = {'__version__': True}

__version__: Final[str] = '1.4.0' + '-beta.0' # Do NOT use double quotes!
"""Package version number"""
