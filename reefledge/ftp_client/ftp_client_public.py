from __future__ import annotations

from typing import Final, final
import os

from .ftp_client import FTPClient

INSTALLING_REEFLEDGE_EXCEL_ADDIN: Final[bool] = eval(
    os.environ.get('INSTALLING_REEFLEDGE_EXCEL_ADDIN', 'False')
)


@final
class FTPClientPublic(FTPClient):

    def __enter__(self) -> FTPClientPublic:
        super().__enter__()

        try:
            self._probe_data_connection()
        except TimeoutError:
            if not self.trust_server_pasv_ipv4_address:
                self.trust_server_pasv_ipv4_address = True
                self.__enter__()
            elif INSTALLING_REEFLEDGE_EXCEL_ADDIN:
                raise # Since the target folder is available locally...
            else:
                self.cafile = None
                self.check_hostname = False # Solution of last resort...
                super().__enter__()

        return self

    def _probe_data_connection(self) -> None:
        self.list_directory()


    def _connect(self) -> None:
        try:
            self._connect_to_main_server()
        except TimeoutError:
            self._connect_to_backup_server()

    def login(self) -> None:
        self._login(user_name='client', password='')


    def retrieve_file(self, remote_file_path: str) -> None:
        remote_directory_name, file_name = os.path.split(remote_file_path)
        self._cwd(remote_directory_name)
        self._retrieve_file(file_name)

    def _retrieve_file(self, file_name: str) -> None:
        with open(file_name, mode='wb') as local_file:
            self.ftp_tls.retrbinary(f"RETR {file_name}", local_file.write)
