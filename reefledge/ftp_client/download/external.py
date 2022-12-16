from typing import Final, final
from typing_extensions import Self
from os import environ as env

from .base import FTPClientDownload

INSTALLING_REEFLEDGE_EXCEL_ADDIN: Final[bool] = (
    env.get('INSTALLING_REEFLEDGE_EXCEL_ADDIN', 'False').capitalize() ==
    'True'
)


@final
class FTPSClientExternalDownload(FTPClientDownload):

    def __enter__(self) -> Self: # type: ignore [valid-type]
        super().__enter__()

        try:
            self._probe_data_connection()
        except TimeoutError:
            if not self.trust_server_pasv_ipv4_address:
                self.trust_server_pasv_ipv4_address = True
                self.__enter__() # Retry
            elif INSTALLING_REEFLEDGE_EXCEL_ADDIN:
                raise # Since the target folder is available locally...
            else:
                self.cafile = None
                self.check_hostname = False # Solution of last resort...
                super().__enter__()

        return self

    def _probe_data_connection(self) -> None:
        self.list_directory()
