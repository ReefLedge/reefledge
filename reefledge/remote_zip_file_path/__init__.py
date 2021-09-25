from typing import Final, Union, List, Optional as Opt

from .environment import Environment as Env
from ..ftp_client import FTPClientPublic
from ..version import __version__
from .optimal_remote_zip_file_finder import OptimalRemoteZipFileFinder

PYTHON_VERSION: Final[str] = Env.python_version()
UNION = Union[List[str], str]


def infer_remote_zip_file_path(ftp_client: Opt[FTPClientPublic] = None) -> str:
    if ftp_client is None:
        ftp_client = FTPClientPublic()

        with ftp_client:
            return _infer_remote_zip_file_path(ftp_client)
    else:
        return _infer_remote_zip_file_path(ftp_client)

def _infer_remote_zip_file_path(ftp_client: FTPClientPublic) -> str:
    remote_zf_dirname = infer_remote_zip_file_directory_name()
    zip_file_name = __select_remote_zip_file(remote_zf_dirname, ftp_client)

    remote_zip_file_path: UNION
    remote_zip_file_path = remote_zf_dirname + [zip_file_name]
    remote_zip_file_path = '/'.join(remote_zip_file_path)
    remote_zip_file_path = '/' + remote_zip_file_path

    return remote_zip_file_path

def __select_remote_zip_file(
    target_remote_dir_name: List[str],
    ftp_client: FTPClientPublic) -> str:
    ###########################################################################
    finder = OptimalRemoteZipFileFinder(target_remote_dir_name, ftp_client)
    optimal_remote_zip_file_name = finder.find()

    return optimal_remote_zip_file_name


def infer_remote_zip_file_directory_name() -> List[str]: # Public function
    remote_zip_file_directory_name = []

    if Env.ON_WINDOWS:
        remote_zip_file_directory_name.append('windows')
    else:
        remote_zip_file_directory_name.append('linux')

    remote_zip_file_directory_name.append(f"python_{PYTHON_VERSION}")
    remote_zip_file_directory_name.append(__version__)

    return remote_zip_file_directory_name