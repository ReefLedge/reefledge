from typing import final, ClassVar, Type, Dict
import ftplib

from .base import FTPClientDownload


@final
class FTPClientInternalDownload(FTPClientDownload):

    FTP_subclass: ClassVar[Type[ftplib.FTP]] = ftplib.FTP

    HOSTS: ClassVar[Dict[str, str]] = {
        'main': '10.156.0.3',
        'backup': '10.164.0.2',
    }

    def __init__(self) -> None:
        pass

    def connect(self) -> None: # type: ignore [override]
        self._connect()

    def _create_ssl_context(self) -> None: # type: ignore [override]
        return
