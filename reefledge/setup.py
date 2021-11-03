from typing import Final
import os
from multiprocessing.dummy import Lock
import shutil
from zipfile import ZipFile

from .ftp_client import FTPClientPublic
from .remote_zip_file_path import infer_remote_zip_file_path

THIS_DIR_NAME: Final[str] = os.path.abspath(
    os.path.dirname(__file__)
)


def setup() -> None:
    with Lock(): # Ensure thread safety.
        if 'reefledge' not in os.listdir(THIS_DIR_NAME) or _version_mismatch():
            _setup()


def _version_mismatch() -> bool:
    from .version import __version__
    reefledge_package_wrapper_version: str = __version__

    from .reefledge.version import __version__
    reefledge_core_package_version: str = __version__

    answer: bool = \
        reefledge_package_wrapper_version != reefledge_core_package_version

    if answer:
        __remove_reefledge_core_package()

    return answer

def __remove_reefledge_core_package() -> None:
    directory_name: str = os.path.join(
        THIS_DIR_NAME,
        'reefledge'
    )

    shutil.rmtree(directory_name)


def _setup() -> None:
    original_cwd: str = os.getcwd()
    os.chdir(THIS_DIR_NAME)

    try:
        _download_reefledge_compiled_cython_package()
    finally:
        os.chdir(original_cwd)

def _download_reefledge_compiled_cython_package() -> None:
    with FTPClientPublic() as ftp_client:
        remote_zip_file_path = infer_remote_zip_file_path(ftp_client)
        ftp_client.retrieve_file(remote_zip_file_path)

    zip_file_name: str = os.path.basename(remote_zip_file_path)
    __extract_zip_file(zip_file_name)

def __extract_zip_file(zip_file_name: str) -> None:
    with ZipFile(zip_file_name, 'r') as zf:
        zf.extractall(path=THIS_DIR_NAME)

    os.remove(zip_file_name)
