import shutil
import sys
import os
from zipfile import ZipFile


def remove_directory(directory_name: str) -> None:
    if ' ' in directory_name:
        directory_name = '"' + directory_name + '"'

    shell_command: str
    try:
        shutil.rmtree(directory_name)
    except PermissionError:
        assert sys.platform in ('linux', 'win32')

        if sys.platform == 'linux':
            shell_command = f'rm -rf {directory_name}'
        else:
            shell_command = f'rmdir /s /q {directory_name}'

        os.system(shell_command)

def extract_zip_file(zip_file_name: str) -> None:
    with ZipFile(zip_file_name, 'r') as zf:
        zf.extractall(path='')

    os.remove(zip_file_name)
