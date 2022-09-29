from typing import TypeVar

from .ftp_client import FTPClient
from .ftp_client_public import FTPClientPublic
from .ftp_client_private import FTPClientPrivate

FTPClient_type = TypeVar('FTPClient_type', bound=FTPClient)
