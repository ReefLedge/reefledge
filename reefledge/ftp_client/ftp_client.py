from __future__ import annotations
from typing import TYPE_CHECKING

from abc import ABC, abstractmethod
from typing import Final, Dict, final, Optional, List, Any
from ftplib import FTP_TLS
from functools import cached_property
import os
import ssl

if TYPE_CHECKING:
    from . import FTPClient_type


class FTPClient(ABC):

    HOSTS: Final[Dict[str, str]] = {
        'main': 'reefledge-ftp-server-main.com',
        'backup': 'reefledge-ftp-server-backup.com',
    }

    SERVER_PORT: Final[int] = 21

    ftp_tls: FTP_TLS

    @cached_property
    def ca_file_path(self) -> str:
        this_directory_name: str = os.path.abspath(os.path.dirname(__file__))
        ca_file_path_ = os.path.join(this_directory_name, 'isrgrootx1.pem')

        return ca_file_path_


    @final
    def connect(self, cafile: Optional[str] = None) -> None:
        self._connect(cafile)

        try:
            self._enforce_tight_security()
        except ssl.SSLCertVerificationError:
            self.connect(cafile=self.ca_file_path)

    @abstractmethod
    def _connect(self, cafile: Optional[str]) -> None:
        pass

    @final
    def _enforce_tight_security(self) -> None:
        self.ftp_tls.auth()
        self.ftp_tls.prot_p()


    @final
    def _connect_to_main_server(self, cafile: Optional[str]) -> None:
        self.__connect(
            host_address=self.HOSTS['main'],
            cafile=cafile
        )

    @final
    def _connect_to_backup_server(self, cafile: Optional[str]) -> None:
        self.__connect(
            host_address=self.HOSTS['backup'],
            cafile=cafile
        )

    def __connect(self, *, host_address: str, cafile: Optional[str]) -> None:
        ssl_context = self.__create_ssl_context(cafile)
        self.ftp_tls = FTP_TLS(context=ssl_context)
        self.ftp_tls.connect(host=host_address, port=self.SERVER_PORT)

    def __create_ssl_context(self, cafile: Optional[str]) -> ssl.SSLContext:
        try:
            ssl_context = ssl.create_default_context(cafile=cafile)
        except Exception as exception:
            if cafile is None:
                raise
            else:
                error_message: str = f'Invalid `cafile`: "{self.ca_file_path}"'
                raise exception.__class__(error_message)
        else:
            return ssl_context


    @abstractmethod
    def login(self) -> None:
        pass

    @final
    def _login(self, *, user_name: str, password: str) -> None:
        self.ftp_tls.login(user=user_name, passwd=password)


    @final
    def _cwd(self, remote_directory_name: str) -> None:
        self.ftp_tls.cwd(remote_directory_name)

    def list_directory(self, remote_directory_name: str) -> List[str]:
        return self.ftp_tls.nlst(remote_directory_name)


    def __enter__(self) -> FTPClient:
        self.connect()
        self.login()

        return self

    def __exit__(self, *args: Any) -> None:
        try:
            self.ftp_tls.quit()
        except:
            self.ftp_tls.close() # Close unilaterally.
