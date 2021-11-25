from typing import final, List
import os

from .ftp_client import FTPClient


@final
class FTPClientPrivate(FTPClient):

    user_name: str
    password: str
    host_address: str

    def __init__(
        self,
        user_name: str,
        password: str,
        host_address: str) -> None:
        ################################################################
        self.user_name = user_name
        self.password = password

        if host_address in self.HOSTS.values():
            self.host_address = host_address
        else:
            raise RuntimeError('Invalid host address.')


    def _connect(self) -> None:
        if self.host_address == self.HOSTS['main']:
            self._connect_to_main_server()
        else:
            self._connect_to_backup_server()

    def login(self) -> None:
        self._login(user_name=self.user_name, password=self.password)


    def upload_file(
        self, *,
        local_file_name: str,
        destination: List[str]) -> None:
        #######################################################################
        assert local_file_name in os.listdir()
        self.cwd(remote_directory_name=destination)
        self._upload_file(local_file_name)

    def _upload_file(self, local_file_name: str) -> None:
        try:
            self.ftp_tls.delete(local_file_name)
        except:
            pass
        finally:
            with open(local_file_name, 'rb') as fh:
                self.ftp_tls.storbinary(f"STOR {local_file_name}", fh)

        print(f"Uploaded file {local_file_name} to {self.host_address}.")


    def cwd(self, remote_directory_name: List[str]) -> None:
        folder_name: str
        for folder_name in remote_directory_name:
            try:
                self.ftp_tls.mkd(folder_name)
            except:
                pass
            finally:
                super().cwd(folder_name)
