from typing import Final
import sys

PLATFORM: Final[str] = sys.platform


class Environment():

    ON_WINDOWS: Final[bool] = (PLATFORM[:3] == 'win') or (PLATFORM == 'cygwin')

    @classmethod
    def python_version(cls) -> str:
        major: int = sys.version_info.major
        minor: int = sys.version_info.minor

        return f"{major}.{minor}"
