import os
import logging
from typing import cast

from .utils.filesystem_utils import remove_directory
from .compiled_cython_subpackage import CompiledCythonSubpackageManager


def setup() -> None:
    this_directory_name: str = os.path.abspath(os.path.dirname(__file__))
    original_cwd: str = os.getcwd()

    os.chdir(this_directory_name)
    try:
        _setup()
    finally:
        os.chdir(original_cwd)

def _setup() -> None:
    __remove_garbage_directory()

    with CompiledCythonSubpackageManager() as manager:
        if 'reefledge' in os.listdir():
            if __version_mismatch():
                manager.update()
        else:
            manager.download()

def __remove_garbage_directory() -> None:
    if (g:='garbage') in os.listdir():
        remove_directory(g)

def __version_mismatch() -> bool:
    from .version import __version__ as python_wrapper_version

    try:
        from .reefledge.version import __version__ as cython_subpackage_version # type: ignore [import]
    except ModuleNotFoundError:
        return True
    except ImportError:
        logging.getLogger('reefledge').exception('Version mismatch.')
        return True
    else:
        return cast(bool, python_wrapper_version != cython_subpackage_version)
