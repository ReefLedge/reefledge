import ftplib
import traceback

from .setup import setup as _setup

try:
    _setup()
except (ftplib.error_perm, ImportError):
    print(traceback.format_exc())
else:
    from . import reefledge
    __doc__ = reefledge.__doc__
    del reefledge

    from .reefledge import __version__
    from .reefledge import *
