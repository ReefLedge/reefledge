from __future__ import annotations
from typing import Final, Dict, Optional, Any
from ftplib import FTP
import os


class FTPClient():

    HOSTS: Final[Dict[str, str]] = {
        'main': '34.141.99.248',
        'backup': '34.141.99.248',
    }

    PORT: Final[int] = 21

    target_file_path: Optional[str] # Unix path
    ftp: FTP

    def __init__(self, target_file_path: Optional[str] = None) -> None:
        self.target_file_path = target_file_path
        self.ftp = FTP()

    def __enter__(self) -> FTPClient:
        self._connect()
        self.ftp.login(user='dstokes', passwd='oewfn8fdn_Qozz')
        self.ftp.set_pasv(False)

        return self

    def _connect(self) -> None:
        try:
            self.ftp.connect(host=self.HOSTS['main'], port=self.PORT)
        except:
            self.ftp.connect(host=self.HOSTS['backup'], port=self.PORT)

    def __exit__(self, *args: Any) -> None:
        try:
            self.ftp.quit()
        except:
            pass


    def retrieve_file(self, file_path: Optional[str] = None) -> None:
        if file_path is None:
            assert isinstance(self.target_file_path, str)
            file_path = self.target_file_path

        self._retrieve_file(file_path)

    def _retrieve_file(self, file_path: str) -> None:
        directory_name, file_name = os.path.split(file_path)
        self.ftp.cwd(directory_name)
        self.__effectively_retrieve_file(file_name)

    def __effectively_retrieve_file(self, file_name: str) -> None:
        with open(file_name, 'wb') as local_file:
            self.ftp.retrbinary(f"RETR {file_name}", local_file.write)
