from sentinel.utils.logger import get_logger
from sentinel.models.contract import Contract


class CommonContractDB:
    name = "contract"

    def __init__(self, network: str, chain_id: int) -> None:
        """
        Common Contract DB Init
        """
        self.logger = get_logger(__name__)
        self.network = network
        self.chain_id = chain_id

    def get(self, address: str) -> Contract:
        """
        returns contract details
        """
        raise NotImplementedError()
