from abc import ABC
from typing import Final, Dict, final, Optional, List
import ssl
from ftplib import FTP_TLS

from .ftp_client_base import FTPClientBase


class FTPClient(FTPClientBase, ABC):

    HOSTS: Final[Dict[str, str]] = {
        'main': 'reefledge-ftp-server-main.com',
        'backup': 'reefledge-ftp-server-backup.com',
    }

    SERVER_PORT: Final[int] = 21

    @final
    def _connect_to_main_server(self) -> None:
        self.__connect(host=self.HOSTS['main'])

    @final
    def _connect_to_backup_server(self) -> None:
        self.__connect(host=self.HOSTS['backup'])

    def __connect(self, *, host: str) -> None:
        ssl_context = self.__create_ssl_context()
        self.ftp_tls = FTP_TLS(context=ssl_context)
        self.ftp_tls.connect(host=host, port=self.SERVER_PORT)

    def __create_ssl_context(self) -> ssl.SSLContext:
        try:
            ssl_context = ssl.create_default_context(cafile=self.cafile)
        except Exception as exception:
            if self.cafile is None:
                raise
            else:
                error_msg = f'Invalid `cafile`: "{self.fallback_ca_file_path}"'
                raise exception.__class__(error_msg)
        else:
            ssl_context.check_hostname = self.check_hostname
            return ssl_context


    @final
    def _cwd(self, remote_directory_name: str) -> None:
        self.ftp_tls.cwd(remote_directory_name)

    @final
    def list_directory(
        self,
        remote_directory_name: Optional[str] = None
    ) -> List[str]:
        args: List[str] = []

        if remote_directory_name is not None:
            args.append(remote_directory_name)

        return self.ftp_tls.nlst(*args)
