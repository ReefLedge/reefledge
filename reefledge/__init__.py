import os
from ftplib import error_perm
import traceback

from .setup import setup as _setup, THIS_DIRECTORY_NAME

try:
    if 'reefledge' not in os.listdir(THIS_DIRECTORY_NAME):
        _setup()
except error_perm:
    print(traceback.format_exc())
else:
    from . import reefledge
    __doc__ = reefledge.__doc__

    from .reefledge import *
    from .reefledge import __version__
