import sys
import platform

from typing import List, Tuple

# import rich
# import PyYAML
import web3
import jinja2
import httpx
import aiokafka
import async_lru
import pydantic
import websockets
# import aiofiles
import sentinel


def component_versions() -> List[Tuple[str, str]]:

    return {
        "sentinel-sdk": sentinel.version.VERSION,
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
