from typing import Final, List, Optional, Union

from ..utils.environment import Env
from ..ftp_client import FTPClientDownload
from .optimal_remote_zip_file_finder import OptimalRemoteZipFileFinder

PYTHON_VERSION: Final[str] = Env.python_version()


def assemble_remote_zip_file_directory_name( # Public function
    *,
    package_version: str,
    python_version: str,
    operating_system: str,
) -> List[str]:
    remote_zip_file_directory_name = [
        package_version,
        python_version,
        operating_system,
    ]

    return remote_zip_file_directory_name

def infer_remote_zip_file_directory_name() -> List[str]: # Public function
    remote_zip_file_directory_name = assemble_remote_zip_file_directory_name(
        package_version=Env.reefledge_package_version(),
        python_version=f"python_{PYTHON_VERSION}",
        operating_system=Env.operating_system()
    )

    return remote_zip_file_directory_name


def pick_optimal_remote_zip_file( # Public function
    *,
    target_remote_directory_name: List[str],
    ftp_client: FTPClientDownload,
    client_ipv4_address: Optional[str] = None
) -> str:
    finder = OptimalRemoteZipFileFinder(
        target_remote_directory_name,
        ftp_client,
        client_ipv4_address
    )

    optimal_remote_zip_file_name = finder.find()
    return optimal_remote_zip_file_name


def infer_remote_zip_file_path(
    ftp_client: Optional[FTPClientDownload] = None
) -> str:
    if ftp_client is None:
        with FTPClientDownload() as ftp_client_:
            return _infer_remote_zip_file_path(ftp_client_)
    else:
        return _infer_remote_zip_file_path(ftp_client)

def _infer_remote_zip_file_path(ftp_client: FTPClientDownload) -> str:
    remote_zip_file_directory_name = infer_remote_zip_file_directory_name()

    zip_file_name: str = pick_optimal_remote_zip_file(
        target_remote_directory_name=remote_zip_file_directory_name,
        ftp_client=ftp_client
    )

    remote_zip_file_path: Union[List[str], str]
    remote_zip_file_path = remote_zip_file_directory_name + [zip_file_name]
    remote_zip_file_path = '/'.join(remote_zip_file_path)
    remote_zip_file_path = '/' + remote_zip_file_path

    return remote_zip_file_path
