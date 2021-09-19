import os

from .setup import setup as _setup, THIS_DIRECTORY_NAME

if 'reefledge' not in os.listdir(THIS_DIRECTORY_NAME):
    _setup()

from . import reefledge
__doc__ = reefledge.__doc__

from .reefledge import *
