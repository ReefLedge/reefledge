import shutil
import sys
from typing import List
import os
import stat
from zipfile import ZipFile


def remove_directory(directory_name: str) -> None:
    if ' ' in directory_name:
        directory_name = '"' + directory_name + '"'

    try:
        shutil.rmtree(directory_name)
    except PermissionError:
        _remove_directory_platform_specific(directory_name)

def _remove_directory_platform_specific(directory_name: str) -> None:
        assert sys.platform in ('linux', 'win32')
        __change_permissions(root_directory_name=directory_name)

        if sys.platform == 'linux':
            shell_command = f'rm -rf {directory_name}'
        else:
            shell_command = f'rmdir /s /q {directory_name}'

        os.system(shell_command)

def __change_permissions(root_directory_name: str) -> None:
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
