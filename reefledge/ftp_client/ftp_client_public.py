from typing import final, Optional
import os

from .ftp_client import FTPClient


@final
class FTPClientPublic(FTPClient):

    target_remote_file_path: Optional[str]

    def __init__(self, target_remote_file_path: Optional[str] = None) -> None:
        self.target_remote_file_path = target_remote_file_path
        super().__init__()


    def _connect(self) -> None:
        try:
            self._connect_to_main_server()
        except:
            self._connect_to_backup_server()

    def login(self) -> None:
        super().login(user_name='client', password='')


    def retrieve_file(self, remote_file_path: Optional[str] = None) -> None:
        if remote_file_path is None:
            assert isinstance(self.target_remote_file_path, str)
            remote_file_path = self.target_remote_file_path

        self._retrieve_file(remote_file_path)

    def _retrieve_file(self, remote_file_path: str) -> None:
        remote_directory_name, file_name = os.path.split(remote_file_path)
        self.cwd(remote_directory_name)
        self.__effectively_retrieve_file(file_name)

    def __effectively_retrieve_file(self, file_name: str) -> None:
        with open(file_name, 'wb') as local_file:
            self.ftp_tls.retrbinary(f"RETR {file_name}", local_file.write)
