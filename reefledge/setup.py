from typing import Final
import os
from multiprocessing.dummy import Lock

from ._filesystem_utils import remove_directory, extract_zip_file
from .ftp_client import FTPClientPublic
from .remote_zip_file_path import infer_remote_zip_file_path


def setup() -> None:
    this_directory_name: Final[str] = os.path.dirname(__file__)

    with Lock(): # Ensure thread safety.
        original_cwd = os.getcwd()
        os.chdir(this_directory_name)

        try:
            _setup()
        finally:
            os.chdir(original_cwd)

def _setup() -> None:
    if 'garbage' in os.listdir():
        remove_directory('garbage')

    if 'reefledge' in os.listdir():
        if __version_mismatch():
            os.rename('reefledge', 'garbage')
            __download_reefledge_compiled_cython_package()
    else:
        __download_reefledge_compiled_cython_package()

def __version_mismatch() -> bool:
    from .version import __version__
    wrapper_version: str = __version__

    from .reefledge.version import __version__
    compiled_cython_package_version: str = __version__

    return (wrapper_version != compiled_cython_package_version)

def __download_reefledge_compiled_cython_package() -> None:
    with FTPClientPublic() as ftp_client:
        remote_zip_file_path = infer_remote_zip_file_path(ftp_client)
        ftp_client.retrieve_file(remote_zip_file_path)

    zip_file_name: str = os.path.basename(remote_zip_file_path)
    extract_zip_file(zip_file_name)
