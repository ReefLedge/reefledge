from typing import Final, Optional as Opt, Union, List

from .environment import Environment as Env
from ..ftp_client import FTPClientPublic
from ..version import __version__
from .optimal_remote_zip_file_finder import OptimalRemoteZipFileFinder

PYTHON_VERSION: Final[str] = Env.python_version()


def infer_remote_zip_file_path(ftp_client: Opt[FTPClientPublic] = None) -> str:
    if ftp_client is None:
        ftp_client = FTPClientPublic()

        with ftp_client:
            return _infer_remote_zip_file_path(ftp_client)
    else:
        return _infer_remote_zip_file_path(ftp_client)

def _infer_remote_zip_file_path(ftp_client: FTPClientPublic) -> str:
    remote_zip_file_path: Union[List[str], str] = []

    if Env.ON_WINDOWS:
        remote_zip_file_path.append('windows')
    else:
        remote_zip_file_path.append('linux')

    remote_zip_file_path.append(f"python_{PYTHON_VERSION}")
    remote_zip_file_path.append(__version__)

    zip_file_name = __select_remote_zip_file(remote_zip_file_path, ftp_client)
    remote_zip_file_path.append(zip_file_name)

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
