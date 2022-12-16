import ftplib
import traceback

from .setup import setup as _setup

try:
    _setup()
except (ftplib.error_perm, ImportError):
    print(traceback.format_exc())
else:
    from . import reefledge as rl
    __doc__ = rl.__doc__
    rl.__doc__ = ""
    del rl

    from .reefledge import * # type: ignore [import]
