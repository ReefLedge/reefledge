from __future__ import annotations
from typing import Final, Dict, Optional, Any
import os
from ftplib import FTP_TLS
from ssl import SSLContext

THIS_DIRECTORY_NAME: Final[str] = os.path.dirname(__file__)


class FTPClient():

    SSL_FILES_PARENT_DIRECTORY_NAME: Final[str] = os.path.join(
        THIS_DIRECTORY_NAME,
        '..', 'ssl_files'
    )

    HOSTS: Final[Dict[str, str]] = {
        'main': '34.141.99.248',
        'backup': '34.141.99.248',
    }

    PORT: Final[int] = 21


    target_file_path: Optional[str] # Linux path
    cert_file_name: str
    priv_key_file_name: str

    ftp_tls: FTP_TLS

    def __init__(self, target_file_path: Optional[str] = None) -> None:
        self.target_file_path = target_file_path
        self.cert_file_name = 'ftp_server_certificate.pem'
        self.priv_key_file_name = 'ftp_server_private_key.pem'

    def __enter__(self) -> FTPClient:
        self.connect()
        self.login()
        #self.disable_passive_mode()

        return self


    def connect(self) -> None:
        try:
            self._connect_to_main_server()
        except:
            self._connect_to_backup_server()
        finally:
            self._enforce_tight_security()

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

    def _enforce_tight_security(self) -> None:
        self.ftp_tls.auth()
        self.ftp_tls.prot_p()


    def login(self, user_name: str = 'client') -> None:
        self.ftp_tls.login(user=user_name)

    def disable_passive_mode(self) -> None:
        self.ftp_tls.set_pasv(False)


    def retrieve_file(self, file_path: Optional[str] = None) -> None:
        if file_path is None:
            assert isinstance(self.target_file_path, str)
            file_path = self.target_file_path

        self._retrieve_file(file_path)

    def _retrieve_file(self, file_path: str) -> None:
        directory_name, file_name = os.path.split(file_path)
        self.ftp_tls.cwd(directory_name)
        self.__effectively_retrieve_file(file_name)

    def __effectively_retrieve_file(self, file_name: str) -> None:
        with open(file_name, 'wb') as local_file:
            self.ftp_tls.retrbinary(f"RETR {file_name}", local_file.write)


    def __exit__(self, *args: Any) -> None:
        try:
            self.ftp_tls.quit()
        except:
            pass
