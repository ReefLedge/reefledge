from abc import ABC, abstractmethod
from typing import Optional, Union, final, Any
from typing_extensions import Self
from ftplib import FTP, FTP_TLS
from functools import cached_property
import os
import ssl


class FTPClientBase(ABC):

    cafile: Optional[str]
    check_hostname: bool
    trust_server_pasv_ipv4_address: bool

    ftp: Union[FTP, FTP_TLS]

    def __init__(self) -> None:
        self.cafile = None
        self.check_hostname = True
        self.trust_server_pasv_ipv4_address = False

    @property
    def trust_server_pasv_addr(self) -> bool:
        return self.trust_server_pasv_ipv4_address

    @cached_property
    def fallback_ca_file_path(self) -> str:
        this_directory_name: str = os.path.abspath(os.path.dirname(__file__))
        ca_file_path = os.path.join(this_directory_name, 'isrgrootx1.pem')

        return ca_file_path


    def connect(
        self, reraise_ssl_cert_verification_error: bool = False
    ) -> None:
        self._connect()

        try:
            self._enforce_tight_security()
        except ssl.SSLCertVerificationError:
            if reraise_ssl_cert_verification_error:
                raise
            else:
                self.cafile = self.fallback_ca_file_path
                self.connect(reraise_ssl_cert_verification_error=True)

    @abstractmethod
    def _connect(self) -> None:
        raise NotImplementedError

    @final
    def _enforce_tight_security(self) -> None:
        assert isinstance(self.ftp, FTP_TLS)

        self.ftp.set_pasv(True) # Note: passive mode should be on by default.
        self.ftp.trust_server_pasv_ipv4_address = self.trust_server_pasv_addr # type: ignore [attr-defined]

        self.ftp.auth()
        self.ftp.prot_p()


    @abstractmethod
    def login(self) -> None:
        raise NotImplementedError

    @final
    def _login(self, *, username: str, password: str) -> None:
        self.ftp.login(user=username, passwd=password)


    def __enter__(self) -> Self: # type: ignore [valid-type]
        self.connect()
        self.login()

        return self

    @final
    def __exit__(self, *args: Any) -> None:
        try:
            self.ftp.quit()
        except:
            self.ftp.close() # Close unilaterally.
