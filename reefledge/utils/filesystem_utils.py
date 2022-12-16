from typing import Final, List
import shutil
import os
import stat
import subprocess
import warnings
from zipfile import ZipFile

from .environment import Env

ON_LINUX: Final[bool] = Env.ON_LINUX
ON_MAC_OS: Final[bool] = Env.ON_MAC_OS
ON_WINDOWS: Final[bool] = Env.ON_WINDOWS


def remove_directory(directory_name: str) -> None:
    try:
        shutil.rmtree(directory_name)
    except FileNotFoundError:
        pass
    except PermissionError:
        _remove_directory_platform_specific(directory_name)

def _remove_directory_platform_specific(directory_name: str) -> None:
    __change_file_permissions(root_directory_name=directory_name)
    shell_command: List[str] = __assemble_shell_command(directory_name)
    __remove_directory_via_subprocess(shell_command, directory_name)

def __change_file_permissions(*, root_directory_name: str) -> None:
    def change_single_file_permissions(file_path: str) -> None:
        try:
            os.chmod(file_path, stat.S_IRUSR + stat.S_IWUSR)
        except PermissionError:
            pass

    dir_name: str
    file_names: List[str]
    file_path: str
    for dir_name, _, file_names in os.walk(root_directory_name):
        for file_name in file_names:
            file_path = os.path.join(dir_name, file_name)
            change_single_file_permissions(file_path)

def __assemble_shell_command(target_directory_name: str) -> List[str]:
    if (ON_LINUX or ON_MAC_OS):
        shell_command = ['rm', '-rf', target_directory_name]
    elif ON_WINDOWS:
        shell_command = ['rmdir', '/s', '/q', target_directory_name]
    else:
        raise OSError('Unsupported operating system.')

    return shell_command

def __remove_directory_via_subprocess(
    shell_command: List[str],
    directory_name: str
) -> None:
    completed_process: subprocess.CompletedProcess = subprocess.run( # type: ignore [type-arg]
        shell_command,
        shell=ON_WINDOWS
    )

    if (completed_process.returncode != 0):
        if (not ON_WINDOWS) and ('sudo' not in shell_command):
            __remove_directory_via_subprocess(
                shell_command=(['sudo'] + shell_command),
                directory_name=directory_name
            )
        else:
            warnings.warn(f'''
                Failed to remove the "{directory_name}" directory.
                Please remove it manually, if possible.
            ''')


def extract_zip_file(zip_file_name: str) -> None:
    with ZipFile(zip_file_name, 'r') as zf:
        zf.extractall(path='')

    os.remove(zip_file_name)
