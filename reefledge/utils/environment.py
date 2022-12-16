from typing import Final
from typing_extensions import assert_never
import sys

PLATFORM: Final[str] = sys.platform


class Environment():

    ON_LINUX: Final[bool] = PLATFORM.startswith('linux')
    ON_MAC_OS: Final[bool] = (PLATFORM == 'darwin')
    ON_WINDOWS: Final[bool] = (PLATFORM[:3] == 'win') or (PLATFORM == 'cygwin')

    @classmethod
    def reefledge_package_version(cls) -> str:
        from ..version import __version__ # Can only import safely at runtime.
        return __version__

    @classmethod
    def python_version(cls) -> str:
        major: int = sys.version_info.major
        minor: int = sys.version_info.minor

        return f"{major}.{minor}"

    @classmethod
    def operating_system(cls) -> str:
        if cls.ON_LINUX:
            return 'linux'
        elif cls.ON_MAC_OS:
            return 'mac_os'
        elif cls.ON_WINDOWS:
            return 'windows'
        else:
            assert False


Env = Environment # Alias
