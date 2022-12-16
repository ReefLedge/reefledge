from typing import Final
import os

IS_REEFLEDGE_WEB_SERVER: Final[bool] = (
    os.environ.get('IS_REEFLEDGE_WEB_SERVER', 'False').capitalize() ==
    'True'
)

from .manager import Manager as CompiledCythonSubpackageManager
__all__ = ['CompiledCythonSubpackageManager']
