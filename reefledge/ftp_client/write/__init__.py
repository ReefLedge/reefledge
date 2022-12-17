from typing import final, List
import ftplib
import os

from .. import FTPClient


@final
class FTPSClientWritePermissions(FTPClient):

    username: str
    password: str
    host: str

    def __init__(
        self,
        username: str,
        password: str,
        *,
        host: str
    ) -> None:
        super().__init__()

        self.username = username
        self.password = password
        self._set_host(host)

    def _set_host(self, host: str) -> None:
        if host in self.__class__.HOSTS.values():
            self.host = host
        else:
            raise ValueError(f"Invalid host {host}")


    def _connect(self) -> None:
        if self.host == self.__class__.HOSTS['main']:
            self._connect_to_main_server()
        else:
            self._connect_to_backup_server()

    def login(self) -> None:
        self._login(username=self.username, password=self.password)


    def cwd(self, directory_name: List[str]) -> None:
        folder_name: str
        for folder_name in directory_name:
            try:
                self._create_folder(folder_name)
            except ftplib.error_perm as exception:
                if '550 File exists.' in str(exception):
                    self._cwd(folder_name)
                else:
                    raise
            else:
                self._cwd(folder_name)

    def _create_folder(self, folder_name: str) -> None:
        self.ftp.mkd(folder_name)


    def remove_directory(
        self,
        directory_name: str,
        *,
        print_report: bool = True
    ) -> None:
        fso_name: str
        for fso_name in self.list_directory(directory_name):
            fso_path = f"{directory_name}/{fso_name}"

            try:
                self._delete_file(file_path=fso_path)
            except ftplib.error_perm as exception:
                if '550 Is a directory.' in str(exception):
                    self.remove_directory(
                        directory_name=fso_path,
                        print_report=False
                    )
                else:
                    raise
        else:
            self._remove_empty_directory(directory_name)

        if print_report:
            print(f'Removed directory "{directory_name}" on {self.host}')

    def _delete_file(self, file_path: str) -> None:
        self.ftp.delete(file_path)

    def _remove_empty_directory(self, directory_name: str) -> None:
        self.ftp.rmd(directory_name)


    def upload_file(
        self,
        *,
        local_file_name: str,
        destination: List[str]
    ) -> None:
        assert local_file_name in os.listdir()
        original_remote_cwd: str = self.ftp.pwd()

        self.cwd(directory_name=destination)
        try:
            self._upload_file(local_file_name)
        finally:
            self._cwd(original_remote_cwd)

    def _upload_file(self, local_file_name: str) -> None:
        try:
            self.ftp.delete(local_file_name)
        except ftplib.error_perm as exception:
            if '550 No such file or directory.' in str(exception):
                self.__upload_file(local_file_name)
            else:
                raise
        else:
            self.__upload_file(local_file_name)

        print(f'Uploaded file "{local_file_name}" to {self.host}')

    def __upload_file(self, local_file_name: str) -> None:
        with open(local_file_name, mode='rb') as fh:
            self.ftp.storbinary(f"STOR {local_file_name}", fh)


from .wrapper import FTPSClientWritePermissionsWrapper
__all__ = ['FTPSClientWritePermissionsWrapper']
