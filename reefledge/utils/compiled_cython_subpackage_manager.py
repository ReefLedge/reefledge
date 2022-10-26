import os
import sys

from ..ftp_client import FTPClientPublic
from ..remote_zip_file_path import infer_remote_zip_file_path
from .filesystem_utils import extract_zip_file


def download() -> None:
    with FTPClientPublic() as ftp_client:
        remote_zip_file_path = infer_remote_zip_file_path(ftp_client)
        ftp_client.retrieve_file(remote_zip_file_path)

    zip_file_name: str = os.path.basename(remote_zip_file_path)
    extract_zip_file(zip_file_name)


def update() -> None:
    _unload()
    os.rename('reefledge', 'garbage')
    download()

def _unload() -> None:
    k: str
    for k in sys.modules.copy():
        if 'reefledge.reefledge' in k:
            sys.modules.pop(k)
