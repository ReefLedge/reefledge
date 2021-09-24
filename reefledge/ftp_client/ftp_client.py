from __future__ import annotations
from typing import Final, Dict, Optional, final, List, Any
import os
from abc import ABC, abstractmethod
from ftplib import FTP_TLS
from ssl import SSLContext

THIS_DIRECTORY_NAME: Final[str] = os.path.dirname(__file__)


class FTPClient(ABC):

    SSL_FILES_PARENT_DIRECTORY_NAME: Final[str] = os.path.join(
        THIS_DIRECTORY_NAME,
        'ssl_files'
    )

    HOSTS: Final[Dict[str, Optional[str]]] = {
        'main': '34.141.99.248',
        'backup': None,
    }

    PORT: Final[int] = 21


    cert_file_name: str
    priv_key_file_name: str

    ftp_tls: FTP_TLS

    def __init__(self) -> None:
        self.cert_file_name = 'ftp_server_certificate.pem'
        self.priv_key_file_name = 'ftp_server_private_key.pem'

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
        self.__construct_FTP_TLS_instance(backup=False)
        self.ftp_tls.connect(host=self.HOSTS['main'], port=self.PORT)

    def _connect_to_backup_server(self) -> None:
        self.__construct_FTP_TLS_instance(backup=True)
        self.ftp_tls.connect(host=self.HOSTS['backup'], port=self.PORT)


    def __construct_FTP_TLS_instance(self, backup: bool) -> None:
        ssl_context = self.__get_ssl_context(backup)
        self.ftp_tls = FTP_TLS(context=ssl_context)

    def __get_ssl_context(self, backup: bool) -> SSLContext:
        ssl_context = SSLContext()

        join = os.path.join
        parent_dirname = self.SSL_FILES_PARENT_DIRECTORY_NAME
        folder_name = ('backup_server' if backup else 'main_server')

        ssl_context.load_cert_chain(
            certfile=join(parent_dirname, folder_name, self.cert_file_name),
            keyfile=join(parent_dirname, folder_name, self.priv_key_file_name)
        )

        return ssl_context


    def login(self, user_name: str, password: str) -> None:
        self.ftp_tls.login(user=user_name, passwd=password)

    def cwd(self, remote_directory_name: str) -> None:
        self.ftp_tls.cwd(remote_directory_name)

    def list_directory(self, remote_directory_name: str) -> List[str]:
        return self.ftp_tls.nlst(remote_directory_name)

    def disable_passive_mode(self) -> None:
        self.ftp_tls.set_pasv(False)


    def __exit__(self, *args: Any) -> None:
        try:
            self.ftp_tls.quit()
        except:
            pass
