from typing import Dict


class CommonTraceDB:
    name = "trace"

    async def get(self, tx_hash: str) -> Dict:
        """
        returns trace details by transaction hash
        """
        raise NotImplementedError()
