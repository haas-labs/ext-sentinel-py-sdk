import platform
import sys
from typing import List, Tuple

import aiokafka
import async_lru
import httpx
import jinja2
import pydantic

# import rich
# import PyYAML
import web3
import websockets

# import aiofiles


class IncorrectVersionFormat(Exception): ...


def component_versions() -> List[Tuple[str, str]]:
    return {
        "httpx": httpx.__version__,
        "python": sys.version.replace("\n", "- "),
        "platform": platform.platform(),
        "jinja2": jinja2.__version__,
        "async_lru": async_lru.__version__,
        "aiokafka": aiokafka.__version__,
        "pydantic": pydantic.__version__,
        "web3": web3.__version__,
        "websockets": websockets.__version__,
        # "aiofiles": aiofiles
        # "rich": rich,
        # "PyYAML": PyYAML
    }


def is_bugfix(main_version: str, version: str) -> bool:
    """
    Check if a version is a bug-fix version for a given major.minor version

    Parameters:
    - main_version: str - the major.minor version as string, for example: 0.1, 1.1, ...
    - version: str - the full version as string, for example: 0.1.4, 1.1.5, ...

    Returns:
    - bool: True if the version is a bug-fix version for a given major.minor version
    """

    def to_tuple(v):
        return tuple(map(int, v.split(".")))

    try:
        main_version = to_tuple(main_version)
    except ValueError:
        raise IncorrectVersionFormat(f"Incorrect main version format: {main_version}")
    if len(main_version) not in (2, 3):
        raise IncorrectVersionFormat(f"Incorrect main version format: {main_version}")

    try:
        version = to_tuple(version)
    except ValueError:
        raise IncorrectVersionFormat(f"Incorrect version format: {version}")
    if len(version) not in (2, 3):
        raise IncorrectVersionFormat(f"Incorrect version format: {version}")

    if len(main_version) == 3:
        return True if main_version == version else False
    else:
        return True if version[:2] == main_version[:2] else False
