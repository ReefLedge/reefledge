from typing import Final
import os
from multiprocessing.dummy import Lock
from zipfile import ZipFile

from .ftp_client import FTPClientPublic
from .remote_zip_file_path import infer_remote_zip_file_path

THIS_DIRECTORY_NAME: Final[str] = os.path.dirname(__file__)


def setup() -> None:
    if 'reefledge' not in os.listdir(THIS_DIRECTORY_NAME):
        with Lock(): # Ensure thread safety.
            original_cwd: str = os.getcwd()
            os.chdir(THIS_DIRECTORY_NAME)

            try:
                _setup()
            finally:
                os.chdir(original_cwd)

def _setup() -> None:
    with FTPClientPublic() as ftp_client:
        remote_zip_file_path = infer_remote_zip_file_path(ftp_client)
        ftp_client.retrieve_file(remote_zip_file_path)

    zip_file_name: str = os.path.basename(remote_zip_file_path)
    __extract_zip_file(zip_file_name)

    os.remove('version.py') # Avoid duplication.

def __extract_zip_file(zip_file_name: str) -> None:
    with ZipFile(zip_file_name, 'r') as zf:
        zf.extractall()

    os.remove(zip_file_name)
    os.rename(zip_file_name[:-4], 'reefledge')
