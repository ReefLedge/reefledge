from abc import ABC
from typing import Final, final
from random import uniform
import os

from pydantic import NonNegativeFloat

from .. import FTPClient


class FTPClientDownload(FTPClient, ABC):

    LOAD_BALANCE: Final[bool] = False

    @final
    def _connect(self) -> None:
        if self.LOAD_BALANCE:
            self.__connect_randomly()
        else:
            self.__connect_hierarchically()

    def __connect_randomly(self) -> None:
        u: NonNegativeFloat = uniform(0, 1)

        if u <= 0.5:
            self._connect_to_main_server()
        else:
            self._connect_to_backup_server()

    def __connect_hierarchically(self) -> None:
        try:
            self._connect_to_main_server()
        except TimeoutError:
            self._connect_to_backup_server()


    @final
    def login(self) -> None:
        self._login(username='client', password='')

    @final
    def retrieve_file(self, remote_file_path: str) -> None:
        local_file_name: str = os.path.basename(remote_file_path)

        with open(local_file_name, mode='wb') as local_file:
            self.ftp.retrbinary(f"RETR {remote_file_path}", local_file.write)
