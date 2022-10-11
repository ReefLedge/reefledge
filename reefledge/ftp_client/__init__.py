from typing import TypeVar

from .ftp_client_base import FTPClientBase
from .ftp_client import FTPClient
from .ftp_client_public import FTPClientPublic
from .ftp_client_private import FTPClientPrivate

FTPClientBase_type = TypeVar('FTPClientBase_type', bound=FTPClientBase)
