from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Final, Dict, Optional, final, List, Any
from ftplib import FTP_TLS
from functools import cached_property
import ssl
import os


class FTPClient(ABC):

    HOSTS: Final[Dict[str, Optional[str]]] = {
        'main': 'reefledge-ftp-server-main.com',
        'backup': 'reefledge-ftp-server-backup.com',
    }

    SERVER_PORT: Final[int] = 21

    ftp_tls: FTP_TLS

    def __enter__(self) -> FTPClient:
        self.connect()
        self.login()

        return self


    @final
    def connect(self) -> None:
        self._connect()
        self._enforce_tight_security()

    @abstractmethod
    def _connect(self) -> None:
        pass

    def _enforce_tight_security(self) -> None:
        self.ftp_tls.auth()
        self.ftp_tls.prot_p()


    def _connect_to_main_server(self) -> None:
        self.__connect(host_address=self.HOSTS['main'])

    def _connect_to_backup_server(self) -> None:
        self.__connect(host_address=self.HOSTS['backup'])

    def __connect(self, *, host_address: str) -> None:
        self.ftp_tls = FTP_TLS(context=self.ssl_context)
        self.ftp_tls.connect(host=host_address, port=self.SERVER_PORT)

    @cached_property
    def ssl_context(self) -> ssl.SSLContext:
        try:
            _ssl_context = ssl.create_default_context(cafile=self.ca_file_path)
        except Exception as exception:
            error_message: str = f'Invalid `cafile`: "{self.ca_file_path}"'
            raise exception.__class__(error_message)
        else:
            return _ssl_context

    @cached_property
    def ca_file_path(self) -> str:
        this_directory_name: str = os.path.abspath(os.path.dirname(__file__))
        _ca_file_path = os.path.join(this_directory_name, 'isrgrootx1.pem')

        return _ca_file_path


    @abstractmethod
    def login(self) -> None:
        pass

    def _login(self, *, user_name: str, password: str) -> None:
        self.ftp_tls.login(user=user_name, passwd=password)


    def cwd(self, remote_directory_name: str) -> None:
        self.ftp_tls.cwd(remote_directory_name)

    def list_directory(self, remote_directory_name: str) -> List[str]:
        return self.ftp_tls.nlst(remote_directory_name)


    def __exit__(self, *args: Any) -> None:
        try:
            self.ftp_tls.quit()
        except:
            self.ftp_tls.close() # Close unilaterally.
