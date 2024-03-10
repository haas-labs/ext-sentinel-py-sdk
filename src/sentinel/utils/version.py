import sys
import platform

from typing import List, Tuple

import httpx
import sentinel


def component_versions() -> List[Tuple[str, str]]:

    return {
        "sentinel-sdk": sentinel.version.VERSION,
        "httpx": httpx.__version__,
        "python": sys.version.replace("\n", "- "),
        "platform": platform.platform(),
    }
