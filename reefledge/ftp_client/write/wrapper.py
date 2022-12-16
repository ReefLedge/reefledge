from functools import cached_property
from typing import Iterator, Any, Tuple, Dict, Callable, List
from typing_extensions import Self
import ftplib
from time import sleep

from . import FTPSClientWritePermissions


class FTPSClientWritePermissionsWrapper():

    username: str
    password: str

    def __init__(self, *, username: str, password: str) -> None:
        self.username = username
        self.password = password

    @cached_property
    def main_ftps_client(self) -> FTPSClientWritePermissions:
        ftps_client = FTPSClientWritePermissions(
            self.username,
            self.password,
            host='reefledge-ftp-server-main.com'
        )

        return ftps_client

    @cached_property
    def backup_ftps_client(self) -> FTPSClientWritePermissions:
        ftps_client = FTPSClientWritePermissions(
            self.username,
            self.password,
            host='reefledge-ftp-server-backup.com'
        )

        return ftps_client


    def __iter__(self) -> Iterator[FTPSClientWritePermissions]:
        for ftps_client in (self.main_ftps_client, self.backup_ftps_client):
            yield ftps_client

    def __enter__(self) -> Self: # type: ignore [valid-type]
        for ftps_client in self:
            ftps_client.__enter__()

        return self

    def __exit__(self, *args: Any) -> None:
        for ftps_client in self:
            ftps_client.__exit__()


    def _call_ftps_client_method(
        self,
        ftps_client: FTPSClientWritePermissions,
        *,
        method_name: str,
        args: Tuple[Any, ...] = (),
        kwargs: Dict[str, Any] = dict()
    ) -> None:
        method: Callable[..., None] = getattr(ftps_client, method_name)

        try:
            method(*args, **kwargs)
        except ftplib.all_errors as exception:
            print(exception)
            sleep(2)


    def remove_directory(self, directory_name: str) -> None:
        for ftps_client in self:
            self._call_ftps_client_method(
                ftps_client,
                method_name='remove_directory',
                args=(directory_name,)
            )

    def upload_file(
        self,
        *,
        local_file_name: str,
        destination: List[str]
    ) -> None:
        kwargs = {
            'local_file_name': local_file_name,
            'destination': destination,
        }

        for ftps_client in self:
            self._call_ftps_client_method(
                ftps_client,
                method_name='upload_file',
                kwargs=kwargs
            )
