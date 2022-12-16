from abc import ABC
from typing import ClassVar, Dict, Type, Final, final, Optional, Union, List
import ftplib
import ssl

from .base import FTPClientBase


class FTPClient(FTPClientBase, ABC):

    HOSTS: ClassVar[Dict[str, str]] = {
        'main': 'reefledge-ftp-server-main.com',
        'backup': 'reefledge-ftp-server-backup.com',
    }

    FTP_subclass: ClassVar[Type[ftplib.FTP]] = ftplib.FTP_TLS
    SERVER_PORT: Final[int] = 21

    @final
    def _connect_to_main_server(self) -> None:
        self.__connect(host=self.__class__.HOSTS['main'])

    @final
    def _connect_to_backup_server(self) -> None:
        self.__connect(host=self.__class__.HOSTS['backup'])

    def __connect(self, *, host: str) -> None:
        ssl_context = self._create_ssl_context()
        kwargs = self.__get_FTP_subclass_constructor_kwargs(ssl_context)

        self.ftp = self.__class__.FTP_subclass(**kwargs) # type: ignore [arg-type]
        self.ftp.connect(host=host, port=self.__class__.SERVER_PORT)

    def _create_ssl_context(self) -> ssl.SSLContext:
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

    def __get_FTP_subclass_constructor_kwargs(
        self, ssl_context: Optional[ssl.SSLContext]
    ) -> Dict[str, ssl.SSLContext]:
        FTP_subclass_constructor_kwargs = dict()

        if ssl_context is not None:
            FTP_subclass_constructor_kwargs['context'] = ssl_context

        return FTP_subclass_constructor_kwargs


    @final
    def _cwd(self, directory_name: str) -> None:
        self.ftp.cwd(directory_name)

    @final
    def list_directory(
        self,
        directory_name: Union[List[str], str, None] = None
    ) -> List[str]:
        args: List[str]
        if isinstance(directory_name, list):
            args = directory_name
        else:
            args = []
            if isinstance(directory_name, str):
                args.append(directory_name)

        return self.ftp.nlst(*args)


from .download import *
from .write import FTPSClientWritePermissionsWrapper

__all__ = [
    'FTPClientDownload',
    'FTPSClientExternalDownload',
    'FTPClientInternalDownload',
    'FTPSClientWritePermissionsWrapper',
]
