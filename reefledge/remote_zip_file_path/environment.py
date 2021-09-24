from typing import Final
import sys


class Environment():

    ON_WINDOWS: Final[bool] = (sys.platform[:3] == 'win')

    @classmethod
    def python_version(cls) -> str:
        major: int = sys.version_info.major
        minor: int = sys.version_info.minor

        return f"{major}.{minor}"
