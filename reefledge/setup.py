from typing import Final, Union, List
from multiprocessing.dummy import Lock
import os
from zipfile import ZipFile

from .environment import Environment as Env
from .version import __version__
from .ftp_client import FTPClient, THIS_DIRECTORY_NAME

CPYTHON_VERSION: Final[str] = Env.cpython_version()


def setup() -> None:
    with Lock(): # Ensure thread safety.
        original_cwd: str = os.getcwd()
        os.chdir(THIS_DIRECTORY_NAME)

        try:
            _setup()
        finally:
            os.chdir(original_cwd)

def _setup() -> None:
    remote_zip_file_path = __infer_remote_zip_file_path()
    __download_zip_file(remote_zip_file_path)
    __extract_zip_file()
    os.remove('version.py') # Avoid duplication.

def __infer_remote_zip_file_path() -> str:
    remote_zip_file_path: Union[List[str], str] = []

    if Env.ON_WINDOWS:
        remote_zip_file_path.append('windows')
    else:
        remote_zip_file_path.append('linux')

    remote_zip_file_path.append(f"python_{CPYTHON_VERSION}")
    remote_zip_file_path.append(__version__)
    remote_zip_file_path.append('reefledge.zip')

    remote_zip_file_path = '/' + '/'.join(remote_zip_file_path)
    return remote_zip_file_path

def __download_zip_file(remote_zip_file_path: str) -> None:
    with FTPClient(remote_zip_file_path) as ftp_client:
        ftp_client.retrieve_file()

def __extract_zip_file() -> None:
    with ZipFile('reefledge.zip', 'r') as zf:
        zf.extractall()

    os.remove('reefledge.zip')
