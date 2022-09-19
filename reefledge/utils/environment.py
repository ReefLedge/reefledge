from typing import Final
import sys

PLATFORM: Final[str] = sys.platform


class Environment():

    ON_LINUX: Final[bool] = PLATFORM.startswith('linux')
    ON_MAC_OS: Final[bool] = (PLATFORM == 'darwin')
    ON_WINDOWS: Final[bool] = (PLATFORM[:3] == 'win') or (PLATFORM == 'cygwin')

    os_name: str

    def __init__(self) -> None:
        self._set_os_name()

    def _set_os_name(self) -> None:
        if self.__class__.ON_LINUX:
            self.os_name = 'linux'
        elif self.__class__.ON_MAC_OS:
            self.os_name = 'mac_os'
        elif self.__class__.ON_WINDOWS:
            self.os_name = 'windows'


    @classmethod
    def python_version(cls) -> str:
        major: int = sys.version_info.major
        minor: int = sys.version_info.minor

        return f"{major}.{minor}"
