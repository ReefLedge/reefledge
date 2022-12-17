from __future__ import annotations

from typing import Any
import os
import sys

from requests import HTTPError

from ..ftp_client.download import *
from . import IS_REEFLEDGE_WEB_SERVER
from ..remote_zip_file import infer_remote_zip_file_path
from ..utils.environment import Env
from ..https.download import download_file
from ..utils.filesystem_utils import extract_zip_file


class Manager():

    ftp_client: FTPClientDownload
    zip_file_name: str

    def __init__(self) -> None:
        if IS_REEFLEDGE_WEB_SERVER:
            self.ftp_client = FTPClientInternalDownload()
        else:
            self.ftp_client = FTPSClientExternalDownload()

    def __enter__(self) -> Manager:
        return self

    def __exit__(self, *args: Any) -> None:
        pass


    def download(self) -> None:
        if IS_REEFLEDGE_WEB_SERVER:
            self._download_via_ftp()
        else:
            try:
                self._download_via_https()
            except HTTPError:
                self._download_via_ftp()

        extract_zip_file(self.zip_file_name)

    def _download_via_ftp(self) -> None:
        with self.ftp_client:
            remote_zip_file_path = infer_remote_zip_file_path(self.ftp_client)
            self.ftp_client.retrieve_file(remote_zip_file_path)

        self.zip_file_name = os.path.basename(remote_zip_file_path)

    def _download_via_https(self) -> None:
        json = {
            'reefledge_package_version': Env.reefledge_package_version(),
            'python_version': Env.python_version(),
            'operating_system': Env.operating_system(),
        }

        self.zip_file_name = download_file(
            url='https://reefledge.com/compiled_cython_subpackage',
            json=json
        )


    def update(self) -> None:
        self._unload()
        os.rename('reefledge', 'garbage')
        self.download()

    @classmethod
    def _unload(cls) -> None:
        k: str
        for k in sys.modules.copy():
            if 'reefledge.reefledge' in k:
                sys.modules.pop(k)
