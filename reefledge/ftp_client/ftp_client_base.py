from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, final, Any
from ftplib import FTP_TLS
from functools import cached_property
import os
import ssl


class FTPClientBase(ABC):

    cafile: Optional[str]
    check_hostname: bool

    ftp_tls: FTP_TLS

    def __init__(self) -> None:
        self.cafile = None
        self.check_hostname = True

    @cached_property
    def fallback_ca_file_path(self) -> str:
        this_directory_name: str = os.path.abspath(os.path.dirname(__file__))
        ca_file_path = os.path.join(this_directory_name, 'isrgrootx1.pem')

        return ca_file_path


    @final
    def connect(self, reraise_exception: bool = False) -> None:
        self._connect()

        try:
            self._enforce_tight_security()
        except ssl.SSLCertVerificationError:
            if reraise_exception:
                raise
            else:
                self.cafile = self.fallback_ca_file_path
                self.connect(reraise_exception=True)

    @abstractmethod
    def _connect(self) -> None:
        pass

    @final
    def _enforce_tight_security(self) -> None:
        self.ftp_tls.auth()
        self.ftp_tls.prot_p()


    @abstractmethod
    def login(self) -> None:
        pass

    @final
    def _login(self, *, user_name: str, password: str) -> None:
        self.ftp_tls.login(user=user_name, passwd=password, secure=True)


    def __enter__(self) -> FTPClientBase:
        self.connect()
        self.login()

        return self

    @final
    def __exit__(self, *args: Any) -> None:
        try:
            self.ftp_tls.quit()
        except:
            self.ftp_tls.close() # Close unilaterally.
