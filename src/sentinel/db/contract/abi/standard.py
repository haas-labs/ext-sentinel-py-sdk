import json
from typing import Dict, Iterator, List

from sentinel.db.contract.utils import to_signature_record
from sentinel.models.contract import ABIRecord, ABISignature
from sentinel.models.database import Database
from sentinel.utils.logger import get_logger

from .erc20 import ERC20
from .erc721 import ERC721
from .erc1155 import ERC1155
from .tranparent_proxy import TRANSPARENT_PROXY


class StandardABISignatures:
    """
    Standard ABI Signatures

    - ERC-20
    - ERC-721
    - ERC-1155
    - TransparentProxy
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
        sentry_name = kwargs.pop("sentry_name")
        sentry_hash = kwargs.pop("sentry_hash")
        standards = settings.parameters.pop("standards", [])
        kwargs.update(settings.parameters)
        return cls(standards=standards, sentry_name=sentry_name, sentry_hash=sentry_hash, **kwargs)

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
            match standard:
                case "ERC20":
                    self._load("ERC20", json.loads(ERC20))
                case "ERC721":
                    self._load("ERC721", json.loads(ERC721))
                case "ERC1155":
                    self._load("ERC1155", json.loads(ERC1155))
                case "TransparentProxy":
                    self._load("TransparentProxy", json.loads(TRANSPARENT_PROXY))
                case _:
                    self.logger.warning(f"Unknown standard name, {standard}")

    def _load(self, standard: str, abi_records: List[Dict]) -> None:
        """
        Load ABI signatures to local database
        """
        for abi_record in abi_records:
            abi_signature = to_signature_record(standard, ABIRecord(**abi_record))
            self._db.append(abi_signature)

    def search(
        self,
        standard: str = None,
        signature_type: str = None,
        signature_hash: str = None,
        signature_name: str = None,
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
            if signature_hash is not None:
                if signature.signature_hash != signature_hash:
                    continue
            if signature_name is not None:
                if signature.abi.name.lower() != signature_name.lower():
                    continue
            yield signature
