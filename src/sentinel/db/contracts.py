from typing import List
from sentinel.models.contract import Contract


class ContractDB:
    name = "contract"

    def __init__(self) -> None:
        """
        Contract DB Init
        """
        # The list of contracts
        self._db: List[Contract] = []

    def load(self, uri: str) -> None:
        """
        Load Contract DB locally
        """
        raise NotImplementedError

    def get(self, address: str) -> Contract:
        """
        returns contract details by an address
        """
        for contract in self._db:
            if contract.address == address:
                return contract
        return None

    def is_suspicious(self, address: str) -> Contract:
        """
        returns Contract details if contact address is suspicious
        """
        for contract in self._db:
            if contract.address == address and contract.suspicious is True:
                return contract
        return None

    def is_verified(self, address: str) -> Contract:
        """
        returns Contract details if contact address is verified
        """
        for contract in self._db:
            if contract.address == address and contract.verified is True:
                return contract
        return None

    def is_malicious(self, address: str) -> Contract:
        """
        returns Contract details if contact address is malicious

        the ML model marked the contract as malicious according to
        the OPCODE of the contract
        """
        for contract in self._db:
            if contract.address == address and contract.malicious is True:
                return contract
        return None
