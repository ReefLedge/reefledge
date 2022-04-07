import shutil
from typing import List
import os
import stat
import sys
from zipfile import ZipFile


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

    if sys.platform.startswith('linux'):
        shell_command = f'rm -rf {directory_name}'
    elif sys.platform.startswith('win'):
        shell_command = f'rmdir /s /q {directory_name}'
    else:
        raise OSError('Unsupported operating system.')

    os.system(shell_command)

def __change_file_permissions(root_directory_name: str) -> None:
    subdirectory_name: str
    file_names: List[str]
    file_path: str
    for subdirectory_name, _, file_names in os.walk(root_directory_name):
        for file_name in file_names:
            file_path = os.path.join(subdirectory_name, file_name)
            os.chmod(file_path, stat.S_IWUSR)


def extract_zip_file(zip_file_name: str) -> None:
    with ZipFile(zip_file_name, 'r') as zf:
        zf.extractall(path='')

    os.remove(zip_file_name)
