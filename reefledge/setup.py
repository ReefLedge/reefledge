import os
import logging

from ._filesystem_utils import remove_directory, extract_zip_file
from .ftp_client import FTPClientPublic
from .remote_zip_file_path import infer_remote_zip_file_path


def setup() -> None:
    this_directory_name: str = os.path.abspath(os.path.dirname(__file__))
    original_cwd: str = os.getcwd()
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
    from .version import __version__ as wrapper_version

    try:
        from .reefledge.version import __version__ as cython_package_version
    except ModuleNotFoundError:
        return True
    except ImportError:
        logging.getLogger('reefledge').exception('Version mismatch.')
        return True
    else:
        return (wrapper_version != cython_package_version)

def __download_reefledge_compiled_cython_package() -> None:
    with FTPClientPublic() as ftp_client:
        remote_zip_file_path = infer_remote_zip_file_path(ftp_client)
        ftp_client.retrieve_file(remote_zip_file_path)

    zip_file_name: str = os.path.basename(remote_zip_file_path)
    extract_zip_file(zip_file_name)
