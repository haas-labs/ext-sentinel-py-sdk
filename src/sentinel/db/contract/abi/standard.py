import json
from typing import Dict, Iterator, List

from sentinel.db.contract.utils import to_signature_record
from sentinel.models.contract import ABIRecord, ABISignature
from sentinel.models.database import Database
from sentinel.utils.logger import get_logger

from .erc20 import ERC20
from .erc721 import ERC721
from .erc1155 import ERC1155


class StandardABISignatures:
    """
    Standard ABI Signatures

    - ERC-20
    - ERC-721
    - ERC-1155
    """

    name = "StandardABISignatures"

    def __init__(self, standards: List[str] = list(), **kwargs) -> None:
        """
        Standard ABI Signatures Init
        """
        self.logger = get_logger(__name__)

        self._db = []
        self._standards = standards
        self.update(standards=self._standards)

    @classmethod
    def from_settings(cls, settings: Database, **kwargs):
        kwargs = kwargs.copy()
        standards = settings.parameters.pop("standards", [])
        kwargs.update(settings.parameters)
        return cls(standards=standards, **kwargs)

    @property
    def total_records(self):
        """
        returns total records number in database
        """
        return len(self._db)

    def update(self, standards: List[str] = list()) -> None:
        """
        Update ABI Signatures
        """
        if len(standards) == 0:
            return

        for standard in standards:
            if standard == "ERC20":
                self._load("ERC20", json.loads(ERC20))
            elif standard == "ERC721":
                self._load("ERC721", json.loads(ERC721))
            elif standard == "ERC1155":
                self._load("ERC1155", json.loads(ERC1155))
            else:
                self.logger.warning(f"Unknown standard name, {standard}")

    def _load(self, standard: str, abi_records: List[Dict]) -> None:
        """
        Load ABI signatures to local database
        """
        for abi_record in abi_records:
            self._db.append(to_signature_record(standard, ABIRecord(**abi_record)))

    def search(
        self,
        standard: str = None,
        signature_type: str = None,
        signature_hash: str = None,
    ) -> Iterator[ABISignature]:
        """
        Search signatures
        """
        for signature in self._db:
            if standard is not None:
                if signature.contract_address != standard:
                    continue
            if signature_type is not None:
                if signature.type != signature_type:
                    continue
            yield signature
