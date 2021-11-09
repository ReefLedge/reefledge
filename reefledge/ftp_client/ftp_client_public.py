from typing import final
import os

from .ftp_client import FTPClient


@final
class FTPClientPublic(FTPClient):

    def _connect(self) -> None:
        try:
            self._connect_to_main_server()
        except:
            self._connect_to_backup_server()

    def login(self) -> None:
        self._login(user_name='client', password='')


    def retrieve_file(self, remote_file_path: str) -> None:
        remote_directory_name, file_name = os.path.split(remote_file_path)
        self.cwd(remote_directory_name)
        self._retrieve_file(file_name)

    def _retrieve_file(self, file_name: str) -> None:
        with open(file_name, 'wb') as local_file:
            self.ftp_tls.retrbinary(f"RETR {file_name}", local_file.write)
