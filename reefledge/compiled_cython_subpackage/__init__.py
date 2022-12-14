from typing import Final
import os

IS_REEFLEDGE_WEB_SERVER: Final[bool]
try:
    IS_REEFLEDGE_WEB_SERVER = eval(os.environ['IS_REEFLEDGE_WEB_SERVER'])
except KeyError:
    IS_REEFLEDGE_WEB_SERVER = False

from .manager import Manager as CompiledCythonSubpackageManager
