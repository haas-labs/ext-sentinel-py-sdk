import logging

from sentinel.models.contract import Contract


logger = logging.getLogger(__name__)


class CommonContractDB:
    name = "contract"

    def __init__(self, network: str, chain_id: int) -> None:
        """
        Common Contract DB Init
        """
        self.network = network
        self.chain_id = chain_id

    def get(self, address: str) -> Contract:
        """
        returns contract details
        """
        raise NotImplementedError()
