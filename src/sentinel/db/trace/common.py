import logging

from typing import Dict

logger = logging.getLogger(__name__)


class CommonTraceDB:
    name = "trace"

    async def get(self, tx_hash: str) -> Dict:
        """
        returns trace details by transaction hash
        """
        raise NotImplementedError()
