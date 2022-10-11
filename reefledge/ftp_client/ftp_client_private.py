from typing import final, List
import os

from .ftp_client import FTPClient


@final
class FTPClientPrivate(FTPClient):

    user_name: str
    password: str
    host: str

    def __init__(
        self,
        user_name: str,
        password: str,
        host: str
    ) -> None:
        super().__init__()

        self.user_name = user_name
        self.password = password
        self._set_host(host)

    def _set_host(self, host: str) -> None:
        if host in self.HOSTS.values():
            self.host = host
        else:
            raise RuntimeError(f"Invalid host '{self.host}'")


    def _connect(self) -> None:
        if self.host == self.HOSTS['main']:
            self._connect_to_main_server()
        else:
            self._connect_to_backup_server()

    def login(self) -> None:
        self._login(user_name=self.user_name, password=self.password)


    def upload_file(
        self,
        *,
        local_file_name: str,
        destination: List[str]
    ) -> None:
        assert local_file_name in os.listdir()
        self.cwd(remote_directory_name=destination)
        self._upload_file(local_file_name)

    def _upload_file(self, local_file_name: str) -> None:
        try:
            self.ftp_tls.delete(local_file_name)
        except:
            pass
        finally:
            with open(local_file_name, mode='rb') as fh:
                self.ftp_tls.storbinary(f"STOR {local_file_name}", fh)

        print(f"Uploaded file {local_file_name} to {self.host}")


    def cwd(self, remote_directory_name: List[str]) -> None:
        folder_name: str
        for folder_name in remote_directory_name:
            try:
                self.ftp_tls.mkd(folder_name)
            except:
                pass
            finally:
                self._cwd(folder_name)
