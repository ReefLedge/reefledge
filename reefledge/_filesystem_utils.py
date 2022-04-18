from typing import Final, List, Callable
import sys
import shutil
import os
import stat
import subprocess
import warnings
from zipfile import ZipFile

ON_LINUX: Final[bool] = sys.platform.startswith('linux')
ON_WINDOWS: Final[bool] = sys.platform.startswith('win')


def remove_directory(directory_name: str) -> None:
    try:
        shutil.rmtree(directory_name)
    except FileNotFoundError:
        pass
    except PermissionError:
        _remove_directory_platform_specific(directory_name)

def _remove_directory_platform_specific(directory_name: str) -> None:
    __change_file_permissions(root_directory_name=directory_name)

    if ' ' in directory_name:
        directory_name = '"' + directory_name + '"'

    shell_command: str
    if ON_LINUX:
        shell_command = f'rm -rf {directory_name}'
    elif ON_WINDOWS:
        shell_command = f'rmdir /s /q {directory_name}'
    else:
        raise OSError('Unsupported operating system.')

    __remove_directory_via_subprocess(shell_command, directory_name)

def __change_file_permissions(*, root_directory_name: str) -> None:
    def change_single_file_permissions(file_path: str) -> None:
        try:
            os.chmod(file_path, stat.S_IWUSR)
        except PermissionError:
            pass

    subdirectory_name: str
    file_names: List[str]
    file_path: str
    for subdirectory_name, _, file_names in os.walk(root_directory_name):
        for file_name in file_names:
            file_path = os.path.join(subdirectory_name, file_name)
            change_single_file_permissions(file_path)

def __remove_directory_via_subprocess(
    shell_command: str, directory_name: str) -> None:
    ###########################################################################
    is_sudo_command: Callable[[str], bool] = \
        lambda command: command.startswith('sudo')

    shell_command_split: List[str] = shell_command.split(' ')
    completed_process = subprocess.run(shell_command_split)

    if completed_process.returncode != 0:
        if ON_LINUX and (not is_sudo_command(shell_command)):
            __remove_directory_via_subprocess(
                shell_command=('sudo ' + shell_command),
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
